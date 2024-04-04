from flask import Flask, render_template, request, redirect, url_for

from context import Context
from models import Base, Devices
from utils import to_dict


c = Context()
Base.metadata.create_all(c.engine) 

app = Flask(__name__)

@app.route('/') 
def index() -> str: 
    devices = c.session.query(Devices).all()
    return render_template('index.html', devices=devices)

@app.route('/device/<id>', methods=['post', 'get']) 
def device(id) -> str:
    device = c.session.query(Devices).filter_by(id=id).first()
    
    if request.method == 'POST':
        for k, v in request.form.items():
            setattr(device, k, v)

            c.session.commit()

    return render_template('device.html', dev_dict=to_dict(device), dev_id=device.id, label=device.label, qr=device.qr)

@app.route('/add_device')
def add_device():
    """Добавление нового прибора
        Созается объект прибора, сохраняется в БД, отображается через /device/<id>
    """
    device = Devices()
    c.session.add(device)
    c.session.commit()

    return render_template('device.html', dev_dict=to_dict(device), dev_id=device.id, label=device.label, qr=device.qr)

@app.route('/delete_device/<id>')
def delete_device(id):
    c.session.query(Devices).filter(Devices.id==id).delete()
    c.session.commit()

    return redirect(url_for('index'), code=302)

@app.route('/device_info/<id>') 
def device_info(id) -> str:
    device = c.session.query(Devices).filter_by(id=id).first()
    return render_template('device_info.html', device=device)
 
app.run(host='0.0.0.0')