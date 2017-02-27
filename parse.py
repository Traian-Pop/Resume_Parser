#!/usr/bin/env python

#Takes in the processed text files and parses
#them to get their respective metric data based on
#pre-defined categories

#These categories include researched and proven
#aspects of what makes a resume "good".

#The main method takes in a folder and processes
#all the txt files inside of the folder.

import glob, os
import docx2txt
import enchant
import re
import sys
import math
from sklearn.cluster import KMeans
import numpy as np
from fuzzywuzzy import fuzz
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO

#convert pdf to txt
def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    text = retstr.getvalue()
    fp.close()
    device.close()
    retstr.close()
    return text

#convert files to txt
def document_to_text(filename, file_path):
    # .docx case
    if filename[-5:] == ".docx":
        text = docx2txt.process(filename)
        docText = text.encode('utf-8')
        return docText

    # .pdf case
    elif filename[-4:] == ".pdf":
        return convert_pdf_to_txt(file_path)

#distance formula
def distance(coor1, coor2):
    xVal = coor2[0] - coor1[0]
    yVal = coor2[1] - coor1[1]
    return math.sqrt(xVal**2 + yVal**2)

# test method for the test resume
def test(argv):
    #return values
    xValue = 0.0
    yValue = 0.0

    #sets spell checker
    d = enchant.Dict("en_US")

    #transforms resume file into txt
    text_file = open(os.path.basename(argv)+".txt", "w")
    data = document_to_text(argv, argv)
    text_file.write(str(data))
    text_file.close()

    #initializing member data
    pronouns = ["he", "she", "they", "it", "we", "who"]
    pronVal = 7
    articles = ["an", "a", "the"]
    artVal = 7
    spellVal = 0
    phoneCheck = False
    emailCheck = False
    quantitative = 0.0
    buzzList = []
    buzzVal = 0.0
    absBuzz = 13.88
    absSpell = 360.38
    absQuan = 11.92
    buzz_file = open("buzz.txt","r")
    data = buzz_file.read()
    for word in data.split():
        buzzList.append(word)

    #calculate first metric
    #fuzzy similarity between the text, x-coordinate
    total = 0
    text_file = open(argv,"r")
    data = text_file.read()
    for fileN in glob.iglob('Resumes-Good/*'):
        good_file = open(fileN, "r")
        key = good_file.read()
        total += fuzz.token_sort_ratio(data, key)
    xValue = (total / 10)

    #calculate second metric
    #positive resume trends, y-coordinate
    total = 0
    data = text_file.read()
    for word in data.split():
        #checks phone number
        pattern = re.compile("(\d{3}[-\.\s]\d{3}[-\.\s]\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]\d{4}|\d{3}[-\.\s]\d{4})")
        if pattern.match(word) is not None and not phoneCheck:
            total += 7
            phoneCheck = True
        #checks for lack of articles
        if word in articles and artVal > 0:
            artVal -= 1
        #checks for lack of pronouns
        if word in pronouns and pronVal > 0:
            pronVal -= 1
        #checks word for spelling
        if d.check(word):
            spellVal += 1.0
        #checks for email
        pattern = re.compile("[^@]+@[^@]+\.[^@]+")
        if pattern.match(word) is not None and not emailCheck:
            total += 7
            emailCheck = True
        #checks for quantitative
        if word.isdigit():
            quantitative += 1.0
        #checks for buzzwords
        if word in buzzList:
            buzzVal += 1.0
    #add values
    total += pronVal
    total += artVal
    if quantitative <= 11.92:
        total += (quantitative / absQuan) * 7
    else:
        total += 7
    if spellVal <= 360.36:
        total += (spellVal / absSpell) * 7
    else:
        total += 7
    if buzzVal <= 13.88:
        total += (buzzVal / absBuzz) * 7
    else:
        total += 7
    #assigns values
    yValue = total
    return [xValue, yValue]

# main
def main(argv):
    #sets spell checker
    d = enchant.Dict("en_US")

    #transforming data into txt
    for filename in glob.iglob('Resumes-Raw/*'):
        text_file = open("Resumes-Txt/"+os.path.basename(filename)+".txt", "w")
        data = document_to_text(filename, filename)
        text_file.write(str(data))
        text_file.close()

    #initializing member data
    pronouns = ["he", "she", "they", "it", "we", "who"]
    pronVal = 7
    articles = ["an", "a", "the"]
    artVal = 7
    spellVal = 0
    phoneCheck = False
    emailCheck = False
    quantitative = 0.0
    buzzList = []
    buzzVal = 0.0
    absBuzz = 13.88
    absSpell = 360.38
    absQuan = 11.92
    buzz_file = open("buzz.txt","r")
    data = buzz_file.read()
    for word in data.split():
        buzzList.append(word)

    #calculate first metric
    #fuzzy similarity between the text, x-coordinate
    xval = {}
    for filename in glob.iglob('Resumes-Txt/*'):
        total = 0
        text_file = open(filename,"r")
        data = text_file.read()
        for fileN in glob.iglob('Resumes-Good/*'):
            good_file = open(fileN, "r")
            key = good_file.read()
            total += fuzz.token_sort_ratio(data, key)
        xval[filename] = (total / 10)

    #calculate second metric
    #positive resume trends, y-coordinate
    yval = {}
    for filename in glob.iglob('Resumes-Txt/*'):
        total = 0
        text_file = open(filename,"r")
        data = text_file.read()
        for word in data.split():
            #checks phone number
            pattern = re.compile("(\d{3}[-\.\s]\d{3}[-\.\s]\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]\d{4}|\d{3}[-\.\s]\d{4})")
            if pattern.match(word) is not None and not phoneCheck:
                total += 7
                phoneCheck = True
            #checks for lack of articles
            if word in articles and artVal > 0:
                artVal -= 1
            #checks for lack of pronouns
            if word in pronouns and pronVal > 0:
                pronVal -= 1
            #checks word for spelling
            if d.check(word):
                spellVal += 1.0
            #checks for email
            pattern = re.compile("[^@]+@[^@]+\.[^@]+")
            if pattern.match(word) is not None and not emailCheck:
                total += 7
                emailCheck = True
            #checks for quantitative
            if word.isdigit():
                quantitative += 1.0
            #checks for buzzwords
            if word in buzzList:
                buzzVal += 1.0
        #add values
        total += pronVal
        total += artVal
        if quantitative <= 11.92:
            total += (quantitative / absQuan) * 7
        else:
            total += 7
        if spellVal <= 360.36:
            total += (spellVal / absSpell) * 7
        else:
            total += 7
        if buzzVal <= 13.88:
            total += (buzzVal / absBuzz) * 7
        else:
            total += 7
        #resets values
        emailCheck = False
        phoneCheck = False
        pronVal = 7
        artVal = 7
        quantitative = 0.0
        spellVal = 0.0
        buzzVal = 0.0
        yval[filename] = total

    #combines both metrics
    coordinates = []
    for k, v in xval.iteritems():
        if k in yval.keys():
            coordinates.append([v, yval[k]])

    #kmeans clustering
    kmeans = KMeans(n_clusters=2, random_state=0).fit(coordinates)

    #test methods, returns coordinates of test resume
    coorTest = test(argv)

    #tests rating of the entered resume
    calcVal = 0.0
    skew = ""
    coorGood = kmeans.cluster_centers_[0]
    coorBad = kmeans.cluster_centers_[1]
    rangeTrend = distance(coorGood, coorBad)
    testGood = distance(coorTest, coorGood)
    testBad = distance(coorTest, coorBad)
    if testGood > testBad:
        calcVal = testBad / testGood
    elif testGood <= testBad:
        calcVal = testGood / testBad
    rating = (1 - calcVal) * 100
    if coorTest[0] > coorTest[1]:
        skew = "Content"
    elif coorTest[1] >= coorTest[0]:
        skew = "Format"

    #output
    print "Entered resume: " + argv
    print "The resume's rating is: " + str(rating)
    print "Your resume is better at: " + skew
    if 0 <= rating and rating < 25:
        print "You need to improve!"
    elif 25 <= rating and rating < 50:
        print "Could be better."
    elif 50 <= rating and rating < 75:
        print "Very good!"
    elif 75 <= rating and rating < 100:
        print "Hey, can you get me a job at Google?"

#run the program
main(sys.argv[1])
