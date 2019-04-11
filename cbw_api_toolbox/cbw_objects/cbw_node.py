"""Node Model"""


class CBWNode:
    """Node Model"""

    def __init__(self,
                 id="",  # pylint: disable=redefined-builtin
                 name="",
                 description="",
                 url="",
                 olympe_version="",
                 cbw_on_premise_version="",
                 boot_time="",
                 created_at="",
                 updated_at=""):
        self.id = id  # pylint: disable=invalid-name
        self.name = name
        self.description = description
        self.url = url
        self.olympe_version = olympe_version
        self.cbw_on_premise_version = cbw_on_premise_version
        self.boot_time = boot_time
        self.created_at = created_at
        self.updated_at = updated_at
