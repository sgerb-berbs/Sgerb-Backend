from sanic.exceptions import SanicException

class BadRequest(SanicException):
    http = 400

class Conflict(SanicException):
    http = 409

class UsernameExists(Conflict):
    code = 1
    message = "Username already exists"

class UsernameInappropriate(BadRequest):
    code = 2
    message = "Username is inappropriate"
