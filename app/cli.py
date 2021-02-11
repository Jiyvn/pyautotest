import argparse


class appOptions:

    show_devices = '--show-devices'
    clean_report = '--clean-report'

    device_config = '--device-config'
    global_config = '--global-config'
    test_case = '--test-case'

    tests_dir = '--tests-dir'
    device = '--device'
    test = '--test'

    service_address = '--service-address'
    bp = '--bp'
    disable_screenshot = '--disable-screenshot'

    output_dir = '--output-dir'
    separate = '--separate'
    allure_report = '--allure-report'
    clean = '--clean'
    log_level = '--pyauto-log-level'
    # log_file = '--pyauto-log-file'


class Parser(object):

    def __init__(self, parser=None, attach=True):
        self.options = None
        self.parser = parser or argparse.ArgumentParser()
        if attach:
            self.addoption()

    def addoption(self):
        self.add_help_option()
        # 配置文件
        self.add_config_option()
        # 测试设备
        self.add_device_option()
        # 测试模块
        self.add_tests_option()
        # log配置
        self.add_log_option()
        # output
        self.add_output_option()
        # appium
        self.add_appium_option()
        # testing
        self.add_testing_option()

    def parse_arg(self, op=None):
        self.options = self.parser.parse_args(op)
        return self.options

    def parse_known_args(self, op):
        return self.parser.parse_known_args(op)

    def add_config_option(self):
        # 配置文件
        self.parser.add_argument(
            appOptions.device_config,
            type=str,
            help='device configuration file'
        )

        self.parser.add_argument(
            appOptions.global_config,
            type=str,
            help='global configuration file'
        )
        self.parser.add_argument(
            appOptions.test_case,
            type=str,
            help='Test case file'
        )

    def add_device_option(self):
        # 运行设备：设备名，输入ios/android会选择默认的ios/android设备，未输入会选择default设备
        self.parser.add_argument(
            appOptions.device,
            type=str,
            help='device to test on, such as ios, android, <device>'
        )

    def add_tests_option(self):
        # 运行case（模块）: ios/android/...
        self.parser.add_argument(
            appOptions.test,
            nargs='*',
            help='Test case to run, such as: ios, android, <dir>/<test_case.py>'
        )
        self.parser.add_argument(
            appOptions.tests_dir,
            type=str,
            help='Test case to run, such as: ios, android, <dir>/<test_case.py>'
        )

    def add_testing_option(self):

        self.parser.add_argument(
            appOptions.disable_screenshot,
            action='store_true',
            help='Disable device screenshot',
        )

    def add_log_option(self):
        # log 配置
        self.parser.add_argument(
            appOptions.log_level,
            type=str,
            help='pyautotest log level',
        )

    def add_output_option(self):
        # report
        self.parser.add_argument(
            appOptions.output_dir,
            type=str,
            help='test report directory'
        )
        self.parser.add_argument(
            appOptions.separate,
            action='store_true',
            help='separate report directory each run',
        )
        self.parser.add_argument(
            appOptions.allure_report,
            action='store_true',
            help='generate allure report',
        )
        self.parser.add_argument(
            appOptions.clean,
            action='store_true',
            help='--clean for allure report command',
        )

    def add_appium_option(self):
        # appium
        self.parser.add_argument(
            appOptions.service_address,
            type=str,
            help='Appium service address'
        )
        self.parser.add_argument(
            appOptions.bp,
            type=str,
            help='WebDriverAgent port or Bootstrap port'
        )

    def add_help_option(self):
        self.parser.add_argument(
            appOptions.show_devices,
            action='store_true',
            help='show available devices in device.yml',
        )
        self.parser.add_argument(
            appOptions.clean_report,
            action='store_true',
            help='clean reports, excluding logs',
        )


class pytestOption(object):

    def __init__(self, parser):
        self.parser = parser

    def add_config_option(self):
        # 配置文件
        self.parser.addoption(
            '--device-config',
            type=str,
            help='device configuration file'
        )
        self.parser.addoption(
            '--global-config',
            type=str,
            help='global configuration file'
        )
        self.parser.addoption(
            '--test-case',
            type=str,
            help='Test case file'
        )
        self.parser.addoption(
            '--data',
            type=str,
            help='Data file'
        )

    def add_device_option(self):
        # 运行设备：设备名，输入ios/android会选择默认的ios/android设备，未输入会选择default设备
        self.parser.addoption(
            '--device',
            type=str,
            help='device to test on, such as ios, android, <device>'
        )
        self.parser.addoption(
            '--system-port',
            type=str,
            help='android desired capabilities - systemPort'
        )

        self.parser.addoption(
            '--platform',
            type=str,
            help='testing device platform, such as ios/android'
        )

    def add_case_option(self):
        # 运行case（模块）: ios/android/bunny/...
        self.parser.addoption(
            '--test',
            type=str,
            help='Test case to run, such as: ios, android, <test_case.py>'
        )

    def add_log_option(self):
        # log 配置
        self.parser.addoption(
            '--pyauto-log-file',
            type=str,
            help='pyautotest log level',
        )

    def add_output_option(self):
        # report
        self.parser.addoption(
            '--output-dir',
            type=str,
            help='output directory'
        )

    def add_appium_option(self):
        # appium
        self.parser.addoption(
            '--service-address',
            type=str,
            help='Appium server host'
        )
        self.parser.addoption(
            '--port',
            type=str,
            help='Appium server host'
        )
        self.parser.addoption(
            '--bp',
            type=str,
            help='WebDriverAgent Port or Bootstrap Port'
        )

    def add_attachment_option(self):
        self.parser.addoption(
            '--disable-screenshot',
            action='store_true',
            help='Disable screenshot',
        )