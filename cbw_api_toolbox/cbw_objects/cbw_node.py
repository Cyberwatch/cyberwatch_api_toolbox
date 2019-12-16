"""Node Model"""


class CBWNode:
    """Node Model"""

    def __init__(self,
                 id="",  # pylint: disable=redefined-builtin
                 name="",
                 updated_at="",
                 created_at="",
                 **kwargs):  # pylint: disable=unused-argument
        self.id = id  # pylint: disable=invalid-name
        self.name = name
        self.created_at = created_at
        self.updated_at = updated_at
