from random import randint
import secrets

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

def miller_rabin_test(getal, iterations=40):
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
    for _ in range(iterations):
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

print(willekeurig_priem_1024_bit_getal())



