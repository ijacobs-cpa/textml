#!/usr/bin/env python3

import os
import shutil

import bin.convertUtils as utils
from bin.cli import args as ARGS

class ConvertProperties:                            # Properties for converted file from commandline
    def __init__(this, userInput, outDir, lang):
        this.userInput = userInput
        this.outDir = outDir
        this.lang = lang

props = ConvertProperties(      # Instanced class of properties
    ARGS.input, 
    ARGS.output, 
    ARGS.lang
)  

def process_file(file, fileProps):      # Function to process file in proper file type
    ext = os.path.splitext(file)[1]

    if ext == ".txt":                                       # Checking if each file's type is supported before converting
        utils.convertText(file, props.outDir, props.lang)   # Text Conversion
    elif ext == ".md":                               
        utils.convertMD(file, fileProps.outDir, fileProps.lang) # Markdown conversion
    elif not os.path.isdir(file):                                                     # Prints error if file is not supported
        raise Exception("Error!: Invalid file type for: " + file + " (Expected .txt, .md)")

def directory_setup(dir):
    if os.path.isdir(dir):         # Check if output dir exists
        shutil.rmtree(dir)  # Removing directory and its contents

    os.mkdir(dir)      # Creating directory

def main():

    if (os.path.isdir(props.outDir) == False) or (props.outDir == "til/"):
        directory_setup(props.outDir)               # Clearing and remaking directory

    if os.path.isfile(props.userInput) is True:               # Checking if the passed argument is a file
        process_file(props.userInput, props)

    elif os.path.isdir(props.userInput) == True:    # If not a file check if it is a directory  

        inputFiles = os.listdir(props.userInput)              # Retriving list of all files in directory  

        for file in inputFiles:
            currFile = os.path.join(props.userInput, file)
            process_file(currFile, props)

    else:
        print(props.userInput + " file/directory does not exist!")
        exit(0)

if (__name__ == "__main__"):
    main()
