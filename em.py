from collections import Counter, defaultdict

def get_word_prob(file_name):
	total_count = sum(1 for line in open(file_name))
	#print("total count: {}".format(total_count))
    total_count = 0
    vocab_size = 0
    vocab = set()
	c= Counter()
	with open(file_name) as f:
		for line in f:
            total_count += 1
            vocab.add(line.split()[0])
			c.update(line.split())
    vocab_size = len(vocab)
	#print(c)
	word_count = dict(c)
	#print("word count: {}".format(word_count))

	word_prob = {}
	for key, value in word_count.items():
		word_prob[key] = value/total_count
	return word_prob, word_count, 
	#print("word probability: {}".format("word_prob"))

def get_bigram_prob(file_name):
	bigram_count = defaultdict(int)
	total_bigrams = 0
	previous = ""
	with open(file_name) as f:
		for line in f:
			if(previous != ""):
				bigram_count[previous + "," + line.split()[0]] += 1
				total_bigrams += 1
			previous = line.split()[0]
	return bigram_count, total_bigrams
	#print("bigram count: {}".format(bigram_count))
