"""CbwParser Module"""

import logging
from json import JSONDecodeError


class CBWParser:
    """CBWParser class"""

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def parse(self, parsed_class, class_dict):
        """Parse the API Json into class_dict"""
        try:
            self.logger.debug("Parsing {0} ...".format(class_dict))
            return parsed_class(**class_dict)

        except JSONDecodeError:
            self.logger.exception("An error occurred when parsing {0} with {1}".
                                  format(parsed_class, class_dict))

        except TypeError:
            self.logger.exception("An error occurred when parsing {0} with {1}".
                                  format(parsed_class, class_dict))
