import math
from RSA_functies import willekeurig_priem_1024_bit_getal, vind_d

def sleutel_opslagen(naam, sleutel):
    n, onderdeel = sleutel #Sleutel bestaat uit (n, e) of (n, d)

    n_grootte = math.ceil(n.bit_length() / 8)
    onderdeel_grootte = math.ceil(n.bit_length() / 8)

    with open(naam, 'wb') as file:
        file.write(n_grootte.to_bytes(4, byteorder='big'))        
        file.write(n.to_bytes(n_grootte, byteorder='big'))
        file.write(onderdeel_grootte.to_bytes(4, byteorder='big'))
        file.write(onderdeel.to_bytes(onderdeel_grootte, byteorder='big'))

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

sleutel_opslagen('RSA/publieke_sleutel.bin', publieke_sleutel)
sleutel_opslagen('RSA/geheime_sleutel.bin', geheime_sleutel)