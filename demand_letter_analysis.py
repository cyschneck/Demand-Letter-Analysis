# Sentiment Analysis of Anti-Racism Letters
# python3 demand_letter_analysis.py
import os
import re
import docx

list_of_demand_letters = [] # total list of all letters and their locations
list_of_demand_letters_as_text = [] # strings of text from letters

## PRE-PROCESSING RAW DIRECTORIES AND FILES ############################

def getListOfLettersFromDirectory(path_directory):
	# get all the letters from a directory
	print("Directories = {0}".format(path_directory))
	for file_name in os.listdir(path_directory):
		if file_name != ".gitignore":
			if os.path.isdir(os.path.join(path_directory, file_name)): # recursively search all subdirectories
				getListOfLettersFromDirectory(os.path.join(path_directory, file_name))
			else:
				list_of_demand_letters.append(os.path.join(path_directory, file_name))

def getFileTypes():
	# find types of files
	extension_types_and_instances_dict = {}
	for letter in list_of_demand_letters:
		extension = letter.split(".")[-1]
		if extension not in extension_types_and_instances_dict.keys():
			extension_types_and_instances_dict[extension] = 1
		else:
			extension_types_and_instances_dict[extension] += 1
	return extension_types_and_instances_dict

def convertDocxToText(docx_file_path):
	# return a text string of docx file
	file_as_text = ''
	print(docx_file_path)
	doc_letter = docx.Document(docx_file_path)
	for paragraph in doc_letter.paragraphs:
		paragraph_of_text = paragraph.text
		## TODO: Clean up unicode values from strings
		#paragraph_of_text = paragraph.text.replace('\u9679', "") # remove ●
		file_as_text += paragraph_of_text
	return file_as_text

def convertPDFToText(pdf_file_path):
	# return a text string of pdf file
	print(pdf_file_path)

########################################################################

if __name__ == '__main__':
	# reference to all demand letters stored in demand_letters/
	root_directory = "demand_letters"
	getListOfLettersFromDirectory(root_directory)
	print("Total Letters = {0}\n".format(len(list_of_demand_letters)))

	# Get File Types for all letters
	extension_dict = getFileTypes()
	if list(set(["docx", "pdf"]) - set(extension_dict)) != []: # if file extensions include files that are not .docx or .pdf
		print("WARNING: new file type found = {0}".format(list(set(["docx", "pdf"]) - set(extension_dict))))
	print("File types: {0}\n".format(extension_dict))

	for file_letter in list_of_demand_letters:
		extension = file_letter.split(".")[-1]
		if extension == "docx":
			list_of_demand_letters_as_text.append(convertDocxToText(file_letter))
		if extension == "pdf":
			#list_of_demand_letters_as_text(convertPDFToText(file_letter))
			exit()

	print(len(list_of_demand_letters_as_text))
