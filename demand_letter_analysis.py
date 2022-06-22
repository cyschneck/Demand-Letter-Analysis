# Sentiment Analysis of Anti-Racism Letters
# python3 demand_letter_analysis.py
import os
import re
import docx # Read .docx files
#import PyPDF2 # Read .pdf files

list_of_demand_letters = [] # total list of all letters and their locations
list_of_demand_letters_as_text = [] # strings of text from letters

## PRE-PROCESSING RAW DIRECTORIES AND FILES ############################

def getListOfLettersFromDirectory(path_directory):
	# get all the letters from a directory
	print("Directories = {0}".format(path_directory))
	for file_name in os.listdir(path_directory):
		if file_name != ".gitignore" and file_name != "file_output.txt":
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
	#print(docx_file_path)
	doc_letter = docx.Document(docx_file_path)
	for paragraph in doc_letter.paragraphs:
		paragraph_of_text = paragraph.text
		## TODO: Clean up unicode values from strings
		#paragraph_of_text = paragraph.text.replace('\u9679', "") # remove ●
		file_as_text += paragraph_of_text
	return file_as_text

def convertPDFToText(pdf_file_path):
	# return a text string of pdf file
	#print(pdf_file_path)
	#letter_as_pdf = PyPDF2.PdfReader(pdf_file_path)
	#for page in letter_as_pdf.pages:
	#	print(page.extract_text())
	#	if page.getPageImagelist()

	# TODO: If text from image is a scanned file, use OCR (Optical Character Recognition)
	#sudo apt-get install tesseract-ocr

	import pytesseract
	from PIL import Image
	from pdf2image import convert_from_path

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
	for pdf_image in pdf_image_list:
		pdf_text = str(((pytesseract.image_to_string(Image.open(pdf_image)))))
		#print(pdf_text)
	
	# Iterate through and remove images
	for temp_image in pdf_image_list:
		os.remove(temp_image) # clean up
	return pdf_text

########################################################################

if __name__ == '__main__':
	# reference to all demand letters stored in demand_letters/
	root_directory = "demand_letters"
	getListOfLettersFromDirectory(root_directory)
	print("Total Letters = {0}\n".format(len(list_of_demand_letters)))

	# Get File Types for all letters
	extension_dict = getFileTypes()
	print(list(extension_dict.keys()))
	print("File types: {0}\n".format(extension_dict))


	for i, file_letter in enumerate(list_of_demand_letters):
		print("{0}/{1} - {2}".format(i, len(list_of_demand_letters), file_letter))
		extension = file_letter.split(".")[-1]
		if extension == "docx":
			list_of_demand_letters_as_text.append(convertDocxToText(file_letter))
		if extension == "pdf":
			list_of_demand_letters_as_text.append(convertPDFToText(file_letter))
			break
		if extension != "docx" and extension != "pdf":
			print("Unsupported file type for conversion: {0}".format(file_letter)) # print out additional file types for testing

	# Save long text list as a text file to improve preformance
	#print(list_of_demand_letters_as_text)
	with open("demand_letters/file_output.txt", "w") as write_text_file:
		# convert list to text version of list
		for text in list_of_demand_letters_as_text:
			write_text_file.write(str(text)) # overwrite
			write_text_file.write("\n\n")
