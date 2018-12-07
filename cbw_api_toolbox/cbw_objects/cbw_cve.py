class CBWCve(object):
    def __init__(self,
                 content: str = "",
                 created_at: str = "",
                 cve_code: str = "",
                 cve_score: str = "",
                 last_modified: str = "",
                 published: str = "",
                 updated_at: str = ""):
        self.content = content
        self.created_at = created_at
        self.cve_code = cve_code
        self.cve_score = cve_score
        self.last_modified = last_modified
        self.published = published
        self.updated_at = updated_at
