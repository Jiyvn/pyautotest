import os
from appium import webdriver

from app.core.drivers.client import Client

try:
    import uiautomation as auto
except:
    pass
try:
    from pywinauto.application import Application
except:
    pass


class Win(Client):

    def __init__(self, devinfo, driver=None):
        super().__init__(devinfo)
        self.driver = driver
        self.winName = self.devinfo.get('')
        self.host = self.devinfo.get('host')
        self.searchProperties = {}

    def app(self, app):
        self.desired_caps['app'] = app
        return self

    def set_caps(self, **kwargs):
        self.desired_caps.update(kwargs)
        return self

    def start(self, host=None, **kwargs):
        url = host or self.host
        self.desired_caps.update(kwargs)
        self.driver = webdriver.Remote(url, self.desired_caps)
        return self.driver


class WinUIAuto(object):

    def __init__(self):
        self.searchProperties = {}
        self.desired_caps = {}
        self.driver = None

    def app(self, app):
        self.desired_caps['app'] = app
        return self

    def set_search_properties(self, **kwargs):
        self.searchProperties.update(kwargs)
        return self

    def start(self, **kwargs):
        timeout = kwargs.get('timeout') or 10
        if kwargs.get('ClassName'):
            self.searchProperties['ClassName'] = kwargs.get('ClassName')
        if kwargs.get('RegexName'):
            self.searchProperties['RegexName'] = kwargs.get('RegexName')
        os.popen(self.desired_caps['app'])
        window = auto.WindowControl(searchDepth=1, **self.searchProperties)
        if not auto.WaitForExist(window, timeout):
            raise Exception('%s launch failed on Windows' % self.desired_caps['app'])
        window.SetActive()
        self.driver = window
        return self.driver


class PyWinAuto(Application):
    pass


class WiniumAuto(object):
    pass
