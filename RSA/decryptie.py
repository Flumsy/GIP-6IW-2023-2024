import base64
import math
from RSA_functies import ontsleutel

def lees_geheime_sleutel(naam):
    with open(naam, 'rb') as file:
        n_grootte = int.from_bytes(file.read(4), byteorder='big')
        n = int.from_bytes(file.read(n_grootte), byteorder='big')

        d_grootte = int.from_bytes(file.read(4), byteorder='big')
        d = int.from_bytes(file.read(d_grootte), byteorder='big')

    return (n, d, n_grootte)

def lees_bericht(naam, n_grootte):
    # Lees en decodeer de Base64-gecodeerde data
    with open(naam, 'rb') as file:
        base64_encoded_data = file.read()
    versleutelde_bytes = base64.b64decode(base64_encoded_data)
    
    # Splits de bytes in integers gebaseerd op de grootte van n
    bericht_integers = []
    for i in range(0, len(versleutelde_bytes), n_grootte):
        blok = versleutelde_bytes[i:i+n_grootte]
        bericht_integers.append(int.from_bytes(blok, byteorder='big'))
    
    return bericht_integers

sleutel = lees_geheime_sleutel('RSA/geheime_sleutel.bin')
versleuteld_bericht = lees_bericht('RSA/bericht.txt', sleutel[2])

print(ontsleutel(versleuteld_bericht, sleutel[0], sleutel[1]))