import yaml

from abstracts import Singleton

class Context(Singleton):
    def __init__(self):
        self._fields_maps = None

        self._init_fields_maps()

    def _init_fields_maps(self):
        with open('fields_map.yml', encoding='utf-8') as fh:
           self._fields_maps = yaml.load(fh, Loader=yaml.FullLoader)

    @property
    def fields_maps(self):
        return self._fields_maps