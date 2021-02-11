#!/usr/bin/env python3
# encoding: utf-8

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
    run(
        start_test,
        [(p, ) for p in pyauto.params],
        len(pyauto.params)
    )