## pyautotest

`pyautotest` supports UI/API automated testing.


#### Get Start
 
###### pyauto.py
`pyautotest` supports multi-device concurrency. Just set all the tests in dict `tests`, notice that the device should be found in `device.yml`

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

###### commandline

- `--test`:  test module
- `--device`: test device

`--test/--device` will directly replace `tests`, and just testing on `--device`. To change some info of device, use environment variable instead.
```bash
python pyauto.py --test <module> --device <device>
```

`--help` to show all `pyauto` options. But `pyauto` actually accepts all `pytest` arguments. check `pytest --help` for `pytest`.

```bash
$python pyauto.py --help
```


#### Dependencies

- [pytest](https://github.com/pytest-dev/pytest)
- [allure-pytest](https://github.com/allure-framework/allure-python/tree/master/allure-pytest)
- [PyYAML](https://github.com/yaml/pyyaml)  
- [requests](https://github.com/psf/requests)

###### app/browser
- [Appium-Python-Client](https://github.com/appium/python-client)

###### windows
- [appium/appium-windows-driver](https://github.com/appium/appium-windows-driver)
- [pywinauto/pywinauto [optional]](https://github.com/pywinauto/pywinauto)
- [yinkaisheng/Python-UIAutomation-for-Windows [optional]](https://github.com/yinkaisheng/Python-UIAutomation-for-Windows)

###### macos
- [appium/appium-for-mac](https://github.com/appium/appium-for-mac)
- [appium/appium-mac-driver [<10.15]](https://github.com/appium/appium-mac-driver)
- [appium/appium-mac2-driver [>=10.15]](https://github.com/appium/appium-mac2-driver)

#### Other tools
###### performance
- [locust](https://github.com/locustio/locust)
- [jmeter](https://jmeter.apache.org/)

####  Example
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