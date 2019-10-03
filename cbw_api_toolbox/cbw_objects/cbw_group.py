"""Group Model"""


class CBWGroup:
    """Group Model"""

    def __init__(self,
                 id="",  # pylint: disable=redefined-builtin
                 name="",
                 description="",
                 created_at="",
                 updated_at="",
                 **kwargs): # pylint: disable=unused-argument
        self.id = id  # pylint: disable=invalid-name
        self.name = name
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at
