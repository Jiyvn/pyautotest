#!/usr/bin/env python3
# encoding: utf-8

import time

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import TimeoutException, WebDriverException, InvalidSessionIdException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from app.core.drivers.client import Client
from . import locate_method


class Mobile(Client):

    def __init__(self, driver=None, devinfo=None, remote=False):
        super().__init__(devinfo)
        if driver:
            self.driver = driver
        self.remote = remote
        self.locate_method = locate_method
        self.tofind = {
            'up': self.scroll_up,
            'down': self.scroll_down,
            'left': self.swipe_left,
            'right': self.swipe_right,
        }
        self.udid = self.devinfo.get('caps').get('udid') if self.devinfo else None
        self.host = self.devinfo.get('host') if self.devinfo else None
        self.cond = ec.visibility_of_element_located

    def set_caps(self, **kwargs):
        self.desired_caps.update(kwargs)
        return self

    def start(self, host=None, **kwargs):
        url = host or self.host
        self.desired_caps.update(kwargs)
        self.driver = webdriver.Remote(url, self.desired_caps)
        return self.driver

    def scroll_to_find(self, by, locator, condition=None, timeout=3, interval=0.2,
                       direction='down', interrupt=None, **kwargs):
        """上/下/左/右滚动查找某一元素
        direction: up, down
        """
        latter_source = self.driver.page_source
        while not self.find(by, locator, condition, timeout=timeout):
            if interrupt:
                if self.find(*interrupt):
                    return
            former_source = latter_source
            self.tofind[direction](**kwargs)
            time.sleep(interval)
            latter_source = self.driver.page_source
            if former_source == latter_source:
                return
        return self.Element

    # def swipe_to_find(self, by, locator, timeout=3, condition=None, interval=0.2,
    #                   direction='left', interrupt=None, **kwargs) -> bool:
    #     """左/右滑动查找某一元素
    #     """
    #     latter_source = self.driver.page_source
    #     while not self.find(by, locator, condition, timeout):
    #         if interrupt:
    #             if self.find(*interrupt):
    #                 return False
    #         former_source = latter_source
    #         self.tofind[direction](**kwargs)
    #         time.sleep(interval)
    #         latter_source = self.driver.page_source
    #         if former_source == latter_source:
    #             return False
    #     return True

    def switch_to_native(self):
        self.driver.switch_to.context(self.driver.contexts[0])

    def switch_to_webview(self):
        self.driver.switch_to.context(self.driver.contexts[-1])

    @staticmethod
    def convert_symbol(text: str):
        txt = ""
        for t in text:
            if t == "'":
                txt = txt + "\"'\""
            elif t == '"':
                txt = txt + '\'"\''
            elif t == "`":
                txt = txt + "\'`\'"
            elif t == "(":
                txt = txt + "\'(\'"
            elif t == ")":
                txt = txt + "\')\'"
            elif t == "|":
                txt = txt + "\'|\'"
            elif t == "<":
                txt = txt + "\'<\'"
            elif t == ">":
                txt = txt + "\'>\'"
            elif t == "&":
                txt = txt + '\'&\''
            elif t == ";":
                txt = txt + '\';\''
            else:
                txt = txt + t
        return txt

    def input_text(self, text: [int, float, str], by: str, locator: str):
        """
        在指定的element输入文字
        :param text: 输入文字
        :param by: element的定位方式
        :param locator: element的参数，比如name,id等
        :return:
        """
        try:
            text = self.convert_symbol(str(text))
            element = WebDriverWait(self.driver, 20, 0.5).until(ec.element_to_be_clickable(
                (by, locator)))
            element.clear()
            self.driver.set_value(element, text)
        except TimeoutException:
            raise Exception(f"Element not found: {by} {locator}")

    def scroll(self, direction, start_pos=None, end_pos=None, duration: int = 400, rect=None):
        _scroll = {
            'up': (0.3, 0.8), 'down': (0.8, 0.3),
            'left': (0.1, 0.9), 'right': (0.9, 0.1),
        }
        if rect:
            pass

    def scroll_down(self, start_pos: float = 0.8, end_pos: float = 0.3, duration: int = 800, element=None):
        """
        模拟手指从屏幕底部向上滑的操作 (页面向上滚动，显示下面的内容)
        """
        if element is None:
            scr_width = self.driver.get_window_size()['width']
            scr_height = self.driver.get_window_size()['height']
            self.driver.swipe(scr_width / 2, scr_height * start_pos, scr_width / 2, scr_height * end_pos,
                              duration=duration)
        else:
            rect = element.rect
            self.driver.swipe(rect['x'] + rect['width'] / 2, rect['y'] + rect['height'] * start_pos,
                              rect['x'] + rect['width'] / 2, rect['y'] + rect['height'] * end_pos,
                              duration=duration)

            # self.driver.execute_script("mobile: swipe", {"direction": "up"})

    def scroll_up(self, start_pos: float = 0.3, end_pos: float = 0.8, duration: int = 800,
                  element=None):
        """模拟手指从屏幕顶部向下滑的操作(页面向下滚动，显示上面的内容)

        :param start_pos: 起始位置，值为屏幕或原始宽度的百分比
        :param end_pos: 结束位置，值为屏幕或原始宽度的百分比
        :param duration: 滑动持续时间
        :param element: 是否指定元素
        :return:
        """
        if element is None:
            scr_width = self.driver.get_window_size()['width']
            scr_height = self.driver.get_window_size()['height']
            self.driver.swipe(scr_width / 2, scr_height * start_pos, scr_width / 2, scr_height * end_pos,
                              duration=duration)
        else:
            rect = element.rect
            self.driver.swipe(rect['x'] + rect['width'] / 2, rect['y'] + rect['height'] * start_pos,
                              rect['x'] + rect['width'] / 2, rect['y'] + rect['height'] * end_pos,
                              duration=duration)
        # self.driver.execute_script("mobile: swipe", {"direction": "down"})

    def swipe_right(self, start_pos: float = 0.9, end_pos: float = 0.1, duration: int = 800, element=None):
        """模拟手指从右向左滑动的操作(页面向左滚动，显示右边的内容)

        :param start_pos: 起始点，值为屏幕或原始宽度的百分比
        :param end_pos: 结束点，值为屏幕或原始宽度的百分比
        :param duration: 滑动持续时间
        :param element: 是否指定元素
        :return: None
        """
        if element is None:
            width = self.driver.get_window_size()['width']
            height = self.driver.get_window_size()['height']
            self.driver.swipe(width * start_pos, height / 2, width * end_pos, height / 2, duration=duration)
        else:
            rect = element.rect
            self.driver.swipe(rect['x'] + rect['width'] * start_pos, rect['y'] + rect['height'] / 2,
                              rect['x'] + rect['width'] * end_pos, rect['y'] + rect['height'] / 2, duration=duration)

    def swipe_left(self, start_pos: float = 0.1, end_pos: float = 0.9, duration: int = 800, element=None):
        """模拟手指从左向右滑动的操作(页面向右滚动，显示左边的内容)

        :param start_pos: 起始点，值为屏幕或原始宽度的百分比
        :param end_pos: 结束点，值为屏幕或原始宽度的百分比
        :param duration: 滑动持续时间
        :param element: 是否指定元素
        :return: None
        """
        if element is None:
            width = self.driver.get_window_size()['width']
            height = self.driver.get_window_size()['height']
            self.driver.swipe(width * start_pos, height / 2, width * end_pos, height / 2, duration=duration)
        else:
            rect = element.rect
            self.driver.swipe(rect['x'] + rect['width'] * start_pos, rect['y'] + rect['height'] / 2,
                              rect['x'] + rect['width'] * end_pos, rect['y'] + rect['height'] / 2, duration=duration)

    def scroll_down_to_bottom(self, start_pos: float = 0.8, end_pos: float = 0.3,
                              duration: int = 800, interval: float = 0.5, element=None):
        """滚动到页面底部

        :return:
        """
        try:
            latter_source = self.driver.page_source
            while True:
                former_source = latter_source
                self.scroll_down(start_pos, end_pos, duration, element)
                time.sleep(interval)
                latter_source = self.driver.page_source
                if former_source == latter_source:
                    break
        except Exception as msg:
            raise Exception(msg)

    def scroll_up_to_top(self, start_pos: float = 0.3, end_pos: float = 0.8,
                         duration: int = 800, interval: float = 0.5, element=None):
        """滚动到页面顶部

        :return:
        """
        try:
            latter_source = self.driver.page_source
            while True:
                former_source = latter_source
                self.scroll_up(start_pos, end_pos, duration, element)
                time.sleep(interval)
                latter_source = self.driver.page_source
                if former_source == latter_source:
                    break
        except Exception as msg:
            raise Exception(msg)

    def touch(self, element):
        """
        通过获取元素的中间点坐标来点击visible=false的元素
        :param element:
        :return:
        """
        x = element.location['x'] + element.size['width'] / 2
        y = element.location['y'] + element.size['height'] / 2
        TouchAction(self.driver).tap(x=x, y=y).perform()



