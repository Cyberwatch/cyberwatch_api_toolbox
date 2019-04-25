""""Model deploying period"""


class CBWDeployingPeriod:
    """Model deploying period"""

    def __init__(self,
                 autoplanning=False,
                 autoreboot=False,
                 end_time="",
                 name="",
                 next_occurrence="",
                 start_time="",
                 **kwargs): # pylint: disable=unused-argument
        self.autoplanning = autoplanning
        self.autoreboot = autoreboot
        self.end_time = end_time
        self.name = name
        self.next_occurrence = next_occurrence
        self.start_time = start_time
