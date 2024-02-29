import base64
import math
import os

import RSA.RSA_functies as RSA

def naar_base64(getal):
    return base64.b64encode(getal.to_bytes(math.ceil(getal.bit_length() / 8), byteorder='big')).decode()

def sleutel_opslagen(naam, sleutel):
    n, onderdeel = sleutel #Sleutel bestaat uit (n, e) of (n, d)

    n_base64 = naar_base64(n)
    onderdeel_base64 = naar_base64(onderdeel)

    with open(naam, 'w') as file:
        file.write(f'{n_base64}\n{onderdeel_base64}\n')

def genereer_sleutel():
    p = RSA.willekeurig_priem_1024_bit_getal()
    q = RSA.willekeurig_priem_1024_bit_getal()

    while(q == p):
        q = RSA.willekeurig_priem_1024_bit_getal()

    n = p*q
    phi_n = (p-1)*(q-1)
    e = 65537
    d = RSA.vind_d(e, phi_n)

    publieke_sleutel = (n, e)
    geheime_sleutel = (n, d)

    sleutel_opslagen(RSA.publieke_sleutel_pad, publieke_sleutel)
    sleutel_opslagen(RSA.geheime_sleutel_pad, geheime_sleutel)

    print('-------------------------------')
    print(f'\nPublieke sleutel\n{naar_base64(publieke_sleutel[0])}\n{naar_base64(publieke_sleutel[1])}\n-----------------------------------------------------')
    print(f'Geheime sleutel\n{naar_base64(geheime_sleutel[0])}\n{naar_base64(geheime_sleutel[1])}\n-----------------------------------------------------')
    print(f'Publieke sleutel opgeslagen naar: {RSA.publieke_sleutel_pad}')
    print(f'Geheime sleutel opgeslagen naar: {RSA.geheime_sleutel_pad}\n')