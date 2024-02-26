#include <iostream>
#include <string>
#include <list>
using namespace std;

int main() {
    int nummer;
    list<int> binairGetal{};
    cout << "Kies een natuurlijk getal: ";
    cin >> nummer;
    
    if(nummer == 0) {
        binairGetal.push_front(0);
    } else {
        while(nummer != 0) {
            int bit = nummer % 2; //Modulus 2 om de rest van het getal / 2 te krijgen
            nummer = nummer / 2; //Getal delen door 2 voor volgende iteratie
            binairGetal.push_front(bit); //Bit (rest) opslagen in een lijst
        }
    }

    for(auto i : binairGetal) {
        cout << i; //Lijst printen
    }

    return 0;
}