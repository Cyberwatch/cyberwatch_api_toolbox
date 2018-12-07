import logging
from json import JSONDecodeError
from typing import Dict


class CBWParser(object):
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def parse(self, parsed_class, class_dict: Dict[str, str]):
        try:
            self.logger.debug(f"Parsing {class_dict} ...")
            return parsed_class(**class_dict)
        except JSONDecodeError as e:
            self.logger.error(f"An error occurred when parsing {parsed_class} with {class_dict} : {e}")
        except TypeError as e:
            self.logger.error(f"An error occurred when parsing {parsed_class} with {class_dict} : {e}")
