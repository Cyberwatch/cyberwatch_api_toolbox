"""Group Model"""


class CBWGroup:
    """Group Model"""

    def __init__(self,
                 id="",  # pylint: disable=redefined-builtin
                 name="",
                 created_at="",
                 updated_at=""):
        self.group_id = id
        self.name = name
        self.created_at = created_at
        self.updated_at = updated_at
