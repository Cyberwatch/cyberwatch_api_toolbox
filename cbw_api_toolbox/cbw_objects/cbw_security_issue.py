"""Security issues Model"""

from cbw_api_toolbox.cbw_parser import CBWParser
from cbw_api_toolbox.cbw_objects.cbw_server import CBWCve

class CBWSecurityIssue:
    """Security issues Model"""

    def __init__(self,
                 sid="",
                 cve_announcements=None,
                 level="",
                 id="", # pylint: disable=redefined-builtin
                 description="",
                 score="",
                 title="",
                 type="", # pylint: disable=redefined-builtin
                 servers=None,
                 **kwargs): # pylint: disable=unused-argument
        self.id = id # pylint: disable=redefined-builtin, C0103
        self.sid = sid
        self.cve_announcements = [CBWParser().parse(CBWCve, cve) for cve in
                                  cve_announcements] if cve_announcements else []
        self.level = level
        self.description = description
        self.title = title
        self.type = type
        self.score = score
        self.servers = servers
