#!/usr/bin/env python3
# encoding: utf-8

import os
import platform
import subprocess
from pathlib import Path


class PROJ:

        PLATFORM = platform.system().lower()
        SYS_OS = "windows" if PLATFORM.startswith('windows') else "mac" if PLATFORM.startswith('darwin') else 'linux'
        HOME_DIR = os.getenv("HOME") if os.getenv("HOME") else ""

        # 目录结构
        PROJECT_DIR = Path(os.path.dirname(__file__))
        CONFIG_DIR = PROJECT_DIR
        SCRIPT_DIR = PROJECT_DIR / Path('tests')
        RESULT_DIR = PROJECT_DIR / Path('result')
        REPORT_DIR = PROJECT_DIR / Path('result/reports')
        LOG_DIR = PROJECT_DIR / Path('result/logs')

        # 配置和数据文件
        GLOBAL_FILE = 'global.yml'
        GLOBAL = str(CONFIG_DIR / Path(GLOBAL_FILE))
        DEVICE_FILE = 'device.yml'
        DEVICE = str(CONFIG_DIR / Path(DEVICE_FILE))
        CAPS = str(PROJECT_DIR/Path('capabilities.yml'))
        TEST_CASE_FILE = ''
        TEST_CASE = str(PROJECT_DIR / Path(TEST_CASE_FILE))
        DATA_FILE = ''
        DATA = str(PROJECT_DIR / Path(DATA_FILE))

        # 日志
        LOGGER = 'pyauto'
        LOG_LEVEL = 'DEBUG'
        LOG_PATH = str(LOG_DIR / Path('app.log'))
        DEVICE_LOG = str(PROJECT_DIR / Path('result/logs/{0}.log'))
        ERROR_LOG = str(PROJECT_DIR / Path('result/logs/error.log'))
        DEVICE_ERROR_LOG = str(PROJECT_DIR / Path('result/logs/{0}_error.log'))

        # Appium
        WIN_PREFIX = os.getenv("Appdata")[:-8] if os.getenv("Appdata") else ""
        APPIUM_WIN = [
                WIN_PREFIX + "/Local/Programs/Appium/resources/app/node_modules/appium/build/lib/main.js",
                WIN_PREFIX + "/Local/Programs/appium-desktop/resources/app/node_modules/appium/build/lib/main.js",
                "C:/\"Program Files (x86)\"/Appium/resources/app/node_modules/appium/build/lib/main.js",
                "C:/\"Program Files\"/Appium/resources/app/node_modules/appium/build/lib/main.js",
                # str(subprocess.getoutput('npm root -g')) + "/appium/build/lib/main.js",
                # str(subprocess.getoutput('npm root')) + "/appium/build/lib/main.js",
        ]
        APPIUM_MAC = [
                "/Applications/Appium.app/Contents/Resources/app/node_modules/appium/build/lib/main.js",
                # str(subprocess.getoutput('npm root -g')) + "/appium/build/lib/main.js",
                # str(subprocess.getoutput('npm root')) + "/appium/build/lib/main.js",
        ]
        APPIUM_LINUX = [
                str(subprocess.getoutput('npm root -g')) + "/appium/build/lib/main.js",
                str(subprocess.getoutput('npm root')) + "/appium/build/lib/main.js",
        ]