"""Users Model"""

from cbw_api_toolbox.cbw_parser import CBWParser
from cbw_api_toolbox.cbw_objects.cbw_user_server_groups import CBWUserServerGroups

class CBWUsers:
    """Users Model"""

    def __init__(self,
                 id="",  # pylint: disable=redefined-builtin
                 login="",
                 name="",
                 firstname="",
                 email="",
                 auth_provider="",
                 locale="",
                 server_groups=None,
                 **kwargs): # pylint: disable=unused-argument
        self.id = id  # pylint: disable=invalid-name
        self.login = login
        self.name = name
        self.firstname = firstname
        self.email = email
        self.auth_provider = auth_provider
        self.locale = locale
        self.server_groups = CBWParser().parse(CBWUserServerGroups, server_groups[0]) if server_groups else []
