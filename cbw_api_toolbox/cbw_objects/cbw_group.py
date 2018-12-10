class CBWGroup(object):
    def __init__(self,
                 id: str = "",
                 name: str = "",
                 created_at: str = "",
                 updated_at: str = ""):
        self.group_id = id
        self.name = name
        self.created_at = created_at
        self.updated_at = updated_at
