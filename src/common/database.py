from pymongo import MongoClient

from src.common.util import config


DB_COLLECTIONS = [
    "config",
    "users",
    "authentication",
    "relationships",
    "uploads",
    "projects",
    "project_assets",
    "comments",
    "forum_topics",
    "forum_posts",
    "cloud_variables"
]


# Connect to MongoDB
try:
    db = MongoClient(config.db_uri)[config.db_name]
except:
    pass


# Create database collections
existing_collections = db.list_collection_names()
for collection_name in DB_COLLECTIONS:
    if collection_name not in existing_collections:
        db.create_collection(collection_name)


# Create default database or run database migrations
migrations = db.config.find_one({"_id": "migrations"}, projection={"_id": 0})
if migrations is None:  # Create default database
    pass
else:
    db_version = migrations.get("db_version", 1)
    match db_version:
        case 0:
            pass  # example database migration
