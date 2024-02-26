#include <iostream>
#include <string>
#include <list>
#include <vector>
#include <random>
using namespace std;

list<int> naar_binair(int nummer) {
    list<int> binairGetal{};
    
    if(nummer == 0) {
        binairGetal.push_front(0);
    } else {
        while(nummer != 0) {
            int bit = nummer % 2; //Modulus 2 om de rest van het getal / 2 te krijgen
            nummer = nummer / 2; //Getal delen door 2 voor volgende iteratie
            binairGetal.push_front(bit); //Bit (rest) opslagen in een lijst
        }
    }

    return binairGetal;
}

int* list_naar_array(const list<int>& lst, size_t& elementen) {
    elementen = lst.size();
    int* arr = new int[elementen];
    auto it = lst.begin();
    for (size_t i = 0; i < elementen; ++i, ++it) {
        arr[i] = *it;
    }
    return arr;
}

int macht_mod(int gndt, int exp, int mod) {
    list<int> binair = naar_binair(exp);
    size_t aantal_kwadraten = binair.size();
    int* arrBinair = list_naar_array(binair, aantal_kwadraten);

    int resultaat = 1;
    int huidige_wortel = gndt % mod;

    for (size_t i = 0; i < aantal_kwadraten; ++i) {
        if (arrBinair[aantal_kwadraten - i - 1] == 1) {
            resultaat = (resultaat * huidige_wortel) % mod;
        }
        huidige_wortel = (huidige_wortel * huidige_wortel) % mod;
    }

    delete[] arrBinair;

    return resultaat;
}

vector<uint32_t> genereerRandom1024BitGetal() {
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<uint32_t> dis;

    vector<uint32_t> getal(32);
    for(size_t i = 0; i < getal.size(); ++i) {
        getal[i] = dis(gen);
    }

    getal.back() |= (uint32_t(1) << 31);

    return getal;
}

int main() {
    vector<uint32_t> random_number = genereerRandom1024BitGetal();

    // Output the generated number in hexadecimal
    for(size_t i = 0; i < random_number.size(); ++i) {
        printf("%08x", random_number[i]);
    }
}