#include <iostream>

int main(int argc, char const *argv[]){
	
	long size = 1000;

	if(argc == 2){
		size = atoi(argv[1]);
	}


	long i;

	long product;
	int tconst = 1997;
	for(i=0; i<size; i++){
		product = i*tconst;
	}

	std::cout << "i: " << i << "\n";

	return 0;
}