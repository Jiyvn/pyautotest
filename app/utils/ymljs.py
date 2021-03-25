import json
import yaml
from pathlib import Path


class Reader(object):

    def __init__(self, file=None):
        self.file = file
        self.data = dict()

    def read(self, file=None):
        file = file or self.file
        endtype = str(file).split('.')[-1]
        parser = {
            'json': self.readjs,
            'yml': self.readyml,
            'yaml': self.readyml,
        }
        self.data = parser[endtype](file)
        return self.data

    @staticmethod
    def readjs(file):
        with open(file, mode='rt', encoding='utf-8') as f:
            data = json.load(f)
        return data

    @staticmethod
    def readyml(file):
        with open(Path(file), 'rt', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return data


class Writer(object):

    def __init__(self, data=None, file=None):
        self.file = file
        self.data = data

    def write(self, data=None, file=None):
        file = file or self.file
        data = data or self.data
        endtype = str(file).split('.')[-1]
        parser = {
            'json': self.writejs,
            'yml': self.writeyml,
            'yaml': self.writeyml,
        }
        parser[endtype](data, file)

    @staticmethod
    def writejs(data, file):
        with open(Path(file), 'w') as f:
            # f.write(json.dump(data))
            json.dump(data, f)

    @staticmethod
    def writeyml(data, file):
        with open(Path(file), 'w') as f:
            # f.write(yaml.dump(data))
            yaml.dump(data, f)


class Converter(object):

    def __init__(self):
        self.writer = Writer()
        self.reader = Reader()

    def dict2yml(self, source, destination):
        if not isinstance(source, dict):
            raise Exception('Unexpected source data: Not \'dict\' instance')
        if not str(destination).endswith('.yml') and not str(destination).endswith('.yaml'):
            raise Exception('Unexpected target file: {}'.format(destination))
        self.writer.write(source, destination)

    def dict2json(self, source, destination):
        if not isinstance(source, dict):
            raise Exception('Unexpected source data: Not \'dict\' instance')
        if not str(destination).endswith('.json'):
            raise Exception('Unexpected target file: {}'.format(destination))
        self.writer.write(source, destination)

    def json2yml(self, source, destination):
        if not str(source).endswith('.json'):
            raise Exception('Unexpected source file: {}'.format(source))
        if not str(destination).endswith('.yml') and not str(destination).endswith('.yaml'):
            raise Exception('Unexpected target file: {}'.format(destination))
        self.writer.write(self.reader.read(source), destination)

    def yml2json(self, source, destination):
        if not str(source).endswith('.yml') and not str(source).endswith('.yaml'):
            raise Exception('Unexpected source file: {}'.format(source))
        if not str(destination).endswith('.json'):
            raise Exception('Unexpected target file: {}'.format(source))
        self.writer.write(self.reader.read(source), destination)


reader = Reader()
