from bson.objectid import ObjectId

def oid() -> str:
    return str(ObjectId())
