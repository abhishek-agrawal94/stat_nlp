from collections import Counter, defaultdict
import math, random

def randomize_character(file_name,res_file):
	character_list = set()
	with open(file_name) as f:
		for line in f:
			character_list.update(list(line))

	# print("Character List: {}".format(character_list))
	# print(len(character_list))
	character_list.discard("\n")
	# print(len(character_list))
	write_file = open(res_file,"w")
	with open(file_name) as f:
		for line in f:
			word = ""
			for char in line.split()[0]:
				random.seed()
				if(random.random() <= 0.0001):
					char = random.choice(list(character_list))
				word += char
			write_file.write(word + "\n")
	write_file.close()

def randomize_word(file_name,res_file):
	word_list = set()
	with open(file_name) as f:
		for line in f:
			word_list.add(line.split()[0])
	#print("word List: {}".format(word_list))
	#print(len(word_list))
	# print(len(character_list))
	write_file = open(res_file,"w")
	with open(file_name) as f:
		for line in f:
			word = line.split()[0]
			random.seed()
			if(random.random() <= 0.1):
				word = random.choice(list(word_list))
			write_file.write(word + "\n")
	write_file.close()

def get_word_prob(file_name):
	total_count = sum(1 for line in open(file_name))
	#print("total count: {}".format(total_count))

	c= Counter()
	with open(file_name) as f:
		for line in f:
			c.update(line.split())

	#print(c)
	word_count = dict(c)
	#print("word count: {}".format(word_count))

	word_prob = {}
	for key, value in word_count.items():
		word_prob[key] = value/total_count
	return word_prob
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

def get_entropy_perplexity(file_name, word_prob, bigram_count, total_bigrams, run):
	previous = ""
	joint_probability = {}
	conditional_probability = {}
	summation = 0
	entropy = 0
	perplexity = 0
	with open(file_name) as f:
		for line in f:
			if(previous != ""):
				#joint_probability[previous + "," + line.split()[0]] = word_prob[previous] * word_prob[line.split()[0]]
				joint_probability[previous + "," + line.split()[0]] = bigram_count[previous + "," + line.split()[0]] / total_bigrams
				conditional_probability[line.split()[0] + "|" + previous] = joint_probability[previous + "," + line.split()[0]] / word_prob[previous]
				summation += joint_probability[previous + "," + line.split()[0]] * math.log(conditional_probability[line.split()[0] + "|" + previous], 2)
			previous = line.split()[0]
	#print("Joint probability: {}".format(joint_probability))
	#print("Conditional probability: {}".format(conditional_probability))
	entropy = (-1) * summation
	print(run)
	print("Entropy: {}".format(entropy))
	perplexity = math.pow(2, entropy)
	print("perplexity: {}".format(perplexity))




file_name = "TEXTCZ1UTF.txt"
word_prob = get_word_prob(file_name)
bigram_count, total_bigrams = get_bigram_prob(file_name)
get_entropy_perplexity(file_name, word_prob, bigram_count, total_bigrams, "original: ")
res_file = "random_text.txt"
for i in range(10):
	randomize_word(file_name, res_file)
	word_prob = get_word_prob(res_file)
	bigram_count, total_bigrams = get_bigram_prob(res_file)
	get_entropy_perplexity(res_file, word_prob, bigram_count, total_bigrams, "run " + str(i) + " :")
