""""Model ignoring policy"""

from cbw_api_toolbox.cbw_parser import CBWParser
from cbw_api_toolbox.cbw_objects.cbw_ignoring_policy_items import CBWIgnoringPolicyItems


class CBWIgnoringPolicy:
    """Model ignoring policy"""

    def __init__(self,
                 ignoring_policy_items=None,
                 name="",
                 **kwargs): # pylint: disable=unused-argument
        self.ignoring_policy_items = ([CBWParser().parse(CBWIgnoringPolicyItems,
                                                         ignoring_policy_item) for
                                       ignoring_policy_item in ignoring_policy_items] if
                                      ignoring_policy_items else [])
        self.name = name
