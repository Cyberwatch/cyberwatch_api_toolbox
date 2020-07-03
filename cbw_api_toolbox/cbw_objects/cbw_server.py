"""CVE Model & Server Model"""

from cbw_api_toolbox.cbw_objects.cbw_deploying_period import CBWDeployingPeriod
from cbw_api_toolbox.cbw_objects.cbw_group import CBWGroup
from cbw_api_toolbox.cbw_objects.cbw_ignoring_policy import CBWIgnoringPolicy
from cbw_api_toolbox.cbw_objects.cbw_package import CBWPackage
from cbw_api_toolbox.cbw_parser import CBWParser


class CBWCve:
    """CVE Model"""

    def __init__(self,
                 content="",
                 created_at="",
                 cve_code="",
                 cvss="",
                 cvss_v3="",
                 cvss_custom="",
                 level="",
                 score="",
                 score_v2="",
                 score_v3="",
                 score_custom="",
                 last_modified="",
                 published="",
                 updated_at="",
                 exploit_code_maturity="",
                 servers=None,
                 **kwargs): # pylint: disable=unused-argument
        self.content = content
        self.created_at = created_at
        self.cve_code = cve_code
        self.cvss_v2 = cvss
        self.cvss_v3 = cvss_v3
        self.cvss_custom = cvss_custom
        self.score = score
        self.score_v2 = score_v2
        self.score_v3 = score_v3
        self.score_custom = score_custom
        self.level = level
        self.last_modified = last_modified
        self.published = published
        self.updated_at = updated_at
        self.exploit_code_maturity = exploit_code_maturity
        self.servers = [{"server": CBWParser().parse(CBWServer, server),
                         "active": server["active"], "ignored": server["ignored"],
                         "comment": server["comment"], "fixed_at": server["fixed_at"]}
                        for server in servers] if servers else []

class CBWServer:
    """Model Server"""

    def __init__(self,
                 id,  # pylint: disable=redefined-builtin
                 applications=None,
                 boot_at="",
                 category="",
                 compliance_groups=None,
                 created_at="",
                 environment=None,
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
        self.applications = [CBWParser().parse(CBWPackage, application) for application in
                             applications] if applications else []
        self.boot_at = boot_at
        self.category = category
        self.compliance_groups = [CBWParser().parse(CBWGroup, group) for group in
                                  compliance_groups] if compliance_groups else []
        self.created_at = created_at
        self.environment = environment
        self.cve_announcements = cve_announcements
        self.cve_announcements_count = cve_announcements_count
        self.deploying_period = (CBWParser().parse(CBWDeployingPeriod, deploying_period) if
                                 deploying_period else None)
        self.description = description
        self.groups = [CBWParser().parse(CBWGroup, group) for group in groups] if groups else []
        self.hostname = hostname
        self.ignoring_policy = (CBWParser().parse(CBWIgnoringPolicy, ignoring_policy) if
                                ignoring_policy else None)
        self.last_communication = last_communication
        self.os = os  # pylint: disable=invalid-name
        self.packages = [CBWParser().parse(CBWPackage, package) for package in
                         packages] if packages else []
        self.reboot_required = reboot_required
        self.remote_ip = remote_ip
        self.security_announcements = security_announcements
        self.status = status
        self.updates = updates
        self.updates_count = updates_count
