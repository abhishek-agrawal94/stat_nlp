from collections import Counter, defaultdict
import random

def get_probs(file_name):
	with open(file_name) as f:
		text = f.read()
	tokens = text.split()
	total_count = len(tokens)
	vocab = set(tokens)
	unigrams = Counter(tokens)
	bigram_text = "<s>\n" + text
	bigram_tokens = bigram_text.split()
	bigrams = zip(bigram_tokens,bigram_tokens[1:])
	bigram_count = Counter(bigrams)
	trigram_text = "<s>\n" + bigram_text
	trigram_tokens = trigram_text.split()
	trigrams = zip(trigram_tokens,trigram_tokens[1:],trigram_tokens[2:])
	trigram_count = Counter(trigrams)
	p0 = 1 / len(vocab)
	p1 = unigrams
	for unigram in unigrams:
		p1[unigram] = unigrams[unigram] / total_count
	p2 = bigram_count
	for bigram in bigram_count:
		if bigram[0] in unigrams:
			p2[bigram] = bigram_count[bigram] / unigrams[bigram[0]]
	p3 = trigram_count
	for trigram in trigram_count:
		if (trigram[0], trigram[1]) in bigrams:
			p3[trigram] = trigram_count[trigram] / bigram_count[trigram[0],trigram[1]]
	return p0, p1, p2, p3

def calc_lambdas(file_name, p0, p1, p2, p3):
	with open(file_name) as f:
		text = f.read()
	text = "<s>\n<s>\n" + text
	tokens = text.split()
	trigrams = list(zip(tokens,tokens[1:], tokens[2:]))
	termination_condition = 0.0001
	lambdas = []
	for i in range(4):
		lambdas.append(random.randint(1,10))
	norm = sum(lambdas)
	for i in range(4):
		lambdas[i] /= norm
	next_lambdas = [0.0] * 4
	expected_counts = [0.0] * 4
	while True:
		for trigram in trigrams:
			prob = lambdas[3] * p3[trigram] + lambdas[2] * p2[trigram[1], trigram[2]] + lambdas[1] * p1[trigram[2]] + lambdas[0] * p0
			expected_counts[0] += lambdas[0] * p0 / prob
			expected_counts[1] += lambdas[1] * p1[trigram[2]] / prob
			expected_counts[2] += lambdas[2] * p2[trigram[1], trigram[2]] / prob
			expected_counts[3] += lambdas[3] * p3[trigram] / prob
		arr = []
		for i in range(4):
			next_lambdas[i] = expected_counts[i] / sum(expected_counts)
			arr.append(abs((lambdas[i] - next_lambdas[i])) < termination_condition)

		lambdas = next_lambdas.copy()
		expected_counts = [0.0] * 4
		if all(arr):
			break
	print("Smoothed lambdas:")
	print(lambdas)



p0, p1, p2, p3 = get_probs("TRAINEN.txt")
lambdas = calc_lambdas("HOLDOUTEN.txt", p0, p1, p2, p3)
#word_prob, word_count, uniform_probability = get_word_prob(file_name)
#get_bigram_prob(file_name, word_count)
#bigram_count, bigram_probability = get_bigram_prob(file_name, word_count)
#trigram_count, trigram_probability = get_trigram_prob(file_name, bigram_count)
