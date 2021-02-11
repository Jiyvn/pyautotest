import time
from datetime import datetime

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from .type import Boolean, Integer, IntFloat, String, Dict, Union


class Proxy:
    def __init__(self, obj):
        self._obj = obj

    def __getattr__(self, name):
        return getattr(self._obj, name)

    def __setattr__(self, name, value):
        if name.startswith('_'):  # protected/private
            super().__setattr__(name, value)
        else:
            setattr(self._obj, name, value)

    def __delattr__(self, name):
        if name.startswith('_'):
            super().__delattr__(name)
        else:
            print('delattr:', name)
            delattr(self._obj, name)


class _Found:

    def __init__(self, found, element):
        self.f = found
        self._element = element

    def __getattr__(self, item):
        if self.f:
            return getattr(self._element, item)
        else:
            # not raise
            return self

    def __call__(self, *args, **kwargs):
        return self.f


class Po(object):

    __attrc__ = False

    def __init__(self, driver):
        self.driver = driver

        self.Item = None
        self.Container = None
        self.Element = None
        self.Locator = None
        self.Timeout = 5
        self.Scroll = False
        self.Direction = None

    def __getattr__(self, item):
        # print('__getattr__  {}   {}'.format(datetime.now(), item))
        if item in self.Container:
            self.__attrc__ = True
            if self.Locator and not self.Item:
                return self
            if self.Item != item:
                self.Item = item
                self.Element = None
                self.Locator = self.Container[item]
            return self
        elif self.__attrc__:
            self.__attrc__ = False
            if self.Scroll and self.scroll_to_find(*self.Locator, direction=self.Direction):
                self.Direction = None
                self.Scroll = False
                self.Element = self.get(*self.Locator)
            if self.Element:
                return getattr(self.Element, item)
            else:
                self.Element = self.get(*self.Locator)
                return getattr(self.Element, item)
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{item}'")

    def __getitem__(self, item):
        self.__attrc__ = True
        self.Item = item
        self.Element = None
        self.Locator = self.Container[item]
        return self

    def __setitem__(self, key, value):
        self.Container[key] = value

    @property
    def found(self):
        return _Found(self.find(*self.Locator), self.Element)

    @property
    def element(self):
        return self.get(*self.Locator)

    def container(self, c):
        self.Container = c
        self.Item = None
        self.Element = None
        self.Locator = None
        return self

    def locator(self, l):
        self.Locator = l
        self.Item = None
        return self

    def timeout(self, t):
        self.Timeout = t
        return self

    def wait(self, t):
        time.sleep(t)
        return self

    def direction(self, d):
        self.Direction = d
        return self

    def get(self, *args, **kwargs):
        raise NotImplementedError("method `get` must be implemented")

    def find(self, *args, **kwargs) -> bool:
        raise NotImplementedError("method `find` must be implemented")

    def scroll_to_find(self, *args, **kwargs):
        raise NotImplementedError("method `find` must be implemented")

    @property
    def scroll_to(self):
        self.Scroll = True
        return self

