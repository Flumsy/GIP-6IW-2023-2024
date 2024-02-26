nummer = int(input("Kies een natuurlijk getal: "))
binairGetal = []

if nummer == 0:
    binairGetal.insert(0, 0)
else:
    while nummer != 0:
        bit = nummer % 2  # Modulus 2 om de rest van het getal / 2 te krijgen
        nummer = nummer // 2  # Getal delen door 2 voor volgende iteratie
        binairGetal.insert(0, bit)  # Bit (rest) opslagen in een lijst

print(''.join(str(i) for i in binairGetal))  # Lijst printen