"""Group Model"""


class CBWGroup:
    """Group Model"""

    def __init__(self,
                 id="",  # pylint: disable=redefined-builtin
                 color="",
                 name="",
                 description="",
                 **kwargs): # pylint: disable=unused-argument
        self.id = id  # pylint: disable=invalid-name
        self.color = color
        self.name = name
        self.description = description
