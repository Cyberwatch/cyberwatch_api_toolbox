"""User Server Groups Model"""

class CBWUserServerGroups:
    """User Server Groups Model"""

    def __init__(self,
                 id="",  # pylint: disable=redefined-builtin
                 name="",
                 role="",
                 **kwargs): # pylint: disable=unused-argument
        self.id = id  # pylint: disable=invalid-name
        self.name = name
        self.role = role
