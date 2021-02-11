import subprocess
from pathlib import Path

from selenium.common.exceptions import InvalidSessionIdException
from app.core.drivers.mobile import Mobile


class IOS(Mobile):

    def app(self, bundle_id):
        self.desired_caps['bundleId'] = bundle_id

    def set_caps(self, **kwargs):
        super().set_caps(**kwargs)
        if 'browserName' in kwargs:
            # del self.desired_caps['bundleId']
            self.desired_caps['bundleId'] = None
        return self

    def app_installed(self, bundle_id: str) -> bool:
        # check_cmd = 'ios-deploy --exists --bundle_id "{0}"'.format(package_name)
        if self.driver.is_app_installed(bundle_id):
            return True
        else:
            return False

    def switch_to_app(self, bundle_id: str):
        args = {
            'bundleId': bundle_id
        }
        try:
            self.driver.execute_script('mobile: activateApp', args)
        except InvalidSessionIdException:
            raise InvalidSessionIdException("Please make sure the App has been launched")

    def install(self, bundle_id: str, installer_path,
                timeout: float = 120, interval: float = 3):
        try:
            count = 1
            # install_cmd = 'ios-deploy -b "{0}"'.format(Path(installer_path + '/' + installer_name))
            self.driver.install_app(str(Path(installer_path)))
            while not self.app_installed(bundle_id):
                self.wait(interval)
                if count * interval > timeout:
                    break
                count += 1

        except Exception as msg:
            raise Exception(msg)

    def uninstall(self, bundle_id: str):
        """
        using ios-deploy to do install or uninstall app in iOS device
        install via "npm i -g ios-deploy"
        :return:
        """
        self.driver.remove_app(bundle_id)
        # uninstall_cmd = 'ios-deploy --uninstall_only --bundle_id "{0}"'.format(bundle_id)
        # status = subprocess.Popen(
        #     uninstall_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        # ).stdout.readlines()

    def open_app(self, bundle_id=None):
        if bundle_id:
            args = {
                'bundleId': bundle_id
            }
            self.driver.execute_script('mobile: launchApp', args)
        else:
            self.driver.launch_app()

    def reopen_app(self, bundle_id):
        self.close_app(bundle_id)
        self.wait(1)
        self.open_app(bundle_id)

    def close_app(self, bundle_id: str = None):
        if bundle_id:
            args = {
                'bundleId': bundle_id
            }
            self.driver.execute_script('mobile: terminateApp', args)
        else:
            self.driver.close_app()

    def open_notifications(self, start_pos: float = 0.05, end_pos: float = 0.9, duration: int = 1000):
        scr_width = self.driver.get_window_size()['width']
        scr_height = self.driver.get_window_size()['height']
        self.driver.swipe(scr_width * 0.2, scr_height * start_pos, scr_width * 0.2, scr_height * end_pos,
                          duration=duration)

    def close_notifications(self, start_pos: float = 0.95, end_pos: float = 0.1, duration: int = 500):
        scr_width = self.driver.get_window_size()['width']
        scr_height = self.driver.get_window_size()['height']
        self.driver.swipe(scr_width * 0.2, scr_height * start_pos, scr_width * 0.2, scr_height * end_pos,
                          duration=duration)