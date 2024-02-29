import base64
import math
import os

import RSA.RSA_functies as RSA

def lees_publieke_sleutel():
    if(os.path.exists(RSA.publieke_sleutel_pad)):
        with open(RSA.publieke_sleutel_pad, 'r') as file:
            regels = file.readlines()

            n_base64 = regels[0].strip()
            e_base64 = regels[1].strip()

            n = int.from_bytes(base64.b64decode(n_base64), byteorder='big')
            e = int.from_bytes(base64.b64decode(e_base64), byteorder='big')

        return (n, e)
    else:
        return 'geen sleutel'

def opslagen_versleuteld_bericht(naam, bericht, n, e):
    versleuteld_bericht = RSA.versleutel(bericht, n, e)
    n_grootte = math.ceil(n.bit_length() / 8)
    versleutelde_bytes = b''.join(int.to_bytes(getal, n_grootte, byteorder='big') for getal in versleuteld_bericht)
    base64_gecodeerd = base64.b64encode(versleutelde_bytes)

    with open(naam, 'wb') as file:
        file.write(base64_gecodeerd)

    print('\n-------------------------------')
    print(f'\nVersleuteld bericht\n{base64_gecodeerd.decode()}\n-----------------------------------------------------')
    print(f'Versleuteld bericht opgeslagen naar: {RSA.berichten_pad}\n')

def encryptie(bericht):
    sleutel = lees_publieke_sleutel()
    if sleutel != 'geen sleutel':
        opslagen_versleuteld_bericht(RSA.berichten_pad, bericht, sleutel[0], sleutel[1])
    else:
        print('\n-------------------------------')
        print('\nGeen RSA publieke sleutel gevonden.\n')