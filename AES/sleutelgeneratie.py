import math
import secrets
import base64

def genereer_sleutel():
    sleutel = secrets.randbits(128)
    sleutel |= (1 << 127)
    sleutel = sleutel.to_bytes(math.ceil(sleutel.bit_length() / 8), byteorder='big')

    return sleutel

def sleutel_opslagen(naam, sleutel):
    with open(naam, 'w') as file:
        sleutel_base64 = base64.b64encode(sleutel).decode()
        file.write(sleutel_base64)

sleutel = genereer_sleutel()
sleutel_opslagen('AES/geheime_sleutel.txt', sleutel)
