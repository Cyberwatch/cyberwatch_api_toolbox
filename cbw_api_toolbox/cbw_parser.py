"""CbwParser Module"""

import logging
import json
from json import JSONDecodeError


class CBWParser:
    """CBWParser class"""

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def parse_response(self, parsed_class, response):
        """Parse the response text of an API request"""
        try:
            result = []
            parsed_response = json.loads(response.text)

            if isinstance(parsed_response, list):
                for class_dict in parsed_response:
                    result.append(self.parse(parsed_class, class_dict))
            else:
                result = self.parse(parsed_class, parsed_response)

            return result

        except JSONDecodeError:
            self.logger.exception("An error occurred when decoding {0}".format(response.text))

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
