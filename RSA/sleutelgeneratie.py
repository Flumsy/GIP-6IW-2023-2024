import base64
import math

from .RSA_functies import willekeurig_priem_1024_bit_getal, vind_d

def sleutel_opslagen(naam, sleutel):
    n, onderdeel = sleutel #Sleutel bestaat uit (n, e) of (n, d)

    n_base64 = base64.b64encode(n.to_bytes(math.ceil(n.bit_length() / 8), byteorder='big')).decode()
    onderdeel_base64 = base64.b64encode(onderdeel.to_bytes(math.ceil(onderdeel.bit_length() / 8), byteorder='big')).decode()

    with open(naam, 'w') as file:
        file.write(f'{n_base64}\n{onderdeel_base64}\n')

def genereer_sleutel():
    p = willekeurig_priem_1024_bit_getal()
    q = willekeurig_priem_1024_bit_getal()

    while(q == p):
        q = willekeurig_priem_1024_bit_getal()

    n = p*q
    phi_n = (p-1)*(q-1)
    e = 65537
    d = vind_d(e, phi_n)

    publieke_sleutel = (n, e)
    geheime_sleutel = (n, d)

    sleutel_opslagen('RSA/publieke_sleutel.txt', publieke_sleutel)
    sleutel_opslagen('RSA/geheime_sleutel.txt', geheime_sleutel)

    print('')
    print('    Publieke sleutel opgeslagen naar: RSA/publieke_sleutel.txt')
    print('    Geheime sleutel opgeslagen naar: RSA/geheime_sleutel.txt')