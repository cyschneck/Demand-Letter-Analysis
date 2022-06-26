# Sentiment Analysis of Anti-Racism Letters
# python3 demand_letter_analysis.py
import os
import re
import docx # Read .docx files
import PyPDF2 # Read .pdf files
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import easyocr # Read jpegs

list_of_demand_letters = [] # total list of all letters and their locations

## PRE-PROCESSING RAW DIRECTORIES AND FILES ############################
def getListOfChildDirectories(parent_directory):
	# Get a list of child directories to make text files for from the root
	sub_directories = []
	for sub_dir in os.listdir(parent_directory):
		if sub_dir != ".gitignore" and "file_output.txt" not in sub_dir:
			sub_directories.append(sub_dir)
	return sub_directories

def getListOfLettersFromDirectory(path_directory):
	# get all the letters from a directory
	print("Directories = {0}".format(path_directory))
	for file_name in os.listdir(path_directory):
		if file_name != ".gitignore" and "file_output.txt" not in file_name:
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

	is_skipped = False # TODO: for memory reasons, skip any docs with too many pages
	if  os.path.getsize(docx_file_path) > 1251350: # size of memory
		is_skipped = True

	if not is_skipped:
		doc_letter = docx.Document(docx_file_path)

		for paragraph in doc_letter.paragraphs:
			paragraph_of_text = paragraph.text
			## TODO: Clean up unicode values from strings
			#paragraph_of_text = paragraph.text.replace('\u9679', "") # remove ●
			file_as_text += paragraph_of_text
	else:
		file_as_text = ''

	return file_as_text, is_skipped

def convertPDFToText(pdf_file_path):
	# return a text string of pdf file
	is_skipped = False # TODO: for memory reasons, skip any PDFS with too many pages
	if os.path.getsize(pdf_file_path) > 344000: # size of memory to prevent crashes
		is_skipped = True

	if not is_skipped:
		pdf_image_list = [] # list of all pages as images
		pdf_pages = convert_from_path(pdf_file_path, 500) # 500 DPI

		# Iterate through pages and store as a temporary image
		for page_number, page in enumerate(pdf_pages):
			# Store pdf file as an image
			pdf_filename = "{0}_page_{1}.jpg".format(pdf_file_path.split("/")[-1], page_number)
			#print(pdf_filename)
			page.save(pdf_filename, "JPEG")
			pdf_image_list.append(pdf_filename)
		
		# Iterate through images stored and convert image to text
		# Convert PDF to an Image and then use OCR(Optical Character Recognition) to return text
		for pdf_image in pdf_image_list:
			pdf_text = str(((pytesseract.image_to_string(Image.open(pdf_image)))))
			#print(pdf_text)
		
		# Iterate through and remove images
		for temp_image in pdf_image_list:
			os.remove(temp_image) # clean up
	else:
		pdf_text = ''

	return pdf_text, is_skipped

def convertJPEGToText(jpeg_file_path):
	# return a text string of jpeg file
	is_skipped = False # TODO: for memory reasons, skip large JPEGs
	if os.path.getsize(jpeg_file_path) > 444000: # size of memory to prevent crashes
		is_skipped = True
	
	if not is_skipped:
		# Iterate through images stored and convert image to text
		# Use OCR(Optical Character Recognition) to return text
		reader = easyocr.Reader(lang_list=['en'], gpu=False, verbose=False)
		jpeg_text = reader.readtext(jpeg_file_path, detail=0, batch_size=2, paragraph=True)
		jpeg_text = " ".join(jpeg_text)
	else:
		jpeg_text = ''

	return jpeg_text, is_skipped

########################################################################

#TODO: clean up documents with unicode values and non-alphabetical characters
#TODO: fix reading of JPEGs

