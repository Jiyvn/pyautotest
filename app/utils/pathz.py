import os
import shutil
from pathlib import Path


class pathz(object):

    def __init__(self, f=None):
        self.f = f

    @staticmethod
    def makedirs(dpath):
        if not os.path.exists(dpath):
            os.makedirs(dpath)

    @staticmethod
    def touch(fpath, repc=False):
        if repc:
            if os.path.exists(fpath):
                pathz.delete(fpath)
        if os.path.exists(fpath):
            raise FileExistsError(
                "Cannot create a file when that file already exists: '{}'".format(fpath)
            )
        # Path().touch() won't replace fpath and won't raise error
        Path(fpath).touch()

    @staticmethod
    def delete(path):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)

    @staticmethod
    def copy(src, dst, repc=False):
        """

        :param src:
        :param dst:
        :param repc:
        :return:
        """
        if repc:
            if os.path.exists(dst):
                pathz.delete(dst)
        if os.path.isdir(src):
            # shutil.copytree raise err if dst dir exists
            shutil.copytree(src, dst)
        else:
            # shutil.copy directly replace dst file if exists
            if os.path.exists(dst):
                raise FileExistsError(
                    "Cannot create a file already existed: '{}'".format(dst)
                )
            shutil.copy(src, dst)


