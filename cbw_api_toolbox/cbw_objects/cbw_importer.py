"""CBWImporter Model"""


class CBWImporter:
    """CBWImporter Model"""

    def __init__(self,
                 id="",  # pylint: disable=redefined-builtin
                 type="", # pylint: disable=redefined-builtin
                 contents="",
                 attachment="",
                 **kwargs):  # pylint: disable=unused-argument
        self.id = id  # pylint: disable=invalid-name
        self.type = type
        self.contents = contents
        self.attachment = attachment
