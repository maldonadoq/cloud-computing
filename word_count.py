dataset = ["humano","persona","gente","hombre","mujer","familia","amigo","conocido","colega","pareja","esposo","matrimonio",
			"amor","criatura","especie","ser","vida","naturaleza","campo","bosque","selva","jungla","desierto","costa","playa",
			"río","laguna","lago","mar","océano","cerro","monte","montaña"]

def mwordcount(filename, data):
	f = open(filename, "r")

	if(f.mode == 'r'):
		content = f.read()
		print(content)

if __name__ == "__main__":
	mwordcount("data/data10k.txt", dataset)