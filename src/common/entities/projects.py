import time

from src.common.database import db
from src.common.entities import users
from src.common.util import uid

class Project:
    def __init__(
        self, 
        _id: str,
        name: str,
        description: str = "",
        instructions: str = "",
        owner_id: str = None,
        flags: int = 0,
        shared: bool = False,
        remixable: bool = True,
        unlisted: bool = False,
        history: dict = {},
        stats: dict = {}
    ):
        self.id = _id
        self.name = name
        self.description = description
        self.instructions = instructions
        self.owner = users.get_user(_id=owner_id)
        self.flags = flags
        self.shared = shared
        self.remixable = remixable
        self.unlisted = unlisted
        self.history = history
        self.stats = stats


def create_project(name: str, owner_id: str, flags: int = 0):
    # Create project data
    project_id = uid.oid()
    project = {
        "_id": project_id,
        "name": name,
        "owner_id": owner_id,
        "flags": flags,
        "history": {"created": int(time.time())}
    }

    # Create project object (TODO: Figure out what file server we'll use)

    # Create database item
    db.projects.insert_one(project)

    # Return project
    return Project(**project)
