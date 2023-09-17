#!/usr/bin/env python3

import sys
import os

class Metadata:
    version = "v0.1.4"

def writeHTMLHeader(title):
    header = "<!doctype html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"utf-8\">\n  <title>" + title + "</title>\n  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n</head>\n<body>\n"    

    return header

def directory_setup(dir):
    if os.path.isdir(dir):         # Check if output dir exists
        oldFiles = os.listdir(dir) # Removing each file in dir before deleting
        if len(oldFiles) > 0:
            for file in oldFiles:
                os.remove(dir + "/" + file)

        os.rmdir(dir)      # Removing directory

    os.mkdir(dir)      # Creating directory

def convertText(file, outDir):
    fo = open(file, "r")    # Opening file to process for writing 

   
    pos = file.find('/')           # Removing input directory from filename if its in a directory
    if pos != -1:
        # print(file[pos + 1:])
        file = file[pos + 1:]

    pos = file.index('.')           # Removing old extenstion 
    newHTMLFile = file
    newHTMLFile = newHTMLFile[0:pos]

    fw = open(outDir + newHTMLFile + ".html", 'w')      # Writing new html file to output directory

    parseTitle = fo.readlines()[0:3]    # Reading first 3 lines for title

    if parseTitle[1] == '\n' and parseTitle[2] == '\n':
        fw.write(writeHTMLHeader(parseTitle[0].rstrip('\n')))       # HTML header as parsed title       
        fw.write("<h1>" + parseTitle[0].rstrip('\n') + '</h1>\n')   # Writing found title to html

        fo.seek(len(parseTitle[0]) + 2, 0)      # Reseting file position to right before title
    else:
        fw.write(writeHTMLHeader(newHTMLFile))       # HTML header as filename (for no title)
        fo.seek(0, 0)
    
    line = fo.readline()
    test = 0
    while line:
        # print(len(line.rstrip('\n')))
        if (len(line.rstrip('\n')) > 0):                        # Checking for empty line
            fw.write("  <p>" + line.rstrip('\n') + "</p>\n")    # Writing line of text as HTML
            test = 0
        elif test == 0:
            fw.write("  <br />\n")        # Replacing empty line with <br>
            test = 1
            
        line = fo.readline()
    
    fw.write("</body>\n")
    fw.write("</html>\n")

    fo.close()      # Closing filestreams
    fw.close()

def command_args(usrArg):
    if usrArg == "-v" or usrArg == "--version":   
        md = Metadata()
        print("\ntextml " + Metadata.version)
    elif usrArg == "-h" or usrArg == "--help":        
        print("\ntextml " + Metadata.version)
        print("Usage:\n python main.py <input-file | input-folder> <modifiers> [modifier value]\n     or\n python main.py <commands>\n")
        print("Modifiers:\n------------------\n-o,--output <output_folder> - Sets the output path of html files to the specified folder (Creates folder if doesnt exist)\n")
        print("Optional Commands:")
        print("------------------")
        print("-v,--version - Prints the current version of the program")
        print("-h,--help - Prints a help message for the program")
    else:
        print("\nInvalid arguments provided!\nUse --help or -h flag for more info")

def main():
    if len(sys.argv) == 1:                                              # Invalid or missing arguments handling 
        raise Exception("ERROR!: No agruments passed to the program")
    # elif len(sys.argv) != 2:
    #     raise Exception("ERROR!: More than 1 file/argument passed to program")

    done = False
    userInput = sys.argv[1]      
    outDir = "textml/"              # Setting default output directory

     # Checking for any additional flags
    if len(sys.argv) > 2:
        if len(sys.argv) <= 5:
            if sys.argv[2] == "-o" or sys.argv[2] == "--output":
                if len(sys.argv[3]) > 0:
                    outDir = sys.argv[3]
                else:
                    raise Exception("ERROR!: No output directory specified!\n Use -h,--help for more info.")

        else:
            raise Exception("ERROR!: Too many arguments passed to program")
        
    if (os.path.isdir(outDir) == False) or (outDir == "textml/"):
        directory_setup(outDir)               # Clearing and remaking directory

    if done != True or userInput.find(".") != -1:               # Checking if the passed argument is a file
        if ".txt" in userInput:
            convertText(userInput, outDir)
            done = True
        else: 
            Exception("Error!: Invalid file type")


    if done != True and os.path.isdir(userInput) == True:    # If not a file check if it is a directory  

        inputFiles = os.listdir(userInput)              # Retriving list of all files in directory

        if userInput[len(userInput) - 1] != '/':    # Adding a slash to diretory if not added already
            userInput += '/'

        for file in inputFiles:
            if ".txt" in file:                                  # Checking if each file's type is supported before converting
                convertText(userInput + file, outDir) 
                done = True    
            else: 
                raise Exception("Error!: Invalid file type") 

    if done != True:            # If not a found file or directory check for supported argument 
        command_args(userInput)

if (__name__ == "__main__"):
    main()