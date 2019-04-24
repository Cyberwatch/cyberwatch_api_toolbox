"""CVE Model"""


class CBWCve:
    """CVE Model"""

    def __init__(self,
                 content="",
                 created_at="",
                 cve_code="",
                 cve_score="",
                 last_modified="",
                 published="",
                 updated_at="",
                 **kwargs): # pylint: disable=unused-argument
        self.content = content
        self.created_at = created_at
        self.cve_code = cve_code
        self.cve_score = cve_score
        self.last_modified = last_modified
        self.published = published
        self.updated_at = updated_at
