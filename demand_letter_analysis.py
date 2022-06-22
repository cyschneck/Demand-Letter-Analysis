# Sentiment Analysis of Anti-Racism Letters
# python3 demand_letter_analysis.py
import os
import docx

list_of_demand_letters = [] # total list of all letters and their locations

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
		#print(letter)
		#print(letter.split("."))
		#print(letter.split(".")[1])
		extension = letter.split(".")[-1]
		if extension not in extension_types_and_instances_dict.keys():
			extension_types_and_instances_dict[extension] = 1
		else:
			extension_types_and_instances_dict[extension] += 1
	return extension_types_and_instances_dict
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
