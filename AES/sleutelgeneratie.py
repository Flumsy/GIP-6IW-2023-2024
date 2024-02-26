import secrets

def genereer_sleutel():
    sleutel = []
    for i in range(1, 5):
        rij = []
        for j in range(1, 5):
            byte = secrets.randbits(8)
            byte |= (1 << 7)
            rij.append(byte)
        sleutel.append(rij)
    return sleutel

def sleutel_opslagen(naam, sleutel):
    with open(naam, 'wb') as file:
        for rij in sleutel:
            for byte in rij:
                file.write(byte.to_bytes(1, byteorder='big'))

sleutel = genereer_sleutel()
sleutel_opslagen('AES/geheime_sleutel.bin', sleutel)
