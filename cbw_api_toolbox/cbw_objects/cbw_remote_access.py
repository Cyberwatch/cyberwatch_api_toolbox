""""Model Remote access"""

class CBWRemoteAccess:
    """Model Remote access"""
    def __init__(self,
                 id="", # pylint: disable=redefined-builtin
                 type="", # pylint: disable=redefined-builtin
                 node_id="",
                 address="",
                 port="",
                 is_valid="",
                 last_error="",
                 server_id="",
                 server_groups="",
                 **kwargs): # pylint: disable=unused-argument
        self.id = id  # pylint: disable=invalid-name
        self.type = type
        self.node_id = node_id
        self.address = address
        self.port = port
        self.is_valid = is_valid
        self.last_error = last_error
        self.server_id = server_id
