""""Model Remote access"""

from cbw_api_toolbox.cbw_parser import CBWParser
from cbw_api_toolbox.cbw_objects.cbw_server import CBWServer
from cbw_api_toolbox.cbw_objects.cbw_node import CBWNode


class CBWRemoteAccess:
    """Model Remote access"""
    def __init__(self,
                 id, # pylint: disable=redefined-builtin
                 type, # pylint: disable=redefined-builtin
                 node,
                 address,
                 port,
                 is_valid,
                 created_at,
                 updated_at,
                 server,
                 server_group,
                 **kwargs): # pylint: disable=unused-argument
        self.id = id  # pylint: disable=invalid-name
        self.type = type
        self.node = CBWParser().parse(CBWNode, node) if node else None
        self.address = address
        self.port = port
        self.is_valid = is_valid
        self.created_at = created_at
        self.updated_at = updated_at
        self.server = CBWParser().parse(CBWServer, server) if server else None
        self.server_group = server_group
