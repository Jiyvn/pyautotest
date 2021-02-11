import sys
from app import logger


class TestIOSSample:

    def test_print_ios(self, device):
        logger.info(sys._getframe().f_code.co_name)
        logger.info(f"device info: {device}")