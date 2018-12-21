class CBWApplication(object):
    def __init__(self,
                 hash_index="",
                 product="",
                 type="",
                 vendor="",
                 version=""):
        self.hash_index = hash_index
        self.product = product
        self.package_type = type
        self.vendor = vendor
        self.version = version
