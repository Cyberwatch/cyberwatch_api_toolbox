import logging
from json import JSONDecodeError


class CBWParser(object):
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def parse(self, parsed_class, class_dict):
        try:
            self.logger.debug("Parsing {0} ...".format(class_dict))
            return parsed_class(**class_dict)
        except JSONDecodeError as e:
            self.logger.error("An error occurred when parsing {0} with {1} : {2}".format(parsed_class, class_dict, e))
        except TypeError as e:
            self.logger.error("An error occurred when parsing {0} with {1} : {2}".format(parsed_class, class_dict, e))
