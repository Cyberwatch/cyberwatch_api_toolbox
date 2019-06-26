""""Model Server"""

from cbw_api_toolbox.cbw_objects.cbw_cve import CBWCve
from cbw_api_toolbox.cbw_objects.cbw_group import CBWGroup
from cbw_api_toolbox.cbw_objects.cbw_package import CBWPackage
from cbw_api_toolbox.cbw_objects.cbw_deploying_period import CBWDeployingPeriod
from cbw_api_toolbox.cbw_objects.cbw_ignoring_policy import CBWIgnoringPolicy
from cbw_api_toolbox.cbw_parser import CBWParser


class CBWServer:
    """Model Server"""

    def __init__(self,
                 id,  # pylint: disable=redefined-builtin
                 agent_version="",
                 applications=None,
                 boot_at="",
                 category="",
                 created_at="",
                 criticality="",
                 cve_announcements=None,
                 cve_announcements_count=0,
                 deploying_period=None,
                 description="",
                 groups=None,
                 hostname="",
                 ignoring_policy=None,
                 last_communication="",
                 os=None,
                 packages=None,
                 reboot_required=False,
                 remote_ip="",
                 security_announcements=None,
                 status=None,
                 updates=None,
                 updates_count=0,
                 **kwargs): # pylint: disable=unused-argument
        self.id = id  # pylint: disable=invalid-name
        self.agent_version = agent_version
        self.applications = [CBWParser().parse(CBWPackage, application) for application in
                             applications] if applications else None
        self.boot_at = boot_at
        self.category = category
        self.created_at = created_at
        self.criticality = criticality
        self.cve_announcements = [CBWParser().parse(CBWCve, cve) for cve in
                                  cve_announcements] if cve_announcements else None
        self.cve_announcements_count = cve_announcements_count
        self.deploying_period = (CBWParser().parse(CBWDeployingPeriod, deploying_period) if
                                 deploying_period else None)
        self.description = description
        self.groups = [CBWParser().parse(CBWGroup, group) for group in groups] if groups else None
        self.hostname = hostname
        self.ignoring_policy = (CBWParser().parse(CBWIgnoringPolicy, ignoring_policy) if
                                ignoring_policy else None)
        self.last_communication = last_communication
        self.os = os  # pylint: disable=invalid-name
        self.packages = [CBWParser().parse(CBWPackage, package) for package in
                         packages] if packages else None
        self.reboot_required = reboot_required
        self.remote_ip = remote_ip
        self.security_announcements = security_announcements
        self.status = status
        self.updates = updates
        self.updates_count = updates_count
