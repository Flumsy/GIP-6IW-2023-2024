import base64
import math
from random import randint
import secrets
import hashlib
import os
import sys

sleutels_folder = os.path.join(os.path.dirname(__file__), '..', 'Sleutels')

if not os.path.exists(sleutels_folder):
    os.makedirs(sleutels_folder)

sleutel_pad = os.path.abspath(os.path.join(sleutels_folder, 'AES_geheime_sleutel.txt'))

def naar_binair(getal):
    binairGetal = []

    if getal == 0:
        binairGetal.insert(0, 0)
    else:
        while getal != 0:
            bit = getal % 2  # Modulus 2 om de rest van het getal / 2 te krijgen
            getal = getal // 2  # Getal delen door 2 voor volgende iteratie
            binairGetal.insert(0, bit)  # Bit (rest) opslagen in een lijst
    return binairGetal

def macht_mod(gndt, exp, mod):
    binair = naar_binair(exp)
    aantal_kwadraten = len(binair)
    resultaat = 1
    basis = gndt % mod
    for i in range(aantal_kwadraten - 1, -1, -1):
        if binair[i] == 1:
            resultaat = (resultaat * basis) % mod

        basis = (basis * basis) % mod
    
    return resultaat % mod

def willekeurig_1024_bit_getal():
    willekeurig_getal = secrets.randbits(1024)
    willekeurig_getal |= (1 << 1023) #Zorgen dat meest belangrijke bit 1 is zodat het getal uit 1024 bits bestaat
    willekeurig_getal |= 1 #Zorgen dat minst belangrijke bit 1 is zodat het getal oneven is
    return willekeurig_getal

def miller_rabin_test(getal, iteraties=40):
    if getal in [2, 3]: #2 en 3 zijn priem
        return True
    if getal % 2 == 0: #Even getallen buiten 2 zijn niet priem
        return False
    n = getal
    n_1 = (getal - 1)
    k = 0
    while (n_1 % 2 == 0):
        n_1 = n_1 // 2
        k += 1
    m = n_1
    for _ in range(iteraties):
        a = randint(2, (n - 2))
        b = macht_mod(a, m, n)
        if b != 1 and b != (n - 1):
            for _ in range(k - 1):
                b = (b * b) % n
                if b == (n - 1):
                    break
            else:
                return False #Samengesteld getal
    return True #Priem getal

def willekeurig_priem_1024_bit_getal():
    getal = willekeurig_1024_bit_getal()
    isPriem = miller_rabin_test(getal)
    while(isPriem == False):
        getal += 2
        isPriem = miller_rabin_test(getal)
    return getal

def genereer_sleutels(n, g):
    geheime_sleutel = secrets.randbelow(n-3) + 2 #[2, n-2]
    publieke_sleutel = macht_mod(g, geheime_sleutel, n)
    return (publieke_sleutel, geheime_sleutel)

def genereer_gedeeld_geheim(publieke_sleutel, geheime_sleutel, n):
    return macht_mod(publieke_sleutel, geheime_sleutel, n)

def sleutel_afleiding_functie(geheim):
    geheim_bytes = geheim.to_bytes(math.ceil(geheim.bit_length() / 8), byteorder='big')
    salt = secrets.randbits(128)
    salt |= (1 << 127)
    salt = salt.to_bytes(math.ceil(salt.bit_length() / 8), byteorder='big')

    afgeleide_sleutel = hashlib.sha256(geheim_bytes + salt).digest()

    while len(afgeleide_sleutel) < 16:
        afgeleide_sleutel += hashlib.sha256(afgeleide_sleutel).digest()

    return afgeleide_sleutel[:16]

def AES_sleutel(geheim):
    afgeleide_sleutel = sleutel_afleiding_functie(geheim)
    sleutel_base64 = base64.b64encode(afgeleide_sleutel).decode()
    return sleutel_base64

def naar_base64(getal):
    return base64.b64encode(getal.to_bytes(math.ceil(getal.bit_length() / 8), byteorder='big')).decode()

def sleuteluitwisseling():
    n = willekeurig_priem_1024_bit_getal()
    g = 2

    print('\n-------------------------------')
    print(f'\nModulus: {naar_base64(n)}\n\nGrondtal: {naar_base64(g)}')

    sleutels_partij_1 = genereer_sleutels(n, g)
    sleutels_partij_2 = genereer_sleutels(n, g)

    print(f'\nPublieke sleutel partij 1: {naar_base64(sleutels_partij_1[0])}\n\n\nGeheime sleutel partij 1: {naar_base64(sleutels_partij_1[1])}')
    print(f'\nPublieke sleutel partij 2: {naar_base64(sleutels_partij_2[0])}\n\n\nGeheime sleutel partij 2: {naar_base64(sleutels_partij_2[1])}')

    gedeeld_geheim_partij_1 = genereer_gedeeld_geheim(sleutels_partij_2[0], sleutels_partij_1[1], n)
    gedeeld_geheim_partij_2 = genereer_gedeeld_geheim(sleutels_partij_1[0], sleutels_partij_2[1], n)

    if(gedeeld_geheim_partij_1 == gedeeld_geheim_partij_2):
        geheim = gedeeld_geheim_partij_1

    print(f'\nGedeeld geheim: {naar_base64(geheim)}')

    sleutel = AES_sleutel(geheim)

    with open(sleutel_pad, 'w') as file:
        file.write(sleutel)

    print(f'\nAES Sleutel: {sleutel}')

    print('-------------------------------')
    print(f'\nGeheime sleutel\n{sleutel}\n-----------------------------------------------------')
    print(f'Geheime sleutel opgeslagen naar: {sleutel_pad}')