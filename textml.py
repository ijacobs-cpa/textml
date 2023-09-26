#!/usr/bin/env python3

import os
import argparse
import shutil

import convert_utils as utils

class Metadata:
    version = "v0.1.5"

def directory_setup(dir):
    if os.path.isdir(dir):         # Check if output dir exists
        shutil.rmtree(dir)  # Removing directory and its contents

    os.mkdir(dir)      # Creating directory
       
def main():
    outDir = "til/"              # Setting default output directory  

    parser = argparse.ArgumentParser(description="Program accepts any .txt/.md file or a folder/directory of .txt/.md files and converts them to HTML files for use in webpages.")

    parser.add_argument('-v', '--version', action='version', version="textml " + Metadata.version)
    parser.add_argument('input', metavar='input', type=str, help="The provided .txt/.md file or a folder/directory of .txt/.md files to be converted")
    parser.add_argument('-o','--output', metavar='output', type=str, help="Optionally specifies a directory to save converted HTML files (Creates folder if one does not exist")

    args = parser.parse_args()

    if args.output:
        outDir = args.output

    userInput = args.input

    if (os.path.isdir(outDir) == False) or (outDir == "til/"):
        directory_setup(outDir)               # Clearing and remaking directory

    if userInput.find(".") != -1:               # Checking if the passed argument is a file
        if ".txt" in userInput:
            utils.convertText(userInput, outDir)
        elif ".md" in userInput:                                #if the file is md and output in the right directory
            utils.convertMD(userInput, outDir)
        else: 
            raise Exception("Error!: Invalid file type")

    elif os.path.isdir(userInput) == True:    # If not a file check if it is a directory  

        inputFiles = os.listdir(userInput)              # Retriving list of all files in directory  

        for file in inputFiles:
            currFile = os.path.join(userInput, file)

            if ".txt" in file:                                  # Checking if each file's type is supported before converting
                utils.convertText(currFile, outDir) 
            elif ".md" in file:                                  # Checking if each file's type is supported before converting
                utils.convertMD(currFile, outDir) 
            else: 
                print("Error!: Invalid file type for: " + file)
    else:
        print("Directory: " + userInput + " does not exist!")

if (__name__ == "__main__"):
    main()