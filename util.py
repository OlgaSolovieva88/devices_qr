import qrcode


def generate_qr(data):
    img = qrcode.make(data)
    outfile_name = data['label'] + '.png'

    img.save(outfile_name)
