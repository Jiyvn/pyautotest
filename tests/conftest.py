import allure
import pytest

from app import logger
from app.cli import pytestOption
from app.core.appium import AppiumService
from app.loader import Loader

procs = []


def pytest_addoption(parser):
    op = pytestOption(parser)
    # 配置文件
    op.add_config_option()
    # 运行设备：设备名，输入ios/android会选择默认的ios/android设备，未输入会选择default设备
    op.add_device_option()
    # 运行case（模块）: ios/android/bunny/...
    op.add_case_option()
    # log 配置
    # op.add_log_option()
    # output
    op.add_output_option()
    # appium
    op.add_appium_option()

    op.add_attachment_option()


def pytest_sessionstart(session):
    from app import Logger
    Logger.init_logging(
        log_path=session.config.getoption('--log-file')
    )


def pytest_sessionfinish(session, exitstatus):
    normal = False
    for p in procs:
        normal = p.stop()
    if procs and not normal:
        exitstatus = 1


# -----------------------
# ----- config file -----
# -----------------------
@pytest.fixture(scope='session', autouse=True)
def global_config(request):
    return request.config.getoption('--global-config')


@pytest.fixture(scope='session', autouse=True)
def device_config(request):
    return request.config.getoption('--device-config')


# ----------------------
# -----  start up  -----
# ----------------------
@pytest.fixture(scope='session', autouse=True)
def device(request, device_config, output_dir):
    devname = request.config.getoption('--device')
    devconfig = Loader.load(device_config)
    devplatform = request.config.getoption('--platform')
    device_info = devconfig[devname]
    default_caps = Loader().get_default_caps().get(devplatform) or {}
    default_caps.update(device_info['caps'])
    device_info['caps'] = default_caps
    device_info['port'] = request.config.getoption('--port')
    device_info['bp'] = request.config.getoption('--bp')
    device_info['host'] = request.config.getoption('--service-address')
    device_info['output_dir'] = output_dir
    if device_info['port']:
        ap = AppiumService(
            device=device_info['caps'],
            ports=[device_info['port'], device_info['bp']]
        )
        ap.start()
        procs.append(ap)
        device_info['caps'] = ap.device
        device_info['host'] = 'http://127.0.0.1:{}/wd/hub'.format(ap.port)
    else:
        if device_info['host'] and \
                not device_info['host'].startswith('http') and \
                not device_info['host'].endswith('/wd/hub'):
            device_info['host'] = 'http://{}/wd/hub'.format(device_info['host'])
    if devplatform == 'Android' and not device_info['caps'].get('systemPort'):
        device_info['caps']['systemPort'] = request.config.getoption('--system-port')
    elif devplatform == 'iOS' and not device_info['caps'].get('wdaLocalPort'):
        device_info['caps']['wdaLocalPort'] = device_info['bp']
    logger.debug('{} caps: {}'.format(devname, device_info['caps']))
    return device_info


@pytest.fixture(scope='session', autouse=True)
def output_dir(request):
    return request.config.getoption('--output-dir')


@pytest.fixture(scope='session', autouse=True)
def options(request):
    return request.config.option


# ----------------------
# ----- attachment -----
# ----------------------
@pytest.fixture(scope='session', autouse=True)
def disable_screenshot(request):
    return request.config.getoption('--disable-screenshot')


def pytest_exception_interact(node, call, report):
    try:
        if not node.funcargs.get('disable_screenshot'):
            if getattr(node.instance, 'driver'):
                driver = node.instance.driver
                allure.attach(driver.get_screenshot_as_png(), 'Fail screenshot', allure.attachment_type.PNG)
    except AttributeError:
        pass
