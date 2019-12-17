"""Host Model"""

from cbw_api_toolbox.cbw_objects.cbw_package import CBWPackage
from cbw_api_toolbox.cbw_objects.cbw_server import CBWCve
from cbw_api_toolbox.cbw_parser import CBWParser

class CBWHost:
    """Host Model"""

    def __init__(self,
                 id,  # pylint: disable=redefined-builtin
                 target="",
                 hostname="",
                 category="",
                 created_at="",
                 updated_at="",
                 cve_announcements_count="",
                 node_id="",
                 server_id="",
                 status="",
                 technologies=None,
                 security_issues=None,
                 cve_announcements=None,
                 scans=None,
                 **kwargs): # pylint: disable=unused-argument
        self.id = id # pylint: disable=invalid-name
        self.target = target
        self.hostname = hostname
        self.category = category
        self.created_at = created_at
        self.updated_at = updated_at
        self.cve_announcements_count = cve_announcements_count
        self.node_id = node_id
        self.server_id = server_id
        self.status = status
        self.technologies = [CBWParser().parse(CBWPackage, technology) for technology in
                             technologies] if technologies else []
        self.security_issues = security_issues
        self.cve_announcements = [CBWParser().parse(CBWCve, cve) for cve in
                                  cve_announcements] if cve_announcements else []
        self.scans = scans
