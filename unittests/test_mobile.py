import time
import unittest

from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy

from app.appbase import settings
from app.core.drivers.mobile import Mobile


class MobileTest(unittest.TestCase):
    driver = None

    @classmethod
    def setUpClass(cls):
        android_set = {
            'LG_G6': {
                'deviceName': 'LG_G6',
                'devicePlatform': 'Android',
                'platformVersion': '7.0',
                'udid': 'VS988b3876fa0',
                'appPackage': None,
                'appActivity': None,

            }
        }
        ios_set = {
            'iphone7': {
                'automationName': 'XCUITest',
                'platformName': 'iOS',
                'platformVersion': '13.1.3',
                'deviceName': 'iphone7',
                'udid': '7524ead2a9a14eab947b648258ba4e02c5c12604',
                'bundleId': 'com.apple.Preferences',
                # 'startIWDP': True,
                'launchTimeout': 60000,
                'newCommandTimeout': 3600,
            }
        }
        cls.param = {
            'p': '4723',
            'bp': '4724',
            'system_port': '8100'
        }

        cls.desired_caps = ios_set['iphone7']

        cls.driver = webdriver.Remote("http://127.0.0.1:" + cls.param['p'] + "/wd/hub", cls.desired_caps)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_bluetooth(self):

        settings = {
            'bluetooth': (MobileBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeCell[`label == "蓝牙"`]'),
        }
        bt = {
            'back_button': (MobileBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`label == "设置"`]'),
            'bluetooth_switch': (MobileBy.IOS_PREDICATE, 'type == "XCUIElementTypeSwitch" AND label == "蓝牙"'),
        }
        page = Mobile(self.driver)
        page.container(settings)
        print(page.bluetooth.text)
        # assert page.bluetooth.text == '打开'
        page.bluetooth.click()
        page.wait(1).container(bt)
        assert page.bluetooth_switch.found() is True
        page.bluetooth_switch.click()
        page.back_button.click()

        page.wait(1).container(settings)
        page.timeout(3)
        page['bluetooth'].click()
        page.wait(1).container(bt)
        page['bluetooth_switch'].found.click()


if __name__ == '__main__':
    unittest.main()
