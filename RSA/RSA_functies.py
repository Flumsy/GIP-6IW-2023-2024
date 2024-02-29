from random import randint
import secrets
import os

sleutels_folder = os.path.join(os.path.dirname(__file__), '..', 'Sleutels')
berichten_folder = os.path.join(os.path.dirname(__file__), '..', 'Berichten')

if not os.path.exists(sleutels_folder):
    os.makedirs(sleutels_folder)

if not os.path.exists(berichten_folder):
    os.makedirs(berichten_folder)

publieke_sleutel_pad = os.path.abspath(os.path.join(sleutels_folder, 'RSA_publieke_sleutel.txt'))
geheime_sleutel_pad = os.path.abspath(os.path.join(sleutels_folder, 'RSA_geheime_sleutel.txt'))
berichten_pad = os.path.abspath(os.path.join(berichten_folder, 'RSA_bericht.txt'))

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

def tekst_naar_ascii(tekst):
    ascii_array = [ord(char) for char in tekst]
    return ascii_array

def ascii_naar_tekst(ascii):
    tekst_array = []
    for i in ascii:
        tekst_array.append(chr(i))
    tekst = ''.join(tekst_array)
    return tekst

def uitgebreid_euclidisch_algoritme(a, b):
    if a == 0:
        return b, 0, 1
    ggd, x1, y1 = uitgebreid_euclidisch_algoritme(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return ggd, x, y

def vind_d(e, phi_n):
    ggd, x, y = uitgebreid_euclidisch_algoritme(e, phi_n)
    if ggd != 1:
        raise Exception('Modulaire inverse bestaat niet')
    else:
        return x % phi_n

def versleutel(m, n, e):
    m = tekst_naar_ascii(m)
    c = []
    for i in m:
        c.append(macht_mod(i, e, n))
    return c

def versleutelde_array_naar_hex(c):
    hex_string = ""
    for getal in c:
        hex_string += hex(getal)
    return hex_string

def ontsleutel(c, n, d):
    m = []
    for i in c:
        m.append(macht_mod(i, d, n))
    return ascii_naar_tekst(m)