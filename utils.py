import os
from copy import copy

import qrcode
from flask import url_for 

from context import Context


c = Context()

def generate_qr(device_id):
    link = url_for('device_info', _external=True, id=device_id)

    dir_path = os.path.join('static', 'qr_codes')
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    filename = os.path.join(dir_path, f'qr__{device_id}.png')
    if not os.path.exists(filename):
        img = qrcode.make(link)
        img.save(filename)

    return url_for('static', filename=os.path.join(f'qr_codes/qr__{device_id}.png'))

def to_dict(device):
    ret = []
    for field in c.fields_maps['fields']:
        ret_dict = copy(field)
        val = getattr(device, ret_dict['name'])
        try:
            ret_dict['value'] = val.name
        except AttributeError:
            ret_dict['value'] = val or ''
        if field['layout'] == 'select':
            ret_dict['data'] = getattr(c, field['source'].lower())

        ret.append(ret_dict)

    return ret

        
