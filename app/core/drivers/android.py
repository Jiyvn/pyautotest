import os
import subprocess
from pathlib import Path

from appium.webdriver.common.mobileby import MobileBy

from app.core.drivers.mobile import Mobile


class Android(Mobile):

    def app(self, package, activity):
        self.desired_caps['appPackage'] = package
        self.desired_caps['appActivity'] = activity
        self.desired_caps["autoGrantPermissions"] = True
        if self.desired_caps['browserName']:
            self.desired_caps['browserName'] = None
        return self

    def set_caps(self, **kwargs):
        super().set_caps(**kwargs)
        if 'browserName' in kwargs:
            # del self.desired_caps['appPackage']
            # del self.desired_caps['appActivity']
            self.desired_caps['appPackage'] = None
            self.desired_caps['appActivity'] = None
        return self

    def _execute_shell(self, cmd, readlines=False):
        if self.remote:
            cmd = cmd.split(' shell ')[-1]
            c = cmd.split()[0]
            result = self.driver.execute_script('mobile: shell', {
                'command': c,
                'args': cmd.split(c)[-1].strip(),
                'includeStderr': True,
                'timeout': 5000
            })
            return result['stdout']
        else:
            if readlines:
                return os.popen(cmd).readlines()
            else:
                os.popen(cmd)

    def enable_gps(self):
        cmd = f'adb -s {self.udid} shell settings put secure location_providers_allowed +gps'
        self._execute_shell(cmd)

    def disable_gps(self):
        cmd = f'adb -s {self.udid} shell settings put secure location_providers_allowed -gps'
        self._execute_shell(cmd)

    def app_installed(self, package: str) -> bool:
        cmd = f'adb -s {self.udid} shell pm list package -3 -f'
        packages = self._execute_shell(cmd, readlines=True)
        packages = [str(name) for name in packages if package in str(name)]
        if not packages:
            return False
        else:
            return True

    def language(self):
        lang = None
        cmd = f'adb -s {self.udid} shell getprop persist.sys.locale'
        res = self._execute_shell(cmd, readlines=True)[0]
        # language = subprocess.getoutput(cmd)
        if res in ['en-US']:
            lang = 'en'
        elif res in ['zh-Hans-CN', 'zh-CN']:
            lang = 'zh'

        return lang

    def clear_app(self, package: str):
        cmd = f'adb -s {self.udid} shell pm clear {package}'
        self._execute_shell(cmd)

    def get_files(self, path, match_string=None) -> list:
        cmd = f'adb -s {self.udid} shell ls {path}'
        files = self._execute_shell(cmd, readlines=True)
        files = [name.decode().split()[0] for name in files]
        if match_string is not None:
            files = [str(name) for name in files if match_string in str(name)]
        return files

    def close_all(self):
        cmd = f'adb -s {self.udid} shell am kill-all'
        self._execute_shell(cmd)

    def enable_bluetooth(self, force=False):
        if (not force) and self.bluetooth_status() == 1:
            return
        cmd = f"adb -s {self.udid} shell am start -a android.bluetooth.adapter.action.REQUEST_ENABLE"
        self._execute_shell(cmd)
        if self.find(MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textMatches("[Aa][Ll][Ll][Oo][Ww]|允许")'):
            self.get(MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textMatches("[Aa][Ll][Ll][Oo][Ww]|允许")').click()

    def disable_bluetooth(self, force=False):
        if (not force) and self.bluetooth_status() == 0:
            return
        cmd = f"adb -s {self.udid} shell am start -a android.bluetooth.adapter.action.REQUEST_DISABLE"
        self._execute_shell(cmd)
        if self.find(MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textMatches("[Aa][Ll][Ll][Oo][Ww]|允许")'):
            self.get(MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textMatches("[Aa][Ll][Ll][Oo][Ww]|允许")').click()

    def bluetooth_status(self):
        cmd = f"adb -s {self.udid} shell settings get global bluetooth_on"
        res = self._execute_shell(cmd, readlines=True)
        return int(res[0].split()[0])

    def disable_wifi(self):
        cmd = f'adb -s {self.udid} shell am broadcast -a io.appium.settings.wifi --es setstatus disable'
        self._execute_shell(cmd)

    def enable_wifi(self):
        cmd = f'adb -s {self.udid} shell am broadcast -a io.appium.settings.wifi --es setstatus enable'
        self._execute_shell(cmd)

    def install(self, installer_path, package=None,
                timeout: float = 120, interval: float = 3):
        try:
            if self.remote:
                self.driver.install_app(installer_path)
            else:
                cmd = 'adb -s {0} install -g {1}'.format(self.udid, Path(installer_path))
                os.popen(cmd)
            count = 1
            while not self.app_installed(package):
                self.wait(interval)
                if count * interval > timeout:
                    break
                count += 1

        except Exception as msg:
            raise Exception(msg)

    def uninstall(self, package: str):
        if self.remote:
            self.driver.remove_app()
        else:
            cmd = 'adb -s {0} uninstall {1}'.format(self.udid, package)
            status = subprocess.Popen(
                cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            ).stdout.readlines()

    def open_app(self, package: str, activity: str = None, wait_activity: str = None):
        if wait_activity:
            self.driver.start_activity(package, activity, app_wait_activity=wait_activity)
        else:
            self.driver.start_activity(package, activity)
            self.driver.wait_activity(activity, timeout=30)

    def reopen_app(self, package, activity=None, wait_activity=None):
        self.close_app(package)
        self.wait(1)
        self.open_app(package, activity=activity, wait_activity=wait_activity)

    def close_app(self, package: str = None):
        cmd = 'adb -s %s shell am force-stop %s' % (self.udid, package)
        self._execute_shell(cmd)
