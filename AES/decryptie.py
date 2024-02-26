import base64
from AES_functies import AddRoundKey, lees_sleutel, sleutel_uitbreiding, gf_vermenigvuldiging, transponeer

inv_S_BOX = [
    0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
    0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
    0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
    0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
    0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
    0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
    0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
    0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
    0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
    0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
    0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
    0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
    0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
    0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
    0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d
]

def lees_bericht(naam, blok_grootte=16):
    with open(naam, 'rb') as file:
        versleutelde_bytes = base64.b64decode(file.read())
    blokken = [versleutelde_bytes[i:i+blok_grootte] for i in range(0, len(versleutelde_bytes), blok_grootte)]

    blokken_als_getallen = [
        [list(blok[i:i+4]) for i in range(0, len(blok), 4)]
        for blok in blokken
    ]
    
    return blokken_als_getallen

def InvSubWord(woord): #Substitueerd elke byte in een woord met de bijhorende byte uit de inverse S-BOX
    return [inv_S_BOX[byte] for byte in woord]

def InvSubBytes(matrix): #Substitueerd elke byte in een blok met de bijhorende byte uit de inverse S-BOX
    nieuwe_matrix = [[0 for i in range(4)] for i in range(4)]
    for i in range(0, 4):
        nieuwe_matrix[i] = InvSubWord(matrix[i])
    return nieuwe_matrix

def InvShiftRows(matrix): #Verschuift elke rij in een blok met een bepaalde stap naar rechts
    nieuwe_matrix = [[0 for i in range(4)] for j in range(4)]
    for i in range(4):
        nieuwe_matrix[i][0] = matrix[i][0]
        nieuwe_matrix[i][1] = matrix[(i-1) % 4][1]
        nieuwe_matrix[i][2] = matrix[(i-2) % 4][2]
        nieuwe_matrix[i][3] = matrix[(i-3) % 4][3]
    return nieuwe_matrix

def InvMixColumns(matrix): #Matrix vermenigvuldiging (in GF(2^8)) tussen een blok en de InvMixColumns matrix
    matrix = transponeer(matrix)
    for i in range(4):
        kol = [matrix[j][i] for j in range(4)]
        matrix[0][i] = gf_vermenigvuldiging(kol[0], 0x0e) ^ gf_vermenigvuldiging(kol[1], 0x0b) ^ gf_vermenigvuldiging(kol[2], 0x0d) ^ gf_vermenigvuldiging(kol[3], 0x09)
        matrix[1][i] = gf_vermenigvuldiging(kol[0], 0x09) ^ gf_vermenigvuldiging(kol[1], 0x0e) ^ gf_vermenigvuldiging(kol[2], 0x0b) ^ gf_vermenigvuldiging(kol[3], 0x0d)
        matrix[2][i] = gf_vermenigvuldiging(kol[0], 0x0d) ^ gf_vermenigvuldiging(kol[1], 0x09) ^ gf_vermenigvuldiging(kol[2], 0x0e) ^ gf_vermenigvuldiging(kol[3], 0x0b)
        matrix[3][i] = gf_vermenigvuldiging(kol[0], 0x0b) ^ gf_vermenigvuldiging(kol[1], 0x0d) ^ gf_vermenigvuldiging(kol[2], 0x09) ^ gf_vermenigvuldiging(kol[3], 0x0e)
    matrix = transponeer(matrix)
    return matrix

