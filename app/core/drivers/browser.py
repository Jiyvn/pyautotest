#!/usr/bin/env python3
# encoding: utf-8


import os
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from app import logger
from app.core.drivers import REMOTE
from app.core.drivers.client import Client


class Browser(Client):
    def __init__(self, param=None, driver=None):
        super().__init__(param)
        self.driver = driver
        self.param = param or self.param
        self.browser = self.param['browserName']
        self.platform = self.param['platform']
        self.host = self.param.get('host')
        self.Options = None
        self.desired_caps.update(self.param['caps'])
        self.desired_caps.update({
            'browserName': self.browser,
            'platform': self.platform
        })
        self.cond = ec.visibility_of_element_located

    @property
    def options(self):
        self.Options = self.Options or REMOTE.BROWSER_OPTIONS[self.browser]
        return self.Options

    @property
    def headless(self):
        self.Options.headless = True
        return self

    def set_caps(self, **kwargs):
        self.desired_caps.update(kwargs)
        return self

    def maximize_window(self):
        self.driver.maximize_window()
        return self

    def start(self, url=None, executable_path=None, maximize=True, host=None, **kwargs):
        driverkwargs = {} if not self.Options else {"options": self.Options}
        # host为Selenium Grid的hub管理服务地址
        if host or self.host:
            driverkwargs['command_executor'] = host or str(self.host)
            driverkwargs['desired_capabilities'] = self.desired_caps
            driverkwargs.update(kwargs)
            self.driver = webdriver.Remote(**driverkwargs)
        else:
            if self.platform != REMOTE.PLATFORM_OS:
                raise OSError('"{0}" does not match target platform: {1}'.format(
                    REMOTE.PLATFORM_OS, self.platform))
            if not executable_path:
                if os.path.isfile(REMOTE.WEBDRIVER_BIN[self.browser]):
                    driverkwargs['executable_path'] = REMOTE.WEBDRIVER_BIN[self.browser]
            else:
                driverkwargs['executable_path'] = executable_path
            driverkwargs.update(kwargs)
            self.driver = REMOTE.WEBDRIVERS[self.browser](**driverkwargs)
            if maximize is True:
                self.driver.maximize_window()
            if url:
                self.driver.get(url)
        return self.driver

    def input(self, text: str, element, timeout: int = 5):
        """
        向网页上的元素输入文字
        :param text: 要输入的文字
        :param element: 要滚动到的web element, 或者element locator
        :param timeout: 查找元素的超时时间
        :return:
        """
        try:
            if isinstance(element, tuple):
                element = self.get(*element, timeout=timeout)
            else:
                element = element

            WebDriverWait(self.driver, 30, 0.5).until(ec.element_to_be_clickable(element))
            # 为了避免反爬虫机制, 输入时稍微等待一点时间
            if text not in (Keys.ENTER, Keys.TAB):
                element.clear()
            time.sleep(0.5)
            element.send_keys(text)
        except TimeoutException:
            raise Exception("Element not found: " + element)

    def move_to_click(self, element_or_locator, timeout: int = 3):
        """
        模拟鼠标移动去点击一个元素, 由于反爬虫机制的原因, 直接移动到元素上点击会失败或者被block, 所以先移动到元素附近, 再移动到元素上进行点击
        :param element_or_locator: 需要点击元素的web element实例或者它的locator, 注意传入locator的话不用解包
        :param timeout:  等待被点击元素出现的时间
        :return:
        """
        if isinstance(element_or_locator, tuple):
            element = self.get(*element_or_locator, timeout=timeout)
        else:
            element = element_or_locator
        ActionChains(self.driver).move_to_element(element).perform()
        time.sleep(0.5)
        ActionChains(self.driver).click(element).perform()

    def scroll_down_by_pixel(self, pixel: int):
        """页面滚动多少像素

        :param pixel: 负值为向上滚动，正值为向下滚动
        :return:
        """
        js = '"window.scrollBy(0,{0})"'.format(pixel)
        self.driver.execute_script(js)

    def scroll_to_element(self, element_or_locator, pixel: int = None, approach: str = None, timeout: int = 5):
        """
        由于chrome driver在计算页面高度时常常会将整个页面计算在内而不是只计算活动部分(比如页面有不会随着的Header), 所以直接使用
        location_once_scrolled_into_view会导致元素被档着, 所以这里设计一个专门的方法以避免这种情况
        :param element_or_locator: 要滚动到的web element, 或者element locator
        :param pixel: 额外滚动的像素, 如果为None就默认会向上滚动多半个屏幕的距离
        :param approach: 判断元素存在的方式
        :param timeout: 等待时间
        :return: 无
        """
        if isinstance(element_or_locator, tuple):
            element_into_view = self.get(*element_or_locator, condition=approach,
                                         timeout=timeout).location_once_scrolled_into_view
        else:
            element_into_view = element_or_locator.location_once_scrolled_into_view
        logger.debug(element_into_view)
        time.sleep(1)
        if pixel is None:
            pixel = 0 - (self.driver.get_window_size()['height'] / 2)

        js = 'window.scrollBy(0,{0})'.format(pixel)
        self.driver.execute_script(js)

    def add_attribute(self, element_or_locator, attribute_name: str, value: str, approach: str = None,
                      timeout: int = 5):
        """
        封装向页面标签添加新属性的方法, 同时也可以用于设置页面对象的属性值
        添加新属性的JS代码语法为：element.attributeName=value, 比如input.name='test'
        使用Selenium调用JS给页面标签添加新属性，arguments[0]~arguments[2]分别会用后面的element，attributeName和value参数进行替换
        :param element_or_locator: 要操作的web element, 或者element locator
        :param attribute_name: 要添加 / 设置的属性名称, 比如style
        :param value: 要添加 / 设置的属性值, 比如"display: block;"
        :param approach: 判断元素存在的方式
        :param timeout: 等待时间
        :return: 无
        """
        if isinstance(element_or_locator, tuple):
            element = self.get(*element_or_locator, condition=approach, timeout=timeout)
        else:
            element = element_or_locator

        self.driver.execute_script("arguments[0].%s=arguments[1]" % attribute_name, element, value)

    def set_attribute(self, element_or_locator, attribute_name: str, value: str, approach: str = None,
                      timeout: int = 5):
        """
        封装设置页面对象的属性值的方法
        使用Selenium调用JS代码修改页面元素的属性值，arguments[0]~arguments[1]分别会用后面的element，attributeName和value参数进行替换
        :param element_or_locator: 要操作的web element, 或者element locator
        :param attribute_name: 要添加 / 设置的属性名称, 比如style
        :param value: 要添加 / 设置的属性值, 比如"display: block;"
        :param approach: 判断元素存在的方式
        :param timeout: 等待时间
        :return: 无
        """
        if isinstance(element_or_locator, tuple):
            element = self.get(*element_or_locator, condition=approach, timeout=timeout)
        else:
            element = element_or_locator

        self.driver.execute_script("arguments[0].setAttribute(arguments[1],arguments[2])", element, attribute_name,
                                   value)

    def get_attribute(self, element_or_locator, attribute_name: str, approach: str = None, timeout: int = 5):
        """
        封装获取页面对象的属性值方法
        :param element_or_locator: 要查询web element, 或者element locator
        :param attribute_name: 要查询的属性名称, 比如style
        :param approach: 判断元素存在的方式
        :param timeout: 等待时间
        :return: 指定的属性值, 比如"display: block;"
        """

        if isinstance(element_or_locator, tuple):
            element = self.get(*element_or_locator, condition=approach, timeout=timeout)
        else:
            element = element_or_locator

        return element.get_attribute(attribute_name)

    def remove_attribute(self, element_or_locator, attribute_name: str, approach: str = None, timeout: int = 5):
        """
        封装删除页面属性的方法
        使用Selenium调用JS代码删除页面元素的指定的属性，arguments[0]~arguments[1]分别会用后面的element，attributeName参数进行替换
        :param element_or_locator: 要操作的web element, 或者element locator
        :param attribute_name: 要添加 / 设置的属性名称, 比如style
        :param approach: 判断元素存在的方式
        :param timeout: 等待时间
        :return:
        """
        if isinstance(element_or_locator, tuple):
            element = self.get(*element_or_locator, condition=approach, timeout=timeout)
        else:
            element = element_or_locator

        self.driver.execute_script("arguments[0].removeAttribute(arguments[1])", element, attribute_name)

    def close(self):
        self.driver.quit()
