import requests, os

flaskUrl = 'http://oharam29.pythonanywhere.com' # python anywhere 
#flaskUrl =  'http://127.0.0.1:5000/'
download_path = 'D:/ConcurrencyAssignment2/DownloadedFiles' # directory for downloads



def uploadFile(fileName): # upload file
	try:
		file = {'upload_file': open(fileName,'rb')}
		response = requests.post(
			flaskUrl+'/upload',
    		files=file
		)
		print(response.content)	
	except Exception as e:
		print('File {} cannot be found'.format(fileName))
	

def chunkfile(fileName,valuePairs): # chunk file
	try:

		print("Chunking {}".format(fileName))
		response = requests.get(
    		flaskUrl+'/chunk',
    		params={'fileName': fileName,'valuePairs' : valuePairs}
		)	

	except Exception as e:
		print("Invalid response from server")
	return response.content


def downloadFile(fileName):

	response = requests.get(
		flaskUrl+'/download',
    	params={'fileName': fileName}
	)
	fileName = fileName.decode("utf-8")
	outputFile = open(os.path.join(download_path, fileName),"w",encoding="utf8") #  creates output file
	for line in response.text:
		outputFile.write(line)
	outputFile.close()
	print("File downloaded")


def ListServerFiles(): # list all files uploaded to the server
	response = requests.get(
		flaskUrl+'/uploadedFiles'
		)
	
	files = (response.content.decode()).split("\n")
	print("Uploaded Files on server: ")
	for f in files:
		print(f) 


def ChunkRandom(num): # chunk random file
	try:
		print("Generating Random Chunk")
		response = requests.get(
    		flaskUrl+'/Random',
    		params={'num':num}
		)
		return response.content
	except Exception as e:
		print("Invalid response from server")
	return ""
	


# start client
while True:
	
	print("Commands : Chunk [Letter - Letter ],Random ,Upload ,Stop") # pick command
	text = input("Input Command: ")

	if ( text == "Chunk"):

		print("You entered: Chunk")
		fileChoice = input("Would you like to chunk: the Default file (command: Default), Choose file from server (command: Choose) or Upload file (command: Upload)?: ")
		
		try:
			valuePairs = ""		
			NumOfChunks = input("Input number of chunks: ")
			for i in range(int(NumOfChunks)):
				val1 = input("Input Starting Letter of chunk {} : ".format(i+1)) # value between two letters of the alphabet
				val2 = input("Input Finishing Letter of chunk {} : ".format(i+1))
				valuePairs += val1 + val2

			try:
			
				if( fileChoice == "Default"):
					fileName = "default.txt" # use default input
				
				elif( fileChoice == "Choose"):
					ListServerFiles()
					fileName = input("Choose file name: ") # pick file from the server

				elif( fileChoice == "Upload"): # upload file
					fileName = input("Input file name to upload: ")
					uploadFile(fileName)
		
				file = chunkfile(fileName, valuePairs)

				if(file.decode("utf-8") != "Values not in File"):
					choice = input("File Chunked Successfully, Would you like to download?(y/n)")
					if( choice == "y"):
						downloadFile(file)

			except:
				print("Invalid input")

		except Exception as e:
			print("Invalid entry")

		

	elif( text == "Random"):
		nums = input("how many chunks: ")
		file = ChunkRandom(int(nums))
		choice = input("File Chunked Successfully, Would you like to download?(y/n)")
		if( choice == "y"):
			downloadFile(file)
		
	elif( text == "Upload" ):
		fileName = input("Input file name: ")
		uploadFile(fileName)

	elif( text == "Stop"):
		break
	
	else:
		print("Invalid input")