def ontsleutel(blokken, sleutel):
    sleutels = sleutel_uitbreiding(sleutel)

    for i in range(1, len(sleutels) - 1):
        sleutels[i] = InvMixColumns(sleutels[i]) #InvMixColumns toepassen op sleutels om decryptie sleutels te krijgen

    ontsleutelde_blokken = []

    for blok in blokken:
        huidig_blok = blok

        # print(f'round[ 0].iinput ' + blok_naar_hex(huidig_blok))
        # print(f'round[ 0].ik_sch ' + blok_naar_hex(sleutels[10]))

        huidig_blok = AddRoundKey(huidig_blok, sleutels[10]) #AddRoundKey tussen de blok en de n-de sleutel

        for ronde in range(1, 10): #Decryptierondes
            # print(f'round[ {ronde}].istart ' + blok_naar_hex(huidig_blok))

            huidig_blok = InvSubBytes(huidig_blok)
            # print(f'round[ {ronde}].is_box ' + blok_naar_hex(huidig_blok))

            huidig_blok = InvShiftRows(huidig_blok)
            # print(f'round[ {ronde}].is_row ' + blok_naar_hex(huidig_blok))

            huidig_blok = InvMixColumns(huidig_blok)
            # print(f'round[ {ronde}].im_col ' + blok_naar_hex(huidig_blok))

            huidig_blok = AddRoundKey(huidig_blok, sleutels[len(sleutels)-1-ronde])

            # print(f'round[ {ronde}].ik_sch ' + blok_naar_hex(sleutels[len(sleutels)-1-ronde]))

        huidig_blok = InvSubBytes(huidig_blok)
        # print(f'round[ {10}].is_box ' + blok_naar_hex(huidig_blok))

        huidig_blok = InvShiftRows(huidig_blok)
        # print(f'round[ {10}].is_row ' + blok_naar_hex(huidig_blok))

        # print(f'round[ {10}].ik_sch ' + blok_naar_hex(sleutels[0]))

        huidig_blok = AddRoundKey(huidig_blok, sleutels[0]) #AddRoundKey tussen de blok en de initiele sleutel

        # print(f'round[ {10}].ioutput ' + blok_naar_hex(huidig_blok))

        ontsleutelde_blokken.append(huidig_blok)

    return ontsleutelde_blokken

def blokken_naar_bytes(blokken): #Alle bytes uit de blokken in 1 lijst plaatsen
    bytes_lijst = [byte for blok in blokken for rij in blok for byte in rij]
    return bytes(bytes_lijst)

def verwijder_padding(ontsleutelde_bytes):
    laatste_byte = ontsleutelde_bytes[-1] #[-1] laatste element in lijst
    if 0 < laatste_byte <= 16:  #PKCS#7 padding grootte nakijken (tussen 1 en 16 bytes = mogelijke padding)
        padding_grootte = laatste_byte
        for i in range(1, padding_grootte):
            if ontsleutelde_bytes[-1 - i] != laatste_byte:
                return ontsleutelde_bytes  #Geen geldige padding
        return ontsleutelde_bytes[:-padding_grootte]  #Verwijder padding
    return ontsleutelde_bytes  #Geen padding gevonden

def ontsleutelde_blokken_naar_tekst(ontsleutelde_blokken):
    ontsleutelde_bytes = blokken_naar_bytes(ontsleutelde_blokken)
    ontsleutelde_bytes_zonder_padding = verwijder_padding(ontsleutelde_bytes)
    return ontsleutelde_bytes_zonder_padding.decode('utf-8') #Bytes omzetting in letters

def hex_sleutel_naar_matrix(hex_sleutel):
    bytes_sleutel = bytes.fromhex(hex_sleutel)
    return [list(bytes_sleutel[i:i+4]) for i in range(0, 16, 4)]

def blok_naar_hex(blok):
    hex_b = ''.join(format(byte, '02x') for woord in blok for byte in woord)
    return hex_b

def print_matrix(matrix):
    for row in matrix:
        row_str = ", ".join(f"{elem:4}" for elem in row)
        print(f"[{row_str}]")
    print('------------------------------')

def print_matrix_hex(matrix):
    for row in matrix:
        row_str = ", ".join(f"{format(elem, '02x'):4}" for elem in row)
        print(f"[{row_str}]")
    print('------------------------------')

originele_sleutel = lees_sleutel('AES/geheime_sleutel.bin')
blokken = lees_bericht('AES/bericht.txt')

print(ontsleutelde_blokken_naar_tekst(ontsleutel(blokken, originele_sleutel)))

# cipher = hex_sleutel_naar_matrix('69c4e0d86a7b0430d8cdb78070b4c55a')
# sleutel = hex_sleutel_naar_matrix('000102030405060708090a0b0c0d0e0f')
# blokken = [[[105, 196, 224, 216], [106, 123, 4, 48], [216, 205, 183, 128], [112, 180, 197, 90]]]

# ontsleutel(blokken, sleutel)