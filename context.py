import os
import yaml

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from abstracts import Singleton

ROOTDIR = os.path.dirname(os.path.abspath(__file__))

class Context(Singleton):
    def __init__(self):
        self.engine = create_engine(f'sqlite:///{ROOTDIR}/dev_qr.db',
    echo=False)
        self.session = sessionmaker(bind=self.engine)()

        self._fields_maps = None
        self._devtypes = []
        self._ctypes = []

        self._init_fields_maps()

    def _init_fields_maps(self):
        with open('fields_map.yml', encoding='utf-8') as fh:
           self._fields_maps = yaml.load(fh, Loader=yaml.FullLoader)

    @property
    def fields_maps(self):
        return self._fields_maps
    
    @property
    def devtypes(self):
        if not self._devtypes:
            from models import DevTypes
            self._devtypes = self.session.query(DevTypes).order_by(DevTypes.id).all()

        return self._devtypes
    
    @property
    def ctypes(self):
        if not self._ctypes:
            from models import CTypes

            self._ctypes = self.session.query(CTypes).order_by(CTypes.id).all()

        return self._ctypes