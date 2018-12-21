from cbw_api_toolbox.cbw_objects.cbw_application import CBWApplication
from cbw_api_toolbox.cbw_objects.cbw_cve import CBWCve
from cbw_api_toolbox.cbw_objects.cbw_group import CBWGroup
from cbw_api_toolbox.cbw_objects.cbw_package import CBWPackage
from cbw_api_toolbox.cbw_parser import CBWParser


class CBWServer(object):
    def __init__(self,
                 id,
                 hostname="",
                 boot_at="",
                 remote_ip="",
                 criticality="",
                 category="",
                 status=None,
                 os=None,
                 updates_count=0,
                 groups=None,
                 cve_announcements_count=0,
                 cve_announcements=None,
                 security_announcements=None,
                 packages=None,
                 applications=None,
                 agent_version="",
                 reboot_required=False,
                 last_communication="",
                 state_sha2=""):
        self.server_id = id
        self.groups = [CBWParser().parse(CBWGroup, group) for group in groups] if groups else None
        self.hostname = hostname
        self.boot_at = boot_at
        self.remote_ip = remote_ip
        self.criticality = criticality
        self.category = category
        self.status = status
        self.os = os
        self.state_sha2 = state_sha2
        self.updates_count = updates_count
        self.cve_announcements_count = cve_announcements_count
        self.cve_announcements = [CBWParser().parse(CBWCve, cve) for cve in
                                  cve_announcements] if cve_announcements else None
        self.security_announcements = security_announcements
        self.packages = [CBWParser().parse(CBWPackage, package) for package in packages] if packages else None
        self.applications = [CBWParser().parse(CBWApplication, application) for application in
                             applications] if applications else None
        self.agent_version = agent_version
        self.reboot_required = reboot_required
        self.last_communication = last_communication