if __name__ == '__main__':
	# track time of python program
	import time
	start_time = time.time()
	# reference to all demand letters stored in demand_letters/
	root_directory = "demand_letters"
	getListOfLettersFromDirectory(root_directory)
	print("Total Letters = {0}\n".format(len(list_of_demand_letters)))

	# Get File Types for all letters
	extension_dict = getFileTypes()
	#print(list(extension_dict.keys()))
	print("File types: {0}\n".format(extension_dict))

	skipped_files_too_large = []

	# Create text files for each parent directory for file output
	child_directories = getListOfChildDirectories(root_directory)
	child_direct_dict = {} # { directory_name : "file_output_name.txt"
	for sub_dir in child_directories:
		sub_dir_name = str(sub_dir)
		file_output_name = sub_dir_name.replace(" ", "_").lower() + ".txt" # converts "2020 Letters" to "2020_letters.txt"
		child_direct_dict[sub_dir] = file_output_name
		with open(os.path.join("demand_letters_output", file_output_name), "w") as output_file:
			output_file.write("")

	# Store text as a list object for a file to be written at the end
	file_output_dict = {} # {file_name.txt : ["text string"]}
	for file_output_text_name in child_direct_dict.values():
		file_output_dict[file_output_text_name] = [] # set to empty list to be populated with each file_letter
	
	for i, file_letter in enumerate(list_of_demand_letters):
		#print("Processing: {0} [{1}]...".format(file_letter, os.path.getsize(file_letter)))
		file_to_write_to = child_direct_dict[file_letter.split("/")[1]]
		extension = file_letter.split(".")[-1]

		if extension == "docx":
			'''docx_text, is_docx_skipped = convertDocxToText(file_letter)
			file_output_dict[file_to_write_to].append(docx_text)
			if not is_docx_skipped:
				print("{0}/{1} - {2}".format(i, len(list_of_demand_letters), file_letter))
			else:
				skipped_files_too_large.append(file_letter)
				print("{0}/{1} - {2} -- SKIPPED".format(i, len(list_of_demand_letters), file_letter))
				'''

		if extension == "pdf":
			'''
			pdf_text, is_pdf_skipped = convertPDFToText(file_letter)
			file_output_dict[file_to_write_to].append(pdf_text)
			if not is_pdf_skipped:
				print("{0}/{1} - {2}".format(i, len(list_of_demand_letters), file_letter, os.path.getsize(file_letter)))
			else:
				skipped_files_too_large.append(file_letter)
				print("{0}/{1} - {2} -- SKIPPED".format(i, len(list_of_demand_letters), file_letter, os.path.getsize(file_letter)))
			#break'''

		if extension == "jpeg":
			print("Processing: {0} [{1}]...".format(file_letter, os.path.getsize(file_letter)))
			jpeg_text, is_jpeg_skipped = convertJPEGToText(file_letter)
			file_output_dict[file_to_write_to].append(jpeg_text)
			if not is_jpeg_skipped:
				print("{0}/{1} - {2}".format(i, len(list_of_demand_letters), file_letter))
			else:
				skipped_files_too_large.append(file_letter)
				print("{0}/{1} - {2} -- SKIPPED".format(i, len(list_of_demand_letters), file_letter))
			print(jpeg_text)

		# Any other file types will be excluded
		if extension != "docx" and extension != "pdf" and extension != "jpeg":
			print("Unsupported file type for conversion: {0}".format(file_letter)) # print out additional file types for testing

	#print(file_output_dict)
	# Save long text list as a text file to improve preformance
	for file_output_name, file_output_text_list in file_output_dict.items():
		#print("{0} Files Saved as Text = {1}".format(file_output_name, len(file_output_text_list)))
		with open(os.path.join("demand_letters_output", file_output_name), "w") as write_text_file:
			# convert list to text version of list
			for text in file_output_text_list:
				write_text_file.write(str(text)) # overwrite
				write_text_file.write("\n")
	print("\nSkipped Files Due to MemoryError [{0}]: {1}".format(len(skipped_files_too_large), skipped_files_too_large))
	
	print("\nRuntime: {0:04f} minutes".format((time.time() - start_time)/60))

