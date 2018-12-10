from typing import Dict, List

from cbw_api_toolbox.cbw_objects.cbw_application import CBWApplication
from cbw_api_toolbox.cbw_objects.cbw_cve import CBWCve
from cbw_api_toolbox.cbw_objects.cbw_group import CBWGroup
from cbw_api_toolbox.cbw_objects.cbw_package import CBWPackage
from cbw_api_toolbox.cbw_parser import CBWParser


class CBWServer(object):
    def __init__(self,
                 id: str = "",
                 hostname: str = "",
                 boot_at: str = "",
                 remote_ip: str = "",
                 criticality: str = "",
                 category: str = "",
                 status: Dict[str, str] = None,
                 os: Dict[str, str] = None,
                 updates_count: int = 0,
                 groups: List[Dict[str, str]] = None,
                 cve_announcements_count: int = 0,
                 cve_announcements: List[Dict[str, str]] = None,
                 security_announcements: List[Dict[str, str]] = None,
                 packages: List[Dict[str, str]] = None,
                 applications: List[Dict[str, str]] = None,
                 agent_version: str = "",
                 reboot_required: bool = False,
                 last_communication: str = "",
                 state_sha2: str = ""):
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
        self.cve_announcements = [CBWParser().parse(CBWCve, cve) for cve in cve_announcements] if cve_announcements else None
        self.security_announcements = security_announcements
        self.packages = [CBWParser().parse(CBWPackage, package) for package in packages] if packages else None
        self.applications = [CBWParser().parse(CBWApplication, application) for application in applications] if applications else None
        self.agent_version = agent_version
        self.reboot_required = reboot_required
        self.last_communication = last_communication
