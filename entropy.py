from collections import Counter, defaultdict
import math, random

def randomize_character(file_name,res_file, mess_probability):
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
				if(random.random() <= mess_probability):
					char = random.choice(list(character_list))
				word += char
			write_file.write(word + "\n")
	write_file.close()
	entropy, perplexity = get_cond_prob_and_perplexity(res_file)
	print("After messing up characters with a probability of {0} for file {1}, the entropy is: {2}".format(mess_probability, file_name, entropy))

def randomize_word(file_name,res_file, mess_probability):
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
			if(random.random() <= mess_probability):
				word = random.choice(list(word_list))
			write_file.write(word + "\n")
	write_file.close()
	entropy, perplexity = get_cond_prob_and_perplexity(res_file)
	print("After messing up words with a probability of {0} for file {1}, the entropy is: {2}".format(mess_probability, file_name, entropy))

def get_cond_prob_and_perplexity(file_name):
	text = open(file_name).read()
	lines = text.split("\n")
	total_count = len(lines)
	unigram = defaultdict(int)
	for line in lines:
		unigram[line] += 1

	bigrams = Counter(zip(lines, lines[1:]))
	sum = 0.0
	bigram_count = total_count - 1
	for word in bigrams:
		if word[0] in unigram:
			joint_prob = float(bigrams[word]/bigram_count)
			cond_prob = float(bigrams[word]/unigram[word[0]])
			sum += joint_prob * math.log(cond_prob, 2)
	entropy = -sum
	perplexity = math.pow(2, entropy)
	return entropy, perplexity

def mess_up_experiments(file, res_file):
	for i in range(10):
		randomize_character(file, res_file, 0.1)
		randomize_character(file, res_file, 0.05)
		randomize_character(file, res_file, 0.01)
		randomize_character(file, res_file, 0.001)
		randomize_character(file, res_file, 0.0001)
		randomize_character(file, res_file, 0.00001)
		randomize_word(file, res_file, 0.1)
		randomize_word(file, res_file, 0.05)
		randomize_word(file, res_file, 0.01)
		randomize_word(file, res_file, 0.001)
		randomize_word(file, res_file, 0.0001)
		randomize_word(file, res_file, 0.00001)

entropy, perplexity = get_cond_prob_and_perplexity("TEXTEN1.txt")
print("The entropy for the English text is", entropy)
print("The perplexity for the English text is", perplexity)
entropy, perplexity = get_cond_prob_and_perplexity("TEXTCZ1UTF.txt")
print("The entropy for the Czech text is", entropy)
print("The perplexity for the Czech text is", perplexity)

res_file = "random_text.txt"
mess_up_experiments("TEXTEN1.txt",res_file)
mess_up_experiments("TEXTCZ1UTF",res_file)
