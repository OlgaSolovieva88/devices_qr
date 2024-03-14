import os

from flask import Flask, render_template

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from context import Context
from models import Base, Devices
from utils import to_dict

ROOTDIR = os.path.dirname(os.path.abspath(__file__))

engine = create_engine(f'sqlite:///{ROOTDIR}/dev_qr.db',
    echo=False)

Base.metadata.create_all(engine) 

c = Context()

Session = sessionmaker(bind=engine)
session = Session()
app = Flask(__name__)

@app.route('/') 
def index() -> str: 
    devices = session.query(Devices).all()
    return render_template('index.html', devices=devices)

@app.route('/device/<id>') 
def device(id) -> str:
    device = session.query(Devices).filter_by(id=id).first()
    
    return render_template('device.html', dev_dict=to_dict(device), label=device.label, qr=device.qr)

@app.route('/device_info/<id>') 
def device_info(id) -> str:
    device = session.query(Devices).filter_by(id=id).first()
    return render_template('device_info.html', device=device)
 
app.run(host='0.0.0.0')