## pyautotest

`pyautotest` 是一个pytest+allure的集成框架，支持UI/API自动化。

[English](/README.md) | 中文

#### 开始

###### pyauto.py
`pyautotest` 支持多设备并发. 在字典`tests`中设置测试设备和测试信息即可, 注意设备信息必须填写在`device.yml`。

```python
from app.core.parallel import run
from app.main import Pyauto

tests = {
    'XiaoMi 6': {
        'test module':
            [
                'android/test_example.py',
                'android/test_sample.py::TestAndroidSample'
            ],
        'service address': '',
        'pytest args': [],
    },
    'iPhone7': {
        'test module': '',
        'service address': '127.0.0.1:4723',
        'pytest args': [],

    },
    'Chrome88-win': {
        'test module': ['smoke chrome/test_example.py'],
        'pytest args': [],
    },
}

tests_dir = 'tests'
pytest_args = ()
pytest_kwargs = {}
separate = False
allure_report = True
clean = True


pyauto = Pyauto(
    tests=tests, tests_dir=tests_dir,
    separate=separate, allure_report=allure_report, clean=clean,
    args=pytest_args,
    **pytest_kwargs
)


def start_test(d):
    pyauto.start_test(d)


if __name__ == '__main__':
    amount = len(pyauto.params)
    args = [(p, ) for p in pyauto.params]
    run(start_test, args, amount)

```

###### 命令行

- `--test`:  测试模块
- `--device`: 测试设备

`--test/--device` 选项会直接替换字典`tests`, 仅仅在`--device`上执行测试。如果需要修改部分设备信息，可以使用环境变量。
```bash
python pyauto.py --test <module> --device <device>
```

`--help`检查`pyautotest`的选项，但`pyautotest`实际上接受`pytest`的所有参数，可通过命令`pytest --help`查看。

```bash
$python pyauto.py --help
```


#### 依赖

- [pytest](https://github.com/pytest-dev/pytest)
- [allure-pytest](https://github.com/allure-framework/allure-python/tree/master/allure-pytest)
- [PyYAML](https://github.com/yaml/pyyaml)  
- [requests](https://github.com/psf/requests)

###### app/browser
- [Appium-Python-Client](https://github.com/appium/python-client)

###### windows
- [appium/appium-windows-driver](https://github.com/appium/appium-windows-driver)
- [pywinauto/pywinauto](https://github.com/pywinauto/pywinauto) [可选]
- [yinkaisheng/Python-UIAutomation-for-Windows](https://github.com/yinkaisheng/Python-UIAutomation-for-Windows) [可选]

###### macOS
- [appium/appium-for-mac](https://github.com/appium/appium-for-mac)
- [appium/appium-mac-driver [<10.15]](https://github.com/appium/appium-mac-driver)
- [appium/appium-mac2-driver [>=10.15]](https://github.com/appium/appium-mac2-driver)


#### 相关工具[可选]
#### pytest
- [pytest-bdd](https://github.com/pytest-dev/pytest-bdd)
- [pytest-xdist](https://github.com/pytest-dev/pytest-xdist)
- [pytest-cov](https://github.com/pytest-dev/pytest-cov)
- [pytest-html](https://github.com/pytest-dev/pytest-html)
- [pytest-django](https://github.com/pytest-dev/pytest-django)


###### 性能
- [locust](https://github.com/locustio/locust)
- [jmeter](https://jmeter.apache.org/)


####  示例
```python
from app.core.drivers.mobile import Mobile

settings = {
        'bluetooth': (MobileBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeCell[`label == "蓝牙"`]'),
}
bt = {
    'back_button': (MobileBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`label == "设置"`]'),
    'bluetooth_switch': (MobileBy.IOS_PREDICATE, 'type == "XCUIElementTypeSwitch" AND label == "蓝牙"'),
}
page = Mobile(driver) # 'settings' page

print(page.bluetooth.text)
page.bluetooth.click()

page.wait(1)
page.container(bt)  # switch to 'bt' page
assert page.bluetooth_switch.found() is True
page.bluetooth_switch.click()
page.back_button.click()

page.wait(1).container(settings)  # switch back to 'settings' page
page['bluetooth'].click()

page.wait(1).container(bt)
page['bluetooth_switch'].found.click() # click if element found

```