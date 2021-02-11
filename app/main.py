import sys
import os
import time
from pathlib import Path
import pytest

from app import Logger
from app.cli import Parser, appOptions
from app.core.communication import get_free_port
from app.core.exceptions import ArgsError
from app.utils.confile import reader
from constant import PROJ


def dump_report(data_dir, report_dir, clean=True):
    os.system('allure generate {0} -o {1} {2}'.format(
        data_dir, report_dir, '--clean' if clean else '')
    )


def __convert(string):
    return '\"' + string + '\"' \
        if ' ' in string and '\"' not in string \
        else string


def _make(*dirpath):
    for d in dirpath:
        if not os.path.exists(d):
            os.makedirs(d)


def start_test(device: dict, extra_args: [list, tuple], extra_kw: dict, clean=True):
    _make(
        device['allure_data_dir'],
        device['allure_report_dir'],
        device['xml_dir']
    )
    device['pytest args'].extend(extra_args)
    pytest.main(device['pytest args'], **extra_kw)
    dump_report(
        __convert(device['allure_data_dir']),
        __convert(device['allure_report_dir']),
        clean
    )


class Pyauto(object):

    def __init__(self,
                 tests: dict = None,
                 separate=False, allure_report=False, clean=False,
                 global_config=None, device_config=None,
                 tests_dir=None,
                 disable_screenshot=False,
                 args=(), **kwargs
                 ):
        self.single_device = False
        self.global_config_file = global_config
        self.device_config_file = device_config
        self.tests_dir = tests_dir or str(PROJ.SCRIPT_DIR)
        self.tests = tests or {}
        self.disable_screenshot = disable_screenshot
        self.separate = separate
        self.report_dir = str(PROJ.REPORT_DIR)
        self.dump_allure_report = allure_report
        self.clean = clean
        self.log_level = None
        self.test_time = time.strftime("%Y-%m-%d_%H%M%S", time.localtime())

        # 解析
        self.sys_argv = sys.argv[1:]
        self.option_args, self.pytest_args = Parser().parse_known_args(self.sys_argv)
        self.extra_args = args
        self.extra_kw = kwargs
        self.pytest_args.extend(self.extra_args)

        self.help_me()
        # print('time: {}'.format(time.localtime()))
        # print(self.option_args)
        # print(self.pytest_args)

        self.initialize()

    def help_me(self):
        if self.option_args.show_devices:
            for k, v in reader.read(PROJ.DEVICE).items():
                print(f'{k}: {v}')
            sys.exit(0)
        if self.option_args.clean_report:
            import shutil
            print('removing {}'.format(PROJ.REPORT_DIR))
            shutil.rmtree(PROJ.REPORT_DIR)
            sys.exit(0)

    def config_log(self):
        self._make(PROJ.LOG_DIR)
        if appOptions.log_level in self.sys_argv and \
                self.option_args.pyauto_log_level != self.log_level:
            self.log_level = self.option_args.log_level
        if '--log-file' in self.pytest_args:
            self.log_file_set = True
        else:
            self.log_file_set = False
        Logger.init_logging(
            level=self.log_level,
            mode='rt',
            # log_path=str(PROJ.LOG_DIR/Path(f'app_{self.test_time}'))
        )
        return self

    def load_info(self):
        if appOptions.global_config in self.sys_argv and \
                self.option_args.global_config != self.global_config_file:
            self.global_config_file = self.option_args.global_config
        if appOptions.device_config in self.sys_argv and \
                self.option_args.device_config != self.device_config_file:
            self.device_config_file = self.option_args.device_config
        if not self.global_config_file:
            self.global_config_file = str(PROJ.GLOBAL)
        if not self.device_config_file:
            self.device_config_file = str(PROJ.DEVICE)
        self.device_config = reader.read(self.device_config_file)
        return self

    def get_tests(self):
        if appOptions.tests_dir in self.sys_argv and \
                self.option_args.tests_dir != self.tests_dir:
            self.tests_dir = self.option_args.tests_dir
        self.default_device = self.get_default_device()
        device = self.option_args.device
        test = self.option_args.test
        if device or test:
            device = self.get_device_name(device)
            if not test:
                if device in self.tests:
                    self.tests = {
                        device: self.tests[device]
                    }
                else:
                    test = self.get_default_test(device)
                    self.tests = {
                        device: {'test module': [test]}
                    }
            else:
                self.tests = {device, {'test module': [test]}}
        for d in self.tests:
            if not self.tests[d].get('test module'):
                test = self.get_default_test(d)
                self.tests[d]['test module'] = [test]

        if not self.tests:
            print('No tests set, using default configuration')
            if not self.default_device:
                raise ArgsError('No default device set')
            test = self.get_default_test(self.default_device)
            self.tests = {self.default_device, {'test module': [test]}}
        self.devices = self.tests.keys()

        return self

    def get_device_name(self, d):
        if str(d).lower() not in \
                ['ios', 'android', 'browser', 'windows', 'mac']:
            d = self.device_config[d.lower().capitalize()]
        else:
            d = d or self.default_device
            if d:
                if d.lower() in \
                        ['ios', 'android', 'browser', 'windows', 'mac']:
                    d = self.device_config[d.lower().capitalize()]
        if not d:
            raise ArgsError(
                'No device set to be testing! '
                'set Default device in `device.yml` at least'
            )
        return d

    def get_default_device(self):
        return self.device_config['Default']

    def get_default_test(self, d):
        device_info = self.device_config[d]
        test = '{0}/{1}'.format(
            self.tests_dir,
            device_info['caps'].get('platformName').lower() if
            device_info['caps'].get('platformName') else
            device_info['caps'].get('browserName').lower()
        )
        return test

    def set_service(self):
        service_address = self.option_args.service_address
        bp = self.option_args.bp
        if len(self.devices) <= 1:
            for d in self.tests:
                device_info = self.device_config[d]
                self.tests[d]['service address'] = \
                    service_address or self.tests[d].get('service address') or device_info.get('host')
                self.tests[d]['bp'] = bp or get_free_port(4726)[0][0]
        else:
            self.get_session_devices()
            self.__set_ports()
            self.__set_sysport()
        return self

    def __set_ports(self):
        sessions_amount = len(self._sessions)
        ports = iter(get_free_port(4726, sessions_amount, 2))
        for d in self._sessions:
            ps = next(ports)
            self.tests[d]['port'] = ps[0]
            self.tests[d]['bp'] = ps[1]

    def __set_sysport(self):
        as_amount = len(self._android_local_remote) + len(self._android_sessions)
        sysports = iter(get_free_port(8200, as_amount))
        for d in (self._sessions+self._android_local_remote):
            ps = next(sysports)
            self.tests[d]['systemPort'] = ps[0]

    def get_session_devices(self):
        self._sessions = []
        self._android_sessions = []
        self._android_local_remote = []
        for d in self.tests:
            device_info = self.device_config[d]
            platform = device_info['caps'].get('browserName') or device_info['caps'].get('platformName')
            self.tests[d]['platform'] = platform
            # ios/android temporarily
            if platform.lower() in ['ios', 'android'] and not self.tests[d].get('service address'):
                self._sessions.append(d)
                if platform.lower() == 'android':
                    self._android_sessions.append(d)
            if self.tests[d].get('service address') in ['127.0.0.1'] and platform.lower() == 'android':
                self._android_local_remote.append(d)
        # print('sessions for: {}'.format(self._sessions))
        return self._sessions

    def set_result(self):
        if appOptions.separate in self.sys_argv and \
                self.option_args.separate != self.separate:
            self.separate = self.option_args.separate
        if appOptions.output_dir in self.sys_argv and \
                self.option_args.output_dir != self.report_dir:
            self.report_dir = self.option_args.output_dir

        self.junitxml = any(str(x).startswith('--junit-xml') for x in self.pytest_args)
        if (self.junitxml or '--alluredir' in self.pytest_args) and len(self.devices) > 1:
            raise ArgsError(
                'Should not set `--alluredir` or `--junit-xml` when more than one devices'
            )

        for d in self.tests:
            if self.separate:
                report_dir = Path(self.report_dir) / Path(d) / Path(self.test_time)
            else:
                report_dir = Path(self.report_dir) / Path(d)
            self.tests[d]['output_dir'] = str(report_dir)

            self.tests[d]['log_file'] = str(report_dir / Path("{}_{}.log".format(d, self.test_time)))
            device_info = self.device_config[d]
            version = device_info['caps'].get('platformVersion') or device_info['caps'].get('version')
            self.tests[d]['allure_report_dir'] = str(report_dir / Path('allure-report'))
            if '--alluredir' not in self.pytest_args:
                self.tests[d]['allure_data_dir'] = str(report_dir / Path('allure-data'))
            if not self.junitxml:
                xml_dir = report_dir / Path('junit-xml')
                self.tests[d]['xml_dir'] = str(xml_dir)
                self.tests[d]['xml'] = str(xml_dir / Path("{}_{}_{}.xml".format(d, version, self.test_time)))

        return self

    def set_allure(self):
        if appOptions.allure_report in self.sys_argv and \
                self.option_args.allure_report != self.dump_allure_report:
            self.dump_allure_report = self.option_args.allure_report

        if appOptions.clean in self.sys_argv and \
                self.option_args.clean != self.clean:
            self.clean = self.option_args.clean
        return self

    def config_testing(self):
        if appOptions.disable_screenshot in self.sys_argv and \
                self.option_args.disable_screenshot != self.disable_screenshot:
            self.disable_screenshot = self.option_args.disable_screenshot
        return self

    def initialize(self):
        # 日志
        self.config_log()

        # 加载配置文件和设备信息
        self.load_info()

        # 设备信息和测试模块
        # > 可通过--test <module> --device <device>
        # > 传入（单设备），覆盖tests多设备字典
        self.get_tests()

        # appium服务
        self.set_service()

        # 结果目录
        self.set_result()

        # testing设置
        self.config_testing()

        # allure报告
        self.set_allure()

        self.complete_argv()
        return self

    @staticmethod
    def _make(*dirpath):
        for d in dirpath:
            if not os.path.exists(d):
                os.makedirs(d)

    # def start(self):
    #     logging.shutdown()
    #     run(
    #         self.start_test, self.params, len(self.params)
    #     )

    def start_test(self, device: dict):
        self._make(
            device['allure_data_dir'],
            device['allure_report_dir'],
            device['xml_dir']
        )
        self.start_pytest(
            device['pytest args'],
        )
        self.dump_report(
            self.__convert(device['allure_data_dir']),
            self.__convert(device['allure_report_dir'])
        )

    def start_pytest(self, args):
        pytest.main(args, **self.extra_kw)

    def dump_report(self, data_dir, report_dir):
        if self.dump_allure_report:
            os.system('allure generate {0} -o {1} {2}'.format(
                data_dir,
                report_dir,
                '--clean' if self.clean else ''
            ))

    def decode_module(self, t):
        if os.path.exists(t) or os.path.exists('{0}'.format(str(t).split('::')[0])):
            return t
        elif os.path.exists('{0}/{1}'.format(self.tests_dir, t)) or \
                os.path.exists('{0}'.format(str(Path(self.tests_dir) / Path(t)).split('::')[0])):
            return '{0}/{1}'.format(self.tests_dir, t)
        return t

    def get_test_module(self, test):
        modules = []
        ts = iter(test)
        while True:
            try:
                t = next(ts)
                if os.path.exists(t) or os.path.exists('{0}'.format(str(t).split('::')[0])):
                    modules.append(t)
                elif os.path.exists('{0}/{1}'.format(self.tests_dir, t)) or \
                        os.path.exists('{0}'.format(Path(self.tests_dir)/Path(t)).split('::')[0]):
                    modules.append('{0}/{1}'.format(self.tests_dir, t))
                else:
                    modules.append('-m')
                    modules.append(t.split()[0])
                    modules.append(self.decode_module(t.split()[-1]))
            except StopIteration:
                break
        return modules

    def __convert(self, string):
        return '\"' + string + '\"' \
            if ' ' in string and '\"' not in string \
            else string

    def complete_argv(self):
        for d in self.devices:
            device = self.tests[d]
            test_module = self.get_test_module(device.get('test module'))

            if '--alluredir' not in self.sys_argv:
                test_module.append('--alluredir')
                test_module.append(device['allure_data_dir'])

            test_module.append('--output-dir')
            test_module.append(device['output_dir'])

            if not self.junitxml:
                test_module.append('--junit-xml')
                test_module.append(device['xml'])

            test_module.append('--global-config')
            test_module.append(self.global_config_file)

            test_module.append('--device-config')
            test_module.append(self.device_config_file)

            test_module.append('--device')
            test_module.append(d)

            test_module.append('--platform')
            test_module.append(self.tests[d]['platform'])

            if not self.log_file_set:
                test_module.append('--log-file')
                test_module.append(self.tests[d]['log_file'])

            if device.get('service address'):
                test_module.append('--service-address')
                test_module.append(device.get('service address'))
            if device.get('port'):
                test_module.append('--port')
                test_module.append(device.get('port'))
            if device.get('systemPort'):
                test_module.append('--system-port')
                test_module.append(device.get('systemPort'))
            if device.get('bp'):
                test_module.append('--bp')
                test_module.append(device.get('bp'))

            if self.disable_screenshot:
                test_module.append('--disable-screenshot')

            if device.get('pytest args'):
                test_module.extend(device['pytest args'])
            else:
                test_module.extend(self.pytest_args)
            device['pytest args'] = test_module
            # print(device)

    @property
    def params(self):
        return [v for k, v in self.tests.items()]

    @property
    def amount(self):
        return len(self.params)

