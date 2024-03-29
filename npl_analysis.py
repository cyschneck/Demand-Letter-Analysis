# NPL and Sentiment Analysis of Anti-Racism Letters
# python3 npl_analysis.py
import os
import math
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})

import nltk
nltk.download('punkt') # Frequency Distribution
nltk.download('stopwords') # Stopwords for cleanup
nltk.download('vader_lexicon') # Sentiment Analysis via VADER (Valence Aware Dictionary for Sentiment Reasoning)
from nltk.sentiment import SentimentIntensityAnalyzer # Sentiment Analysis via VADER

most_freq_amount = 20

occurrence_dict = {} # file_name, occurence

def textAsToken(file_dir):
	# Return the text file as tokens
	print(file_dir)
	with open(file_dir, "r") as f:
		file_text = f.readlines()
	file_text = " ".join(file_text) # combine all lines into one string

	# Break into Tokens and Clean-up
	string_as_tokens_list = nltk.word_tokenize(file_text)
	stopwords = nltk.corpus.stopwords.words("english")
	string_as_tokens_list = [w for w in string_as_tokens_list if w not in stopwords] # remove stopwords
	punctuation = [".", ",", ";", ")", "(", "‘", "●", ":", '“', '”', '○', "[", "]", "&", '’', "%", "*", "–", "·", "-"]
	string_as_tokens_list = [w for w in string_as_tokens_list if w not in punctuation] # remove punctuation

	return string_as_tokens_list

def frequencyDistribution(plot_title_from_file_name, root_dir, file_as_tokens):
	# Frequency Distribution of text
	# Frequency Breakdown
	plt_title = plot_title_from_file_name.replace(" ", "_").lower()
	frequency_dist = nltk.FreqDist(file_as_tokens)

	# Plot Frequency Distribution
	frequencyDistribution_as_dict = dict(frequency_dist.most_common(most_freq_amount)) # convert to dict for plotting
	occurrence_dict["{0}_single".format(plt_title)] = frequencyDistribution_as_dict
	#print(frequencyDistribution_as_dict)

	fig = plt.figure(figsize=(12,12), dpi=100)
	plt.title("{0}: Word Frequency".format(plot_title_from_file_name))
	plt.bar(frequencyDistribution_as_dict.keys(), frequencyDistribution_as_dict.values())
	plt.xticks(rotation=90)
	plt.ylabel("Occurrence")
	#plt.show()
	fig.savefig('{0}/{1}_frequency_dist.png'.format(root_dir, plt_title))

def collocationDistribution(plot_title_from_file_name, root_dir, file_as_tokens):
	# Find word combinations
	plt_title = plot_title_from_file_name.replace(" ", "_").lower()

	def plotNGram(n_gram_amount, n_gram_finder):
		# Plot N-Grams
		nGram_as_dict_temp = dict(n_gram_finder.ngram_fd.most_common(most_freq_amount)) # convert to dict for plotting
		occurrence_dict["{0}_{1}".format(plt_title, n_gram_amount.lower())] = nGram_as_dict_temp
		#print(nGram_as_dict_temp)

		nGram_as_dict = {}
		for k, v in nGram_as_dict_temp.items():
			nGram_as_dict[", ".join(k)] = v # rename key from ('graduate', 'division') to "graduate, division"

		fig = plt.figure(figsize=(12,12), dpi=100)
		fig.subplots_adjust(bottom=0.3)
		plt.title("{0}: {1}".format(plot_title_from_file_name, n_gram_amount))
		plt.bar(nGram_as_dict.keys(), nGram_as_dict.values())
		plt.xticks(rotation=90)
		plt.ylabel("Occurrence")
		fig.savefig('{0}/{1}_frequency_dist_{2}.png'.format(root_dir, 
																	plot_title_from_file_name.replace(" ", "_").lower(),
																	n_gram_amount.lower()))


	# Bigrams: Two-Word Combinations
	bigram_collocation_dist = nltk.collocations.BigramCollocationFinder.from_words(file_as_tokens)
	plotNGram("Bigrams", bigram_collocation_dist)
	# Trigrams: Three-Word Combinations
	trigram_collocation_dist = nltk.collocations.TrigramCollocationFinder.from_words(file_as_tokens)
	plotNGram("Trigrams", trigram_collocation_dist)
	# Quadgrams: Four-Word Combinations
	quadgram_collocation_dist = nltk.collocations.QuadgramCollocationFinder.from_words(file_as_tokens)
	plotNGram("Quadgrams", quadgram_collocation_dist)

