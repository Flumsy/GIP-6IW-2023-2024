import os

from RSA.sleutelgeneratie import genereer_sleutel as RSA_sleutel
from AES.sleutelgeneratie import genereer_sleutel as AES_sleutel

from RSA.encryptie import encryptie as RSA_versleutel
from AES.encryptie import encryptie as AES_versleutel
from AES.encryptie import encryptie_DH as AES_DH_versleutel

from RSA.decryptie import decryptie as RSA_ontsleutel
from AES.decryptie import decryptie as AES_ontsleutel

os.system('cls')

def sleutelgeneratie():
    print('-------------------------------')
    keuze = input('-Sleutelgeneratie- Kies een algoritme:\n1) RSA\n2) AES\n3) Terug\n-------------------------------\n')
    match keuze:
        case '1':
            RSA_sleutel()
        case '2':
            AES_sleutel()
        case '3':
            pass
        case _:
            print("-------------------------------\n\nOngeldige keuze\n")
            sleutelgeneratie()

def encryptie():
    print('-------------------------------')
    keuze = input('-Encryptie- Kies een algoritme:\n1) RSA\n2) AES\n3) AES + DH\n4) Terug\n-------------------------------\n')
    match keuze:
        case '1':
            print('-------------------------------')
            bericht = input('\nBericht te versleutelen:\n')
            RSA_versleutel(bericht)
        case '2':
            print('-------------------------------')
            bericht = input('\nBericht te versleutelen:\n')
            AES_versleutel(bericht)
        case '3':
            print('-------------------------------')
            bericht = input('\nBericht te versleutelen:\n')
            AES_DH_versleutel(bericht)
        case '4':
            pass
        case _:
            print("-------------------------------\n\nOngeldige keuze\n")
            encryptie()

def decryptie():
    print('-------------------------------')
    keuze = input('-Decryptie- Kies een algoritme:\n1) RSA\n2) AES\n3) Terug\n-------------------------------\n')
    match keuze:
        case '1':
            print('-------------------------------\n')
            RSA_ontsleutel()
        case '2':
            print('-------------------------------\n')
            AES_ontsleutel()
        case '3':
            pass
        case _:
            print("-------------------------------\n\nOngeldige keuze\n")
            decryptie()

while True:
    print('-------------------------------')
    keuze = input('''Kies een optie:\n1) Sleutelgeneratie\n2) Encryptie\n3) Decryptie\n4) Afsluiten\n-------------------------------\n''')

    match keuze:
        case '1':
            sleutelgeneratie()
        case '2':
            encryptie()
        case '3':
            decryptie()
        case '4':
            break
        case _:
            print("-------------------------------\n\nOngeldige keuze\n")

