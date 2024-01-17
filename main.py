import json

from util import generate_qr


filename = "devices.json"
with open(filename) as fcc_file:
    fcc_data = json.load(fcc_file)

print(fcc_data)

for A in fcc_data:
    print(A)
    generate_qr(A)