def sentimentAnalysis(plot_title_from_file_name, root_dir, file_as_tokens):
	# Sentiment Analysis of Pieces of X Length
	# VADER Citation: Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.
	size_of_sentiment_string = 15 # average length of a sentence
	list_of_strings_x_length = []
	for i in range(0, len(file_as_tokens), size_of_sentiment_string):
		string_sentence = " ".join(file_as_tokens[i:i+size_of_sentiment_string])
		list_of_strings_x_length.append(string_sentence)

	sentiment_analyzer = SentimentIntensityAnalyzer() # Via VADER*
	sent_dict_postive = {}
	sent_dict_neutral = {}
	sent_dict_negative = {}
	for i, string_sent in enumerate(list_of_strings_x_length):
		sent_dict_for_sentence = sentiment_analyzer.polarity_scores(string_sent)
		sent_dict_postive[i] = sent_dict_for_sentence["pos"]
		sent_dict_neutral[i] = sent_dict_for_sentence["neu"]
		sent_dict_negative[i] = sent_dict_for_sentence["neg"]

	color_plot = {"Postive": "Reds", "Negative": "Blues", "Neutral": "gray"} # colors for plot (cmap)

	# Plot Sentiment Individually
	def plotSentimentIndvidually(polarity_name, polarity_dict):
		# Plot
		fig = plt.figure(figsize=(12,12), dpi=100)
		plt.title("{0}: {1} Sentiment".format(plot_title_from_file_name, polarity_name))
		plt.scatter(polarity_dict.keys(), polarity_dict.values(), c=[i * 10 for i in polarity_dict.values()], cmap=color_plot[polarity_name])
		plt.xticks(rotation=90)
		plt.xlabel("Sentence Piece")
		plt.ylabel("{0} Sentiment %".format(polarity_name))
		fig.savefig('{0}/{1}_{2}_sentiment.png'.format(root_dir, 
														plot_title_from_file_name.replace(" ", "_").lower(),
														polarity_name.lower()))
	plotSentimentIndvidually("Postive", sent_dict_postive)
	plotSentimentIndvidually("Neutral", sent_dict_neutral)
	plotSentimentIndvidually("Negative", sent_dict_negative)

	# Plot as Group
	fig = plt.figure(figsize=(12,12), dpi=100)
	plt.title("{0}: Postive and Negative Sentiment".format(plot_title_from_file_name))
	plt.scatter(sent_dict_postive.keys(), sent_dict_postive.values(), c=[i * 10 for i in sent_dict_postive.values()], cmap=color_plot["Postive"])
	#plt.scatter(sent_dict_neutral.keys(), sent_dict_neutral.values(), c=[i * 10 for i in sent_dict_neutral.values()], cmap=color_plot["Neutral"])
	plt.scatter(sent_dict_negative.keys(), sent_dict_negative.values(), c=[i * 10 for i in sent_dict_negative.values()], cmap=color_plot["Negative"])
	plt.xticks(rotation=90)
	plt.xlabel("Sentence #")
	plt.ylabel("Sentiment %")
	fig.savefig('{0}/{1}_pos_and_neg_sentiment.png'.format(root_dir, plot_title_from_file_name.replace(" ", "_").lower()))

	# Plot Trends by Ploting a Line Graph for Every X
	size_of_text_chunks = len(sent_dict_postive.keys()) - 1
	average_every_x = 25 # average the sentiment of x sentences
	average_pos_dict = {}
	average_neg_dict = {}
	for i in range(0, size_of_text_chunks, math.floor(size_of_text_chunks/average_every_x)):
		pos_polarity_values = []
		neg_polarity_values = []
		for j in range(i, i+average_every_x-1):
			if j in sent_dict_postive.keys() and j in sent_dict_negative.keys():
				pos_polarity_values.append(sent_dict_postive[j])
				neg_polarity_values.append(sent_dict_negative[j])
		average_pos_dict[i] = sum(pos_polarity_values) / len(pos_polarity_values)
		average_neg_dict[i] = sum(neg_polarity_values) / len(neg_polarity_values)

	fig = plt.figure(figsize=(12,12), dpi=100)
	plt.title("{0}: Trends in Sentiment".format(plot_title_from_file_name))
	plt.scatter(sent_dict_postive.keys(), sent_dict_postive.values(), c=[i * 10 for i in sent_dict_postive.values()], cmap=color_plot["Postive"])
	plt.scatter(sent_dict_negative.keys(), sent_dict_negative.values(), c=[i * 10 for i in sent_dict_negative.values()], cmap=color_plot["Negative"])
	plt.plot(list(average_pos_dict.keys()), list(average_pos_dict.values()), c="red")
	plt.plot(list(average_neg_dict.keys()), list(average_neg_dict.values()), c="blue")
	plt.xticks(rotation=90)
	plt.xlabel("Sentence #")
	plt.ylabel("Sentiment %")
	#plt.show()
	fig.savefig('{0}/{1}_pos_and_neg_sentiment.png'.format(root_dir, plot_title_from_file_name.replace(" ", "_").lower()))

