import os
import requests
from Common import *
import json
import base64
import re
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO

def GenerateParameters():
    data_instance = LoadSaveFile()
    data_dict = data_instance.__dict__.copy()
    data_dict['lastPdf'] = ""
    data_dict['newPdf'] = ""
    data = {'fileName': "test", 'saveFile': data_dict}
    return data


def LoadSaveFile():
    data = DataFromUser()
    data.bilData = ReadBilanStruct()

    with open("python/Data/data.json") as dataIdFile:
        dataJson = json.load(dataIdFile)
        data.usernameInsta = dataJson["instaName"]
        data.passwordInsta = dataJson["instaPassWord"]
        #data.ytbId = dataJson["YtbId"]

    last = f"python/localSaveData/{GetDirectoryHighIndex(increment=False)}/baseData.json"
    data.lastPdf = open(last, 'r')

    # get data from last month if the last PDF is valid
    for line in data.lastPdf:
        print(line)
        words = line.split()
        for i in range(len(words) - 1):
            current_word = words[i].replace('_', ' ')
            next_word = words[i + 1].replace('_', ' ')
            if current_word in data.knowData:
                if next_word not in data.knowData[current_word]:
                    data.knowData[current_word] = next_word
            else:
                data.knowData[current_word] = next_word
    return data


def ReadBilanStruct():
    blDataTab = [0, 0, 0, 0, 0, 0, 0]

    lineCounter = 0

    jsonDataName = ["generateInstagram","generateBestPosts", "generateAgeChart","generateGenderChart","generateCityChart","generateCountryChart"]

    with open("python/bilanSenderToPython/bilanSaveFile.json", 'r') as blFile:
        dataJson = json.load(blFile)
        for i in range(0, len(jsonDataName)):
            blDataTab[i] = dataJson[jsonDataName[i]]

    print(f'value of bilansavefile in program : {blDataTab}')
    
    # Initialize an empty list to store boolean values
    boolean_args = []

    # Iterate through blDataTab and append each boolean value to boolean_args
    for data in blDataTab:
        boolean_args.append(bool(data))

    # Call GenerateBilanData with unpacked boolean_args
    bilanData = GenerateBilanData(*boolean_args)

    return blDataTab

# Function to get the highest index directory in 'localSaveData'
def GetDirectoryHighIndex(base_path='python/localSaveData', increment=True):
    # List all directories in the base path
    directories = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]

    # Extract indices from directory names using regular expressions
    indices = []
    for directory in directories:
        match = re.search(r'\d+$', directory)
        if match:
            indices.append(int(match.group()))

    # Find the highest index
    highest_index = max(indices) if indices else 0
    if increment:
        highest_index += 1

    highest_index_directory = f'{highest_index}'

    return highest_index_directory


def RemoveAllFilesInDirectory(path="python/temp/"):
    try:
        # Ensure the directory exists
        if not os.path.exists(path):
            print(f"The directory {path} does not exist.")
            return
        
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            if os.path.isfile(file_path):  # Check if it is a file
                os.remove(file_path)
            elif os.path.isdir(file_path):
                print(f"{file_path} is a directory, skipping...")
    except Exception as e:
        print(f"An error occurred: {e}")


def MergeAllPdfsInOrder(outputFilePath):
    pdfs = [
        "0",
        "GraphGender",
        "GraphAge",
        "GraphCity",
        "GraphCountry",
        "BestPosts",
    ]
    path = 'python/temp'
    debutName = 'instagramPage'
    extension = 'pdf'

    pdf_writer = PdfWriter()

    for pdf in pdfs:
        filePath = f'{path}/{debutName}_{pdf}.{extension}'
        if os.path.exists(filePath):
            with open(filePath, 'rb') as opened:
                pdf_reader = PdfReader(opened)
                for page_num in range(len(pdf_reader.pages)):
                    pdf_writer.add_page(pdf_reader.pages[page_num])

    with open(outputFilePath, 'wb') as output_file:
        pdf_writer.write(output_file)

    print(f'PDFs have been merged into {outputFilePath}')