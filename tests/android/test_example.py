import sys
import pytest
from app import logger


class TestAndroidExample:

    def test_print_android(self, device):
        logger.info(sys._getframe().f_code.co_name)
        logger.info(f"device info: {device}")