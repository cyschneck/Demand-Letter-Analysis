# NPL and Sentiment Analysis of Anti-Racism Letters
# python3 demand_letter_analysis.py
import os
import matplotlib.pyplot as plt

import nltk
nltk.download('punkt') # Frequency Distribution
nltk.download('stopwords') # Stopwords for cleanup

def textAsToken(file_dir):
	# Return the text file as tokens
	with open(file_dir) as f:
		file_text = f.readlines()
	file_text = " ".join(file_text) # combine all lines into one string

	# Break into Tokens and Clean-up
	string_as_tokens_list = nltk.word_tokenize(file_text)
	stopwords = nltk.corpus.stopwords.words("english")
	string_as_tokens_list = [w for w in string_as_tokens_list if w not in stopwords] # remove stopwords
	punctuation = ["!", ".", ",", ";", ")", "(", "‘", "●", ":", '“', '”', '○', "[", "]", "&", '’', "%"]
	string_as_tokens_list = [w for w in string_as_tokens_list if w not in punctuation] # remove punctuation

	return string_as_tokens_list

def frequencyDistribution(file_given, file_as_tokens):
	# Frequency Distribution of text
	# Frequency Breakdown
	frequency_dist = nltk.FreqDist(file_as_tokens)

	# Plot Frequency Distribution
	frequencyDistribution_as_dict = dict(frequency_dist.most_common(50)) # convert to dict for plotting
	#print(frequencyDistribution_as_dict)

	root_dir, file_name = file_given.split("/")
	title_plot = file_name.split(".")[0].replace("_", " ").upper()
	
	fig = plt.figure(figsize=(12,12), dpi=100)
	plt.title(title_plot)
	plt.bar(frequencyDistribution_as_dict.keys(), frequencyDistribution_as_dict.values())
	plt.xticks(rotation=90)
	plt.ylabel("Occurance")
	plt.show()
	fig.savefig('{0}/{1}_frequency_dist.png'.format(root_dir, file_name.split(".")[0]))

def collocationDistribution(file_as_tokens):
	# Find word combinations
	# Bigrams: Two-Word Combinations
	# Trigrams: Three-Word Combinations
	# Quadgrams: Four-Word Combinations
	pass

if __name__ == '__main__':
	# retrieve text from letters
	file_output_list = []
	root_directory = "demand_letters_output"
	for file_output in os.listdir(root_directory):
		file_output_list.append(os.path.join(root_directory, file_output))

	for file_dir in file_output_list:
		file_text_tokens = textAsToken(file_dir)
		frequencyDistribution(file_dir, file_text_tokens)
		collocationDistribution(file_text_tokens)
		break
