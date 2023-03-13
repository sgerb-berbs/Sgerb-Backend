class Session:
    def __init__(
        self,
        _id: str,
        user_id: str,
        user_agent: str,
        created: int
    ):
        self.id = _id
        self.user = ""
        self.user_agent = user_agent
        self.created = created
