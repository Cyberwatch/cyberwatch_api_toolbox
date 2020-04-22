""""Model Agent"""

class CBWAgent:
    """Model Agent"""
    def __init__(self,
                 id="", # pylint: disable=redefined-builtin
                 server_id="", # pylint: disable=redefined-builtin
                 node_id="",
                 version="",
                 remote_ip="",
                 last_communication="",
                 **kwargs): # pylint: disable=unused-argument
        self.id = id  # pylint: disable=invalid-name
        self.server_id = server_id
        self.node_id = node_id
        self.version = version
        self.remote_ip = remote_ip
        self.last_communication = last_communication
