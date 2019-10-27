#include <iostream>
#include <bitset>
#include <cmath>

using namespace std;

int main(int argc, char const *argv[]){
    const int sieve_size = 100000;

    bitset<sieve_size> sieve;
    sieve.flip();

    int finalBit = sqrt(sieve.size()) + 1;

    // Perform sieve of Eratosthenes
    for(int i = 2; i < finalBit; ++i){
		if(sieve.test(i)){
			for(int j = 2*i; j < sieve_size; j+=i){
				sieve.reset(j);
			}
		}
    }
    
    // Print First prime numbers in range [2, sieve_size]
    int count = 0;
    for(int i = 2; i < sieve_size; i++){
		if(sieve.test(i)){
			count++;
			//cout << i << " ";
		}
    }
    cout << "Primes [2-" << sieve_size << "]: " << count << "\n";
}  