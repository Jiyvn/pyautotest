import sys
import pytest
from app import logger


class TestChromeSample:

    @pytest.mark.smoke
    def test_print_chrome(self, device):
        logger.info(sys._getframe().f_code.co_name)
        logger.info(f"device info: {device}")