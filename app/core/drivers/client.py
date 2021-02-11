#!/usr/bin/env python3
# encoding: utf-8

import os

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from app.appbase import appActivity, appPackage, appBundleId
from . import REMOTE
from ..po import Po


class Client(Po):

    def __init__(self, devinfo=None):
        self.driver = None
        self.devinfo = devinfo
        self.desired_caps = self.devinfo.get('caps')
        super().__init__(self.driver)

    def alert(self):
        """
        查找是否出现弹窗
        :return:
        """
        try:
            WebDriverWait(self.driver, 3).until(ec.alert_is_present())
            flag = True
        except TimeoutException:
            flag = False
        return flag

    def start_up(self, **kwargs):
        """
        通过appium启动APP/ 通过selenium启动浏览器
        :return: driver
        """
        try:
            if kwargs.get('url'):
                from selenium import webdriver
                options = None
                browser = self.devinfo['deviceName'].lower()
                if browser in REMOTE.BROWSERS:
                    if not kwargs.get('host') and not self.devinfo['host']:
                        if (browser in ("edge", "ie") and not REMOTE.PLATFORM.startswith('window')) or \
                                (browser in ["safari"] and not REMOTE.PLATFORM.startswith('darwin')):
                            raise OSError(
                                "{0} is not supported on {1}".format(self.devinfo['deviceName'],
                                                                     self.devinfo['devicePlatform']))
                    if kwargs.get('headless') is True:
                        options = REMOTE.BROWSER_OPTIONS[browser]
                        options.add_argument('--headless')
                    driverkwargs = {} if browser in ["edge", "safari"] else {"options": options}
                    # host为Selenium Grid的hub管理服务地址
                    if kwargs.get('host') or self.devinfo['host']:
                        driverkwargs['command_executor'] = kwargs.get('host') or str(self.devinfo['host'])
                        driverkwargs['desired_capabilities'] = {
                            'browserName': self.devinfo['browserName'].lower(),
                            'platform': self.devinfo['browserName'].lower()
                        }
                        self.driver = webdriver.Remote(**driverkwargs)
                    else:
                        if self.devinfo['devicePlatform'].lower() != REMOTE.PLATFORM_OS:
                            raise OSError('"{0}" does not match target platform: {1}'.format(
                                REMOTE.PLATFORM_OS, self.devinfo['devicePlatform']))
                        driverkwargs['executable_path'] = REMOTE.WEBDRIVER_BIN[browser] \
                            if os.path.isfile(REMOTE.WEBDRIVER_BIN[browser]) else REMOTE.DEFAULT_DRIVER[browser]
                        self.driver = REMOTE.WEBDRIVERS[browser](**driverkwargs)

                else:
                    raise OSError("{0} is not supported currently.".format(self.devinfo['deviceName']))

                if kwargs.get('maximize') is True:
                    self.driver.maximize_window()
                self.driver.get(kwargs.get('url'))

            else:
                from appium import webdriver
                if self.devinfo['devicePlatform'].lower() == 'android':
                    self.desired_caps['platformName'] = 'Android'
                    self.desired_caps['platformVersion'] = self.devinfo['platformVersion']
                    self.desired_caps['deviceName'] = self.devinfo['deviceName']
                    self.desired_caps['udid'] = self.devinfo['udid']
                    self.desired_caps["newCommandTimeout"] = 3600
                    self.desired_caps["recreateChromeDriverSessions"] = True

                    if kwargs.get('launch_browser') is True:
                        self.desired_caps['browserName'] = 'Chrome'
                    else:
                        self.desired_caps['appPackage'] = appPackage[kwargs.get('app')]
                        self.desired_caps['appActivity'] = appActivity[kwargs.get('app')]
                        self.desired_caps["autoGrantPermissions"] = True
                    if kwargs.get('uiautomator') is True:
                        self.desired_caps['automationName'] = 'uiautomator'
                    else:
                        self.desired_caps['automationName'] = 'uiautomator2'
                        # self.desired_caps['systemPort'] = self.param['system_port']
                    if kwargs.get('no_reset') is True:
                        self.desired_caps['noReset'] = True
                    if kwargs.get('unicode_keyboard') is True:  # 用于解决无法输入中文的问题
                        self.desired_caps["unicodeKeyboard"] = True
                        self.desired_caps["resetKeyboard"] = True

                elif self.devinfo['devicePlatform'].lower() == 'ios':
                    self.desired_caps['automationName'] = 'XCUITest'
                    self.desired_caps['platformName'] = 'iOS'
                    self.desired_caps['platformVersion'] = self.devinfo['platformVersion']
                    self.desired_caps['deviceName'] = self.devinfo['deviceName']
                    self.desired_caps['udid'] = self.devinfo['udid']
                    if kwargs.get('launch_browser') is True:
                        self.desired_caps['browserName'] = 'safari'
                    else:
                        self.desired_caps['bundleId'] = appBundleId[kwargs.get('app')]
                    self.desired_caps['startIWDP'] = True
                    self.desired_caps["launchTimeout"] = 60000
                    self.desired_caps["newCommandTimeout"] = 3600
                    self.desired_caps['webviewConnectTimeout'] = 90000
                if kwargs.get('host') or self.devinfo['host']:
                    self.driver = webdriver.Remote(self.devinfo['host'], self.desired_caps)
                else:
                    self.desired_caps['wdaLocalPort'] = self.devinfo['bp']
                    self.driver = webdriver.Remote("http://127.0.0.1:{}".format(self.devinfo['p']) + "/wd/hub", self.desired_caps)
            return self.driver
        except Exception as msg:
            raise ConnectionError(msg)

    def get(self, by, locator, condition=None, timeout=None, frequency=0.5):
        try:
            self.Element = WebDriverWait(self.driver, timeout or self.TIMEOUT, frequency).until(
                self._m2l_[condition or self.cond]((by, locator)))
            return self.Element
        except TimeoutException:
            raise Exception("Element not found: {}, {}".format(by, locator))

    def find(self, by, locator, condition=None, timeout=None, frequency=0.5):
        try:
            self.Element = WebDriverWait(self.driver, timeout or self.TIMEOUT, frequency).until(
                condition or self._m2l_[self.cond]((by, locator)))
            flag = True
        except TimeoutException:
            flag = False
        return flag

    def wait_until_not(self, by, locator, condition=None, timeout=None, frequency=0.5):
        try:
            WebDriverWait(self.driver, timeout or self.TIMEOUT, frequency).until_not(
                self._m2l_[condition or self.cond]((by, locator)))
            flag = True
        except TimeoutException:
            flag = False
        return flag

    def has_text(self, by: str, locator: str, approach: str = None, timeout: float = 3, txt: str = None):
        """
        判断文本是否出现在元素中
        """
        try:
            if approach == 'text':
                WebDriverWait(self.driver, timeout, 0.5).until(ec.text_to_be_present_in_element(
                    (by, locator), txt))
            else:
                WebDriverWait(self.driver, timeout, 0.5).until(ec.text_to_be_present_in_element_value(
                    (by, locator), txt))
            flag = True
        except TimeoutException:
            flag = False
        return flag

    def clickable(self, by: str, locator: str, timeout: float = 3):
        """判断元素是否可以点击
        """
        try:
            WebDriverWait(self.driver, timeout, 0.5).until(ec.element_to_be_clickable(
                (by, locator)))
            flag = True
        except TimeoutException:
            flag = False
        return flag

    def close(self):
        self.driver.quit()
