import json
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

ROOTDIR = os.path.dirname(os.path.abspath(__file__))

engine = create_engine(f'sqlite:///{ROOTDIR}/dev_qr.db',
    echo=False)

Base.metadata.create_all(engine) 

Session = sessionmaker(bind=engine)
session = Session()

from models import DevTypes, CTypes, Devices


with open('C_type.json', encoding='utf-8') as json_file:
    data = json.load(json_file)
    for p in data:
        c_type = CTypes(**p)
        session.add(c_type)
        session.commit()

types = session.query(CTypes).all()
print(types)
print('----------------------------------')

with open('dev_type.json', encoding='utf-8') as json_file:
    data = json.load(json_file)
    for p in data:
        dev_type = DevTypes(**p)
        session.add(dev_type)
        session.commit()


types = session.query(DevTypes).all()
print(types)
print('----------------------------------')

with open('devices.json', encoding='utf-8') as json_file:
    data = json.load(json_file)
    for p in data:
        c_type = session.query(CTypes).filter_by(name=p['c_type']).first()
        dev_type = session.query(DevTypes).filter_by(name=p['dev_type']).first()
        p['dev_type'] = dev_type
        p['c_type'] = c_type
        devices = Devices(**p)
        session.add(devices)
        session.commit()

devs = session.query(Devices).all()
print(devs)
print('----------------------------------')