import base64
import math
import os

import RSA.RSA_functies as RSA

def lees_geheime_sleutel():
    if(os.path.exists(RSA.geheime_sleutel_pad)):
        with open(RSA.geheime_sleutel_pad, 'r') as file:
            regels = file.readlines()

        n_base64 = regels[0].strip()
        d_base64 = regels[1].strip()

        n = int.from_bytes(base64.b64decode(n_base64), byteorder='big')
        d = int.from_bytes(base64.b64decode(d_base64), byteorder='big')

        return (n, d)
    else:
        return 'geen sleutel'

def lees_bericht(n):
    if(os.path.exists(RSA.berichten_pad)):
        with open(RSA.berichten_pad, 'rb') as file:
            base64_encoded_data = file.read()
        versleutelde_bytes = base64.b64decode(base64_encoded_data)
        
        n_grootte = math.ceil(n.bit_length() / 8)

        bericht_integers = []
        for i in range(0, len(versleutelde_bytes), n_grootte):
            blok = versleutelde_bytes[i:i+n_grootte]
            bericht_integers.append(int.from_bytes(blok, byteorder='big'))
        
        return bericht_integers
    else:
        return 'geen bericht'

def decryptie():
    sleutel = lees_geheime_sleutel()
    if sleutel != 'geen sleutel':
        versleuteld_bericht = lees_bericht(sleutel[0])
        if versleuteld_bericht != 'geen bericht':
            print(f'Ontsleuteld bericht\n{RSA.ontsleutel(versleuteld_bericht, sleutel[0], sleutel[1])}\n')
        else:
            print('Geen bericht gevonden.\n')
    else:
        print('Geen RSA geheime sleutel gevonden.\n')