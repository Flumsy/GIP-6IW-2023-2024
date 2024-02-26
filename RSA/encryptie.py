import base64
import math
from RSA_functies import versleutel

def lees_publieke_sleutel(naam):
    with open(naam, 'rb') as file:
        n_grootte = int.from_bytes(file.read(4), byteorder='big')
        n = int.from_bytes(file.read(n_grootte), byteorder='big')

        e_grootte = int.from_bytes(file.read(4), byteorder='big')
        e = int.from_bytes(file.read(e_grootte), byteorder='big')

    return (n, e)

def opslagen_versleuteld_bericht(naam, bericht, n, e):
    versleuteld_bericht = versleutel(bericht, n, e)
    n_grootte = math.ceil(n.bit_length() / 8)
    versleutelde_bytes = b''.join(int.to_bytes(getal, n_grootte, byteorder='big') for getal in versleuteld_bericht)
    base64_encoded = base64.b64encode(versleutelde_bytes)

    with open(naam, 'wb') as file:
        file.write(base64_encoded)

bericht = '''
    Brylan Bristopher Woods - 175.35.188.56
    Israel Chaves - 174.57.138.172
    Gustavo Alves - 52.9.202.244
    Fabio Di Nota - 255.255.255.0
    Thomas Vatthis - 192.54.219.179
    Charles Hoskinson - 0x40b38765696e3d5d8d9d834d8aad4bb6e418e489 - 91.137.57.7
    Joao Aribal - 106.72.177.15
    Finn Davies - 191.193.101.209
    Jayden Marthinez - 150.199.206.10
    Ruben Sitku - 0.91.60.193
    Alex Smith - 48.154.205.127
    Spencer Dan - 76.26.7.146
'''
sleutel = lees_publieke_sleutel('RSA/publieke_sleutel.bin')
opslagen_versleuteld_bericht('RSA/bericht.txt', bericht, sleutel[0], sleutel[1])