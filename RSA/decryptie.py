import base64
import math
from RSA_functies import ontsleutel

def lees_geheime_sleutel(naam):
    with open(naam, 'r') as file:
        regels = file.readlines()

        n_base64 = regels[0].strip()
        d_base64 = regels[1].strip()

        n = int.from_bytes(base64.b64decode(n_base64), byteorder='big')
        d = int.from_bytes(base64.b64decode(d_base64), byteorder='big')

    return (n, d)

def lees_bericht(naam, n):
    with open(naam, 'rb') as file:
        base64_encoded_data = file.read()
    versleutelde_bytes = base64.b64decode(base64_encoded_data)
    
    n_grootte = math.ceil(n.bit_length() / 8)

    bericht_integers = []
    for i in range(0, len(versleutelde_bytes), n_grootte):
        blok = versleutelde_bytes[i:i+n_grootte]
        bericht_integers.append(int.from_bytes(blok, byteorder='big'))
    
    return bericht_integers

sleutel = lees_geheime_sleutel('RSA/geheime_sleutel.txt')
versleuteld_bericht = lees_bericht('RSA/bericht.txt', sleutel[0])
print(versleuteld_bericht)
print(ontsleutel(versleuteld_bericht, sleutel[0], sleutel[1]))