def plotComparisons(root_directory, comparison_dict):
	# Plot Comparisons Graphs to see if common words are used across letters
	titles = list(comparison_dict.keys())
	x_word_label = []
	# collect a list of all the words in all the text
	for text_title, occurrence_dict in comparison_dict.items():
		temp_title_lst = []
		for word, occurrence in occurrence_dict.items():
			if word not in x_word_label:
				x_word_label.append(word)
	#print(x_word_label)

	# create a list of lists for all texts with each word and their occurrence
	titles_lst_of_lst = []
	for i in titles:
		titles_lst_of_lst.append([]) # create an empty list of lists for each title

	# create a list of lists to track frequency of specific works to multi-group bar graph
	for word in x_word_label:
		for title, word_with_occurrence in comparison_dict.items():
			if word in word_with_occurrence:
				titles_lst_of_lst[titles.index(title)].append(word_with_occurrence[word])
			else:
				titles_lst_of_lst[titles.index(title)].append(0)

	fig = plt.figure(figsize=(12,12), dpi=100)
	word_type_title = titles[0].split("_")[-1]
	plt.title("Comparisons for {0} Words".format(word_type_title.capitalize()))
	for i, title in enumerate(titles):
		plt.bar(x_word_label, titles_lst_of_lst[i], label = title) # plot multiple bar graphs in one graph
	plt.xticks(rotation=90)
	plt.tight_layout()
	plt.ylabel("Occurrence")
	plt.legend()
	#plt.show()
	fig.savefig('{0}/comparisons_{1}.png'.format(root_directory, word_type_title))

if __name__ == '__main__':
	# retrieve text from letters
	file_output_list = []
	root_directory = "demand_letters_output"
	for file_output in os.listdir(root_directory):
		if file_output.split(".")[-1] == "txt":
			file_output_list.append(os.path.join(root_directory, file_output))
	print("File list: {0}".format(file_output_list))

	for file_dir in file_output_list:
		file_text_tokens = textAsToken(file_dir)

		title_plot = file_dir.split("/")[1].split(".")[0].replace("_", " ").upper() # retrieve file name from path

		# NPL:
		frequencyDistribution(title_plot, root_directory, file_text_tokens)
		collocationDistribution(title_plot, root_directory, file_text_tokens)
		sentimentAnalysis(title_plot, root_directory, file_text_tokens)

	# compare the frequency of common words between texts
	comparison_dict_single = {}
	comparison_dict_bigrams = {}
	comparison_dict_trigrams = {}
	comparison_dict_quadgrams = {}
	for key, values in occurrence_dict.items():
		if "single" in key:
			comparison_dict_single[key] = values
		if "bigrams" in key:
			nGrams_dict = {}
			for nGrams, amount in values.items():
				nGrams_dict[' '.join(nGrams)] = amount # combine to form a single word to search
			comparison_dict_bigrams[key] = nGrams_dict
		if "trigrams" in key:
			nGrams_dict = {}
			for nGrams, amount in values.items():
				nGrams_dict[' '.join(nGrams)] = amount # combine to form a single word to search
			comparison_dict_trigrams[key] = nGrams_dict
		if "quadgrams" in key:
			nGrams_dict = {}
			for nGrams, amount in values.items():
				nGrams_dict[' '.join(nGrams)] = amount # combine to form a single word to search
			comparison_dict_quadgrams[key] = nGrams_dict

	plotComparisons(root_directory, comparison_dict_single)
	plotComparisons(root_directory, comparison_dict_bigrams)
	plotComparisons(root_directory, comparison_dict_trigrams)
	plotComparisons(root_directory, comparison_dict_quadgrams)
