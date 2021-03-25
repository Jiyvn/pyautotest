import os


class Adb(object):

    remote = False

    @staticmethod
    def kill():
        cmd = 'adb kill-server'
        os.popen(cmd)

    @staticmethod
    def start():
        cmd = 'adb start-server'
        os.popen(cmd)

    @staticmethod
    def connect(url) -> None:
        """

        :param url: e.g. 192.168.107.132:5555
        :return:
        """
        cmd = 'adb connect {0}'.format(url)
        os.popen(cmd)

    @staticmethod
    def disconnect(url) -> None:
        """

        :param url: e.g. 192.168.107.132:5555
        :return:
        """
        cmd = 'adb disconnect {0}'.format(url)
        os.popen(cmd)