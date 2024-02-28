import os

from flask import Flask, render_template

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Devices

ROOTDIR = os.path.dirname(os.path.abspath(__file__))

engine = create_engine(f'sqlite:///{ROOTDIR}/dev_qr.db',
    echo=False)

Base.metadata.create_all(engine) 

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
    return render_template('device.html', dev_dict=device.to_dict())
 
app.run()