import random
import reportlab.lib.pagesizes
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color
from reportlab.lib.utils import ImageReader
from PyPDF2 import PdfWriter, PdfReader
import requests
from bs4 import BeautifulSoup
from io import BytesIO
import os
from typing import TextIO
import json


HALF_LETTER_LANDSCAPE = (8.5 * 72, 5.5 * 72)  # Width x Height in points (1 inch = 72 points)
CHAR_SIZE_X = 10

class DataFromUser:
    def __init__(self):
        self.usernameInsta = ""
        self.passwordInsta = ""
        self.ytbId = ""
        self.lastPdf = None
        self.newPdf = {}
        #know data from last PDF
        self.knowData = {}
        self.bilData = GenerateBilanData()

class GenerateBilanData:
    def __init__(self,
                 instaPDF=True,
                 ytbPDF=True,
                 fbPDF=True,
                 pintPDF=True,
                 followerByAgeGraph=True,
                 followerByCountryGraph=True,
                 followerByCityGraph=True):
        self.instaPDF = instaPDF
        self.ytbPDF = ytbPDF
        self.fbPDF = fbPDF
        self.pintPDF = pintPDF
        self.followerByAgeGraph = followerByAgeGraph
        self.followerByCountryGraph = followerByCountryGraph
        self.followerByCityGraph = followerByCityGraph


BLACK_COLOR = Color(0, 0, 0)

ROUND_RECT_COLOR = Color(174 / 255, 226 / 255, 255 / 255)
ROUND_RECT_SIZE = 145
MIDDLE_RECT = ROUND_RECT_SIZE/2

def GetMiddlePosition(c, text):
    textWidth = c.stringWidth(text, c._fontname, c._fontsize)

    return textWidth/2

def DrawTextAtMiddle(xPos, yPos, text, c):
    xPos -= GetMiddlePosition(c, text)
    c.drawString(xPos, yPos, text)


def WriteDictToFile(data, filename, writeType='w'):
    with open(filename, writeType, encoding='utf-8') as file:
        for key, value in data.items():
            file.write(f"{key} {value}\n")


def InstaListToFile(instaList, file, writeType='w'):
    for data in instaList:
        print(data.ToString())
        file = f'{file} {data.ToString()} '

    return file


def FindFileName(directory, mode='next'):
    index = 0
    lastIndex = -1

    while True:
        file_name = f"{index}.txt"
        file_path = os.path.join(directory, file_name)

        if mode == 'next':
            if not os.path.exists(file_path):
                return file_path
        elif mode == 'last':
            if os.path.exists(file_path):
                lastIndex = index
            else:
                return f"{directory}{lastIndex}.txt" if lastIndex != -1 else None

        index += 1