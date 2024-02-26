import base64
from AES_functies import AddRoundKey, lees_sleutel, SubWord, gf_vermenigvuldiging, sleutel_uitbreiding, transponeer

def bericht_opvulling(bericht):
    bytes_nodig = 16 - (len(bericht) % 16)
    opvulling = bytes([bytes_nodig] * bytes_nodig)
    return bericht + opvulling

def splitsen_in_blokken(bericht, blok_grootte = 16):
    return [bericht[i:i+blok_grootte] for i in range(0, len(bericht), blok_grootte)]

def SubBytes(matrix): #Substitueerd elke byte in een blok met de bijhorende byte uit de S-BOX
    nieuwe_matrix = [[0 for i in range(4)] for i in range(4)]
    for i in range(0, 4):
        nieuwe_matrix[i] = SubWord(matrix[i])
    return nieuwe_matrix

def ShiftRows(matrix): #Verschuift elke rij in een blok met een bepaalde stap naar links
    nieuwe_matrix = [[0 for i in range(4)] for i in range(4)]
    for i in range(0, 4):
        nieuwe_matrix[i][0] = matrix[i][0]
        nieuwe_matrix[i][1] = matrix[(i+1) % 4][1]
        nieuwe_matrix[i][2] = matrix[(i+2) % 4][2]
        nieuwe_matrix[i][3] = matrix[(i+3) % 4][3]
    return(nieuwe_matrix)

def MixColumns(matrix): #Matrix vermenigvuldiging (in GF(2^8)) tussen een blok en de MixColumns matrix
    matrix = transponeer(matrix)
    for i in range(4):
        kol = [matrix[j][i] for j in range(4)]
        matrix[0][i] = gf_vermenigvuldiging(kol[0], 2) ^ gf_vermenigvuldiging(kol[1], 3) ^ gf_vermenigvuldiging(kol[2], 1) ^ gf_vermenigvuldiging(kol[3], 1)
        matrix[1][i] = gf_vermenigvuldiging(kol[0], 1) ^ gf_vermenigvuldiging(kol[1], 2) ^ gf_vermenigvuldiging(kol[2], 3) ^ gf_vermenigvuldiging(kol[3], 1)
        matrix[2][i] = gf_vermenigvuldiging(kol[0], 1) ^ gf_vermenigvuldiging(kol[1], 1) ^ gf_vermenigvuldiging(kol[2], 2) ^ gf_vermenigvuldiging(kol[3], 3)
        matrix[3][i] = gf_vermenigvuldiging(kol[0], 3) ^ gf_vermenigvuldiging(kol[1], 1) ^ gf_vermenigvuldiging(kol[2], 1) ^ gf_vermenigvuldiging(kol[3], 2)
    matrix = transponeer(matrix)
    return matrix

def versleutel(bericht, sleutel):
    sleutels = sleutel_uitbreiding(sleutel)
    bericht_bytes = bericht.encode('utf-8') #Zet elke letter om in bytes
    blokken = [[list(blok[i:i+4]) for i in range(0, len(blok), 4)] for blok in splitsen_in_blokken(bericht_opvulling(bericht_bytes))] #1. Vult bericht op om een veelvoud van 16 bytes te krijgen. 2. Splitst bytes op in blokken van 16 bytes. 3. Splitst elk blok op in 4 woorden. 4. Splitst elk woord op in 4 bytes.
    versleutelde_blokken = []
    
    for blok in blokken:
        huidig_blok = blok
        # print('round[ 0].input ' + blok_naar_hex(huidig_blok))
        # print('round[ 0].k_sch ' + blok_naar_hex(sleutel))
        huidig_blok = AddRoundKey(huidig_blok, sleutels[0]) #AddRoundKey tussen de blok en de initiele sleutel

        for ronde in range(1, 10): #Encryptierondes
            # print(f'round[ {ronde}].start ' + blok_naar_hex(huidig_blok))

            huidig_blok = SubBytes(huidig_blok)
            # print(f'round[ {ronde}].s_box ' + blok_naar_hex(huidig_blok))

            huidig_blok = ShiftRows(huidig_blok)
            # print(f'round[ {ronde}].s_row ' + blok_naar_hex(huidig_blok))

            huidig_blok = MixColumns(huidig_blok)
            # print(f'round[ {ronde}].m_col ' + blok_naar_hex(huidig_blok))
            
            huidig_blok = AddRoundKey(huidig_blok, sleutels[ronde])
            # print(f'round[ {ronde}].k_sch ' + blok_naar_hex(sleutels[ronde]))

        # print(f'round[ {10}].start ' + blok_naar_hex(huidig_blok))

        huidig_blok = SubBytes(huidig_blok)
        # print(f'round[ {10}].s_box ' + blok_naar_hex(huidig_blok))

        huidig_blok = ShiftRows(huidig_blok)
        # print(f'round[ {10}].s_row ' + blok_naar_hex(huidig_blok))

        huidig_blok = AddRoundKey(huidig_blok, sleutels[10]) #AddRoundKey tussen de blok en n-de sleutel
        # print(f'round[ {10}].k_sch ' + blok_naar_hex(sleutels[10]))

        versleutelde_blokken.append(huidig_blok)
        # print(f'round[ {10}].output ' + blok_naar_hex(huidig_blok))
    return versleutelde_blokken

def opslagen_versleuteld_bericht(naam, versleutelde_blokken):
    versleutelde_bytes = b''.join(byte.to_bytes(1, byteorder='big') for blok in versleutelde_blokken for rij in blok for byte in rij)
    base64_gecodeerd = base64.b64encode(versleutelde_bytes)

    with open(naam, 'wb') as file:
        file.write(base64_gecodeerd)

def hex_naar_matrix(hex_sleutel):
    bytes_sleutel = bytes.fromhex(hex_sleutel)
    return [list(bytes_sleutel[i:i+4]) for i in range(0, 16, 4)]

def blok_naar_hex(blok):
    hex_b = ''.join(format(byte, '02x') for woord in blok for byte in woord)
    return hex_b

originele_sleutel = lees_sleutel('AES/geheime_sleutel.bin')
bericht = '''
    Brylan Bristopher Woods - 175.35.188.56
    Israel Chaves - 174.57.138.172
    Gustavo Alves - 52.9.202.244
    Fabio Di Nota - 255.255.255.0
    Thomas Vatthis - 192.54.219.179
    Charles Hoskinson - 0x40b38765696e3d5d8d9d834d8aad4bb6e418e489 - 91.137.57.7
    Joao Aribal - 106.72.177.15
    Finn Davies - 191.193.101.209
    Jayden Marthinez - 150.199.206.10
    Ruben Sitku - 0.91.60.193
    Alex Smith - 48.154.205.127
    Spencer Dan - 76.26.7.146
'''

opslagen_versleuteld_bericht('AES/bericht.txt', versleutel(bericht, originele_sleutel))

# sleutel = hex_naar_matrix('000102030405060708090a0b0c0d0e0f')
# tekst = hex_naar_matrix('00112233445566778899aabbccddeeff')
# blokken = [[[0, 17, 34, 51], [68, 85, 102, 119], [136, 153, 170, 187], [204, 221, 238, 255]]]

# versleutel(blokken, sleutel)

