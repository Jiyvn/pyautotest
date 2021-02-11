import json
import logging
import logging.config
from pathlib import Path

from constant import PROJ

_configuration = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(levelname)s %(asctime)s %(message)s",
            "datefmt": "%Y/%m/%d %X"
        },
        "developer": {
            "format": "[%(levelname)s] %(asctime)s [%(name)s] [%(filename)s - %(funcName)s:%(lineno)d] %(message)s",
            "datefmt": "%Y/%m/%d %X"
        },
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "developer",
            "stream": "ext://sys.stdout"
        },

        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "developer",
            "maxBytes": 10485760,
            "backupCount": 20,
            "encoding": "utf8"
        }
    },

    "loggers": {
        'pyauto': {
            'level': 'DEBUG',
            "handlers": ["console", "file"],
            "propagate": False
        }
    }
}


class Logger(object):

    config = _configuration
    name = PROJ.LOGGER
    level = 'DEBUG'
    log_path = PROJ.LOG_PATH

    @staticmethod
    def init_logging(name=None, config=None, level=None, log_path=None, mode=None):
        Logger.name = name or Logger.name
        config = config or Logger.config
        if not isinstance(config, dict):
            if not Path(config).is_file():
                raise FileNotFoundError('Invalid log configuration: {}'.format(config))
            mode = mode or 'rt+'
            with open(config, mode) as f:
                config = json.load(f)
        log_path = log_path or Logger.log_path
        if not Path(log_path).exists():
            Path(log_path).touch()
        config['handlers']['file']['filename'] = log_path
        if Logger.name not in config['loggers']:
            config['loggers'][Logger.name] = config['loggers'][Logger.name]
        config['loggers'][Logger.name]['level'] = level or Logger.level
        logging.config.dictConfig(config)
        return Logger

    @staticmethod
    def set_level(level=None):
        Logger.level = level or Logger.level
        return Logger

    @staticmethod
    def set_logfile(file=None):
        Logger.log_path = file or Logger.log_path
        return Logger

    @staticmethod
    def getLogger(name=None):
        Logger.name = name or Logger.name
        return logging.getLogger(Logger.name)

