import math
import secrets
import base64

from AES.AES_functies import sleutel_pad

def genereer_sleutel():
    sleutel = secrets.randbits(128)
    sleutel |= (1 << 127)
    sleutel = sleutel.to_bytes(math.ceil(sleutel.bit_length() / 8), byteorder='big')
    
    with open(sleutel_pad, 'w') as file:
        sleutel_base64 = base64.b64encode(sleutel).decode()
        file.write(sleutel_base64)

    print('-------------------------------')
    print(f'\nGeheime sleutel\n{sleutel_base64}\n-----------------------------------------------------')
    print(f'Geheime sleutel opgeslagen naar: {sleutel_pad}\n')
