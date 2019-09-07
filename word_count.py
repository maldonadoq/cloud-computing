def wordcount(str):
    counts = dict()
    words = str.split()

    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    return counts

def mwordcount(filename):
	f = open(filename, "r")

	if(f.mode == 'r'):
		content = f.read()
		words = wordcount(content)

		for word, count in words.items():
			print(word, " => ", count)

if __name__ == "__main__":
	counts = mwordcount("data/data1k.txt")