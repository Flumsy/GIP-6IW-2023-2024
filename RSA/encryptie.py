import base64
import math
from RSA_functies import versleutel

def lees_publieke_sleutel(naam):
    with open(naam, 'r') as file:
        regels = file.readlines()

        n_base64 = regels[0].strip()
        e_base64 = regels[1].strip()

        n = int.from_bytes(base64.b64decode(n_base64), byteorder='big')
        e = int.from_bytes(base64.b64decode(e_base64), byteorder='big')

    return (n, e)

def opslagen_versleuteld_bericht(naam, bericht, n, e):
    versleuteld_bericht = versleutel(bericht, n, e)
    n_grootte = math.ceil(n.bit_length() / 8)
    versleutelde_bytes = b''.join(int.to_bytes(getal, n_grootte, byteorder='big') for getal in versleuteld_bericht)
    base64_encoded = base64.b64encode(versleutelde_bytes)

    with open(naam, 'wb') as file:
        file.write(base64_encoded)

bericht = '''boingboingboingboing'''
sleutel = lees_publieke_sleutel('RSA/publieke_sleutel.txt')
opslagen_versleuteld_bericht('RSA/bericht.txt', bericht, sleutel[0], sleutel[1])