import os

from flask import Flask, render_template

from sqlalchemy import create_engine

from models import Base

ROOTDIR = os.path.dirname(os.path.abspath(__file__))

engine = create_engine(f'sqlite:///{ROOTDIR}/dev_qr.db',
    echo=False)

Base.metadata.create_all(engine)  

app = Flask(__name__)

@app.route('/') 
def index() -> str: 
    return render_template('index.html')

@app.route('/device/<id>') 
def device(id) -> str: 
    return render_template('device.html')
 
app.run()