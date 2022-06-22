# Sentiment Analysis of Anti-Racism Letters
# python3 demand_letter_analysis.py
import os
import docx

list_of_demand_letters = [] # total list of all letters and their locations

## PRE-PROCESSING RAW DIRECTORIES AND FILES ############################

def GetListOfLettersFromDirectory(path_directory):
	# get all the letters from a directory
	print("Directories = {0}".format(path_directory))
	for file_name in os.listdir(path_directory):
		if file_name != ".gitignore":
			if os.path.isdir(os.path.join(path_directory, file_name)): # recursively search all subdirectories
				GetListOfLettersFromDirectory(os.path.join(path_directory, file_name))
			else:
				list_of_demand_letters.append(os.path.join(path_directory, file_name))

def GetFileTypes():
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
	GetListOfLettersFromDirectory(root_directory)
	print("Total Letters = {0}\n".format(len(list_of_demand_letters)))

	extension_dict = GetFileTypes()
	print("File types: {0}\n".format(extension_dict))
