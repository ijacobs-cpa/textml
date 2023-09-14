#!/usr/bin/env python3

import time
import sys
import os

class Metadata:
    version = "v0.1.1"

def writeHTML5Header():
    header = "<!doctype html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"utf-8\">\n  <title>Filename</title>\n  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n</head>\n"    

    return header

def defaultDirSetup():
    if os.path.isdir("textml"):         # Check if output dir exists
        oldFiles = os.listdir("textml") # Removing each file in dir before deleting
        if len(oldFiles) > 0:
            for file in oldFiles:
                os.remove("textml/" + file)

        os.rmdir('textml')      # Removing directory

    os.mkdir('textml')      # Recreating directory

def convertHTML(file, outDir, isDir = False):
    fo = open(file, "r")    # Opening file to process for writing 

    if isDir == True:           # Removing input directory from filename if its in a directory
        pos = file.index('/')
        # print(file[pos + 1:])
        file = file[pos + 1:]

    pos = file.index('.')           # Removing old extenstion 
    newHTMLFile = file
    newHTMLFile = newHTMLFile[0:pos]

    fw = open(outDir + newHTMLFile + ".html", 'w')      # Writing new html file to output directory

    fw.write(writeHTML5Header())       # HTML header
    fw.write("<body>\n")

    line = fo.readline()
    while line:
        # print(len(line.rstrip('\n')))
        if (len(line.rstrip('\n')) > 0):                        # Checking for empty line
            fw.write("  <p>" + line.rstrip('\n') + "</p>\n")    # Writing line of text as HTML
        else:
            fw.write("  <br />\n")        # Replacing empty line with <br>
            
        line = fo.readline()
    
    fw.write("</body>\n")
    fw.write("</html>\n")

    fo.close()      # Closing filestreams
    fw.close()

def main():
    # print(sys.argv[1])
    # print(len(sys.argv))

    if len(sys.argv) == 1:                                              # Invalid or missing arguments handling 
        raise Exception("ERROR!: No agruments passed to file")
    elif len(sys.argv) != 2:
        raise Exception("ERROR!: More than 1 file/argument passed to program")

    outDir = "textml/"              # Setting default output directory
    defaultDirSetup()               # Clearing and remaking directory

    userInput = sys.argv[1]      

    if userInput.find(".") != -1:               # Checking if the passed argument is a file
        if ".txt" in userInput:
            convertHTML(userInput, outDir, True)
        else: 
            Exception("Error!: Invalid file type")
    elif (os.path.isdir(userInput)):    # If not a file check if it is a directory                                     
        inputFiles = os.listdir(userInput)              # Retriving list of all files in directory

        for file in inputFiles:
            if ".txt" in file:                                  # Checking if each file's type is supported before converting
                convertHTML(userInput + file, outDir, True)     
            else: 
                raise Exception("Error!: Invalid file type")    

    else: # If not a found file or directory check for supported argument 
        if userInput == "-v" or userInput == "--version":   
            md = Metadata()
            print("\ntextml " + Metadata.version)
        elif userInput == "-h" or userInput == "--help":        
            print("textml " + Metadata.version)
            print("Usage:\n python3 main.py <commands> [input files]\n")
            print("Optional Commands:")
            print("------------------")
            print("-v,--version - Prints the current version of the program")
            print("-h,--help - Prints a help message for the program")
        else:
            print("\nInvalid arguments provided!\nUse --help or -h flag for more info")

if (__name__ == "__main__"):
    main()