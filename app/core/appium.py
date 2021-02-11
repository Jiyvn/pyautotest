#!/usr/bin/env python3
# encoding: utf-8

import os
import platform
import subprocess
import time
from pathlib import Path
from typing import Optional
from urllib.error import URLError

from urllib3.exceptions import NewConnectionError, MaxRetryError

from app import logger
from app.core.communication import get_free_port
from app.core.exceptions import AppiumNotFound, AppiumNotStart, ArgsError
from constant import PROJ

PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))


class AppiumService:

    def __init__(self, device: dict = None, ports: list = None,
                 log_dir=None, relaxed_security=False, timestamp=None):
        self._p: Optional[subprocess.Popen] = None
        self.args = ['node']
        self.device = device or {}
        self.device_name = device.get('deviceName')
        self.platform = device.get('platformName')
        if self.platform:
            self.platform = self.platform.lower()
        self.udid = device.get('udid')
        self.ports = ports
        self.port = ports[0] if ports else None
        self.bp = ports[1] if ports else None
        self.log_dir = log_dir or PROJ.LOG_DIR
        self.relaxed = relaxed_security
        self.log_time = timestamp

    def add_args(self, *args, **kwargs):
        for a in args:
            self.args.append(a)
        for k, v in kwargs.items():
            self.args.append(k)
            self.args.append(v)

    def set_timestamp(self, ts=None):
        self.log_time = ts or self.log_time
        if not self.log_time:
            raise ArgsError('timestamp must be set')
        return self

    def set_platform(self, device_platform=None):
        self.platform = device_platform or self.platform
        if not self.platform:
            raise ArgsError('platform must be set')
        return self

    def set_logfile(self, logfile=None):
        if logfile:
            self.appium_log = str(logfile) if Path(logfile).is_file() else str(self.log_dir/Path(logfile))
        else:
            self.appium_log = str(Path(self.log_dir).joinpath(
                "appium_{}_{}.log".format(
                    self.device_name,
                    self.log_time or time.strftime("%Y-%m-%d_%H%M%S", time.localtime())
                )))
        self.args.append('-g')
        self.args.append(self.appium_log)
        return self

    def get_mainjs(self, mainjs=None):
        if not mainjs:
            js = {
                'mac': PROJ.APPIUM_MAC,
                'linux': PROJ.APPIUM_LINUX,
                'windows': PROJ.APPIUM_WIN,
            }
            for f in js[PROJ.SYS_OS]:
                if os.path.isfile(f):
                    mainjs = f
        if not mainjs:
            raise AppiumNotFound(
                'Appium not found, please install Appium or set main script at `constant.py`')
        self.args.append('{}'.format(mainjs))
        self.args.append('--session-override')
        if self.relaxed:
            self.args.append('--relaxed-security')
        return self

    def set_port(self, port=None):
        self.port = port or self.port
        if not self.port:
            raise ArgsError('port must be not None')
        self.args.append('-p')
        self.args.append('{}'.format(self.port))
        return self

    def set_bp(self, port=None):
        self.bp = port or self.bp
        if not self.platform:
            raise ArgsError('platform not set')
        if not self.bp:
            raise ArgsError('bp must be not None')
        if self.platform == 'ios':
            self.device['wdaLocalPort'] = '{}'.format(self.bp)
            self.args.append('--webdriveragent-port')
        else:
            # self.device['systemPort'] = '{}'.format(self.bp)
            # self.device['systemPort'] = '{}'.format(system_port or get_free_port(8200)[0][0])
            self.args.append('--bootstrap-port')
        self.args.append('{}'.format(self.bp))
        return self

    def add_udid(self, udid=None):
        self.udid = udid or self.udid
        if not self.udid:
            raise ArgsError('udid must be set')
        self.device['udid'] = self.udid
        self.args.append('-U')
        self.args.append('{}'.format(self.udid))
        return self

    def set_log_level(self, level=None):
        self.args.append('--log-level')
        self.args.append(level or 'debug')
        return self

    def start(self, ports=None, timeout=120):
        if len(self.args) == 1:
            ports = ports or self.ports or get_free_port(4726, 1, amount_per_pair=2)[0]
            if ports != self.ports:
                self.port, self.bp = ports[0], ports[1]
            self.get_mainjs().set_port().set_bp().add_udid()
            self.set_log_level().set_logfile()
        logger.debug('appium startup args: {}'.format(self.args))
        logger.debug('appium log: {}'.format(self.appium_log))
        self.start_appium(self.args, timeout=timeout)

    def start_appium(self, arg: [str, list], timeout=120):
        if isinstance(arg, str):
            kw = dict(shell=True)
        else:
            kw = dict(shell=False)
        kw.update(dict(stdout=subprocess.PIPE, stderr=subprocess.PIPE))
        if PROJ.PLATFORM in ["darwin", "linux"]:
            kw.update(dict(bufsize=1, close_fds=True))
        self._p = subprocess.Popen(self.args, **kw)
        if not self._running(
                "http://127.0.0.1:{}".format(self.port) + "/wd/hub" + "/status",
                timeout=timeout
        ):
            raise AppiumNotStart('Fail to start appium')
        self.pid = self._p.pid
        logger.debug('----- appium pid: {} -----'.format(self.pid))

    def response_valid(self, url: str):
        try:
            if PROJ.SYS_OS == 'windows':
                import urllib.request
                status_code = urllib.request.urlopen(url, timeout=5).getcode()
                if status_code < 400:
                    return True
            else:
                # import urllib3
                # status_code = urllib3.PoolManager(timeout=1.0).request('HEAD', f'{url}').status
                # if status_code < 400:
                #     return True
                line = self._p.stdout.readline().strip().decode()
                if 'listener started' in line or 'Error: listen' in line:
                    return True
        except (URLError, MaxRetryError, NewConnectionError):
            return False
        return False

    def _running(self, url: str, timeout: int):
        start_time = time.time()
        while time.time() < start_time + timeout:
            try:
                logger.info("------- starting appium -------")
                if self.response_valid(url):
                    logger.info("------- appium started -------")
                    return True
            except URLError:
                pass
            time.sleep(1.0)
        return False

    def stop(self):
        stoped = False
        if self._p and not self._p.poll():
            self._p.terminate()
            stoped = True
        if stoped:
            logger.debug('----- appium {} stopped -----'.format(self.pid))
        else:
            logger.debug('----- error when stopping appium {} -----'.format(
                self.pid))
        return stoped

    @staticmethod
    def stop_server():
        sysstr = platform.system()
        if sysstr == 'Windows':
            os.popen("taskkill /f /im node.exe")
        else:
            os.popen("killall -2 node")
            os.popen('killall -2 iproxy')
        time.sleep(2)

    def get_pid(self, port=None):
        pid = None
        if PROJ.SYS_OS != 'windows':
            cmd = 'lsof -i tcp:{}'.format(port or self.port)
            res = subprocess.getoutput(cmd)
            if res:
                pid = res.split('\n')[-1].split()[1].strip()
        else:
            cmd = 'netstat -ano|findstr 0.0.0.0:{}'.format(port)
            res = subprocess.getoutput(cmd)
            if res:
                pid = res.split()[-1].strip()
        return pid

    def stop_process(self, pid=None):
        pid = pid or self.get_pid()
        if PROJ.SYS_OS == 'windows':
            killcmd = 'taskkill /f /pid {}'.format(pid)
        else:
            killcmd = 'kill {}'.format(pid)
        os.popen(killcmd)
