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

def can_show(obj, data_list):
    def recursive_get_data(obj, path_list):
        if len(path_list) == 1:
            return getattr(obj, path_list[0])
        
        obj = getattr(obj, path_list[0])
        if not obj:
            return ''
        return recursive_get_data(obj, path_list[1:])

    def calculate(op, val1, val2):
        if op == 'in' and val1 and val2:
            return val1 in val2    

        # чтобы отобразить все поля в новом объете
        return True

    if not data_list:
        return True
    
    for conds_dict in data_list:
        attr = recursive_get_data(obj, conds_dict['attr'].split('.'))
        res = calculate(conds_dict['op'], attr, conds_dict['data'])
        if not res:
            return
        
    return True

def to_dict(device):
    ret = []
    for field in c.fields_maps['fields']:
        if not can_show(device, field.get('show', [])):
            continue

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

        
