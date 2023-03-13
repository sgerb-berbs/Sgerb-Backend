import bcrypt
import time

from src.common.database import db
from src.common.util import uid, errors, profanity

DELETED = {
    "_id": "0",
    "username": "Deleted",
    "lower_username": "deleted",
    "history": {"joined": 0}
}

class User:
    def __init__(
        self,
        _id: str,
        username: str,
        lower_username: str,
        history: dict = {},
        admin: bool = False,
        banned_until: int = 0,
        stats: dict = {"followers": 0, "following": 0, "projects": 0},
        bio: str = "",
        profile: dict = {},
        appearing_offline: bool = False,
        config: bytes = None,
        secure_data: bytes = None
    ):
        self.id = _id
        self.username = username
        self.lower_username = lower_username
        self.history = history
        self.admin = admin
        self.banned_until = banned_until
        self.stats = stats
        self.bio = bio
        self.profile = profile
        self.appearing_offline = appearing_offline
        self._config = config
        self._secure_data = secure_data

    @property
    def public(self):
        return {
            "id": self.id,
            "username": self.username,
            "history": self.history,
            "admin": self.admin,
            "stats": self.stats,
            "bio": self.bio,
            "profile": self.profile,
            "online": self.public_online_status
        }

    @property
    def client(self):
        return {
            "id": self.id,
            "username": self.username,
            "history": self.history,
            "admin": self.admin,
            "banned_until": self.banned_until,
            "stats": self.stats,
            "bio": self.bio,
            "profile": self.profile,
            "online": self.online_status,
            "appearing_offline": self.appearing_offline,
            "config": self.config
        }
    
    @property
    def partial(self):
        return {
            "id": self.id,
            "username": self.username,
            "online": self.online_status
        }

    @property
    def public_online_status(self):
        return (False if self.appearing_offline else self.online_status)

    @property
    def online_status(self):
        pass  # TODO: Get Redis working so we can store online statuses

    @property
    def authentication_settings(self):
        return db.authentication.find_one({"_id": self.id}, projections={"_id": 0})
    
    def check_password(self, password: str):
        hashed_password = self.authentication_settings["password"]
        return bcrypt.checkpw(password.encode(), hashed_password)


def username_exists(username: str) -> bool:
    if db.users.find_one({"lower_username": username.lower()},
                         projection={"_id": 1}): return True
    return False


def get_user(_id: str = None, username: str = None, return_deleted=True) -> User:
    user = db.users.find_one(({"_id": _id} if _id else {"lower_username": username.lower()}))
    if (not user) and return_deleted: return User(**DELETED)
    if not user: raise errors
    return User(**user)


def create_user(username: str, password: str, email: str = None, admin: bool = False) -> User:
    # Run validations
    if profanity.check(username): raise errors.UsernameInappropriate
    if username_exists(username): raise errors.UsernameExists

    # Create user data
    user_id = uid.oid()
    user = {
        "_id": user_id,
        "username": username,
        "lower_username": username.lower(),
        "email": email,
        "history": {"joined": int(time.time())},
        "admin": admin
    }
    authentication = {
        "_id": user_id,
        "password": bcrypt.hashpw(password.encode(), bcrypt.gensalt(12)),
        "last_updated": int(time.time())
    }

    # Create database items
    db.users.insert_one(user)
    db.authentication.insert_one(authentication)

    # Return user
    return User(**user)
