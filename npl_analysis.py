# NPL and Sentiment Analysis of Anti-Racism Letters
# python3 demand_letter_analysis.py
import os

import nltk
nltk.download('punkt') # Frequency Distribution
nltk.download('stopwords') # Stopwords for cleanup

def textAsString(file_dir):
	# Return the text file as a single long string
	with open(file_dir) as f:
		file_text = f.readlines()
	file_text = " ".join(file_text) # combine all lines into one string
	return file_text

def frequencyDistribution(file_string):
	# Frequency Distribution of text
	# Break into Tokens and Clean-up
	string_as_tokens_list = nltk.word_tokenize(file_string)
	stopwords = nltk.corpus.stopwords.words("english")
	string_as_tokens_list = [w for w in string_as_tokens_list if w not in stopwords] # remove stopwords
	punctuation = ["!", ".", ",", ";", ")", "(", "‘", "●", ":", '“', '”', '○', "[", "]", "&", '’', "%"]
	string_as_tokens_list = [w for w in string_as_tokens_list if w not in punctuation] # remove punctuation
	# Frequency Breakdown
	frequency_dist = nltk.FreqDist(string_as_tokens_list)
	print(frequency_dist.most_common(50))

if __name__ == '__main__':
	# retrieve text from letters
	file_output_list = []
	root_directory = "demand_letters_output"
	for file_output in os.listdir(root_directory):
		file_output_list.append(os.path.join(root_directory, file_output))

	for file_dir in file_output_list:
		file_text = textAsString(file_dir)
		frequencyDistribution(file_text)
		break
