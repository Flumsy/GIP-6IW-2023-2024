from RSA import sleutelgeneratie as RSA

keuze = input(
    '''
    Kies een optie:
    1) Sleutelgeneratie
    2) Encryptie
    3) Decryptie
    -------------------------------
    '''
)

match keuze:
    case '1':
        print('')
        keuze = input('    Kies een encryptie algoritme:\n    1) RSA\n    2) AES\n    -------------------------------\n    ')
        match keuze:
            case '1':
                RSA.genereer_sleutel()
            case '2':
                print('dwadaw')
    case '2':
        print('dwadaw')
    case '3':
        print('dwadaw')