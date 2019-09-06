from random import randint

dataset = ["humano","persona","gente","hombre","mujer","familia","amigo","conocido","colega","pareja","esposo","matrimonio",
			"amor","criatura","especie","ser","vida","naturaleza","campo","bosque","selva","jungla","desierto","costa","playa",
			"río","laguna","lago","mar","océano","cerro","monte","montaña"]

def mprint(data):
    for word in data:
    	print(word)

def mgenerate(filename, data, count):
	msize = len(data)-1
	f = open(filename,"w+")

	for i in range(count):
		r = randint(0, msize)
		f.write(data[r] + "\n")
		# print(data[r])

	f.close()

if __name__ == "__main__":
	#mprint(dataset)
	mgenerate("data/data1000000k.txt", dataset, 1000000000)