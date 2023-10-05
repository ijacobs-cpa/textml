#!/usr/bin/env python3

import os
import argparse
import shutil
import convertUtils as utils
import tomli
import sys

class Metadata:
    version = "v0.1.7"

def directory_setup(dir):
    if os.path.isdir(dir):         # Check if output dir exists
        shutil.rmtree(dir)  # Removing directory and its contents

    os.mkdir(dir)      # Creating directory

def read_config_file(original_args, file_path):
    """Parses the toml configuration file, returns the parsed options as a dictionary"""

    # Start with default arguments
    args = original_args

    # Read the TOML file
    try:
        with open(file_path, "rb") as file:
                custom_configuration = tomli.load(file)
    except tomli.TOMLDecodeError:
        sys.exit("Supplied TOML file is not valid.")
    except:
        sys.exit("File path supplied to --config or -c option is invalid.")

    # Set the specified options, use default if any not specified 
    for (key, value) in custom_configuration.items():
        setattr(args, key, value)

    return args

def main():
    outDir = "til/"              # Setting default output directory  
    lang = "en-CA"

    # Argument parsing below 
    parser = argparse.ArgumentParser(description="Program accepts any .txt/.md file or a folder/directory of .txt/.md files and converts them to HTML files for use in webpages.")

    parser.add_argument('-v', '--version', action='version', version="textml " + Metadata.version)
    parser.add_argument('input', metavar='input', type=str, help="The provided .txt/.md file or a folder/directory of .txt/.md files to be converted")
    parser.add_argument('-o','--output', metavar='output', type=str, help="Optionally specifies a directory to save converted HTML files (Creates folder if one does not exist")
    parser.add_argument('-l','--lang', metavar='lang', type=str, help="Specifies a language for the <html lang=...> element in the <html> root element")
    parser.add_argument('-c','--config', metavar='config', type=str, help="Allows to specify all the options in a TOML formatted configuration file instead of having to pass them all as command line arguments every time.")

    args = parser.parse_args()

    if args.config is not None:
        args = read_config_file(args, args.config)

    if args.output:
        outDir = args.output

    if args.lang:
        lang = args.lang
        
    userInput = args.input

    if (os.path.isdir(outDir) == False) or (outDir == "til/"):
        directory_setup(outDir)               # Clearing and remaking directory

    if userInput.find(".") != -1:               # Checking if the passed argument is a file
        if ".txt" in userInput:
            utils.convertText(userInput, outDir, lang)
        elif ".md" in userInput:                                #if the file is md and output in the right directory
            utils.convertMD(userInput, outDir, lang)
        else: 
            raise Exception("Error!: Invalid file type")

    elif os.path.isdir(userInput) == True:    # If not a file check if it is a directory  

        inputFiles = os.listdir(userInput)              # Retriving list of all files in directory  

        for file in inputFiles:
            currFile = os.path.join(userInput, file)

            if ".txt" in file:                                  # Checking if each file's type is supported before converting
                utils.convertText(currFile, outDir, lang) 
            elif ".md" in file:                                  # Checking if each file's type is supported before converting
                utils.convertMD(currFile, outDir, lang) 
            else: 
                print("Error!: Invalid file type for: " + file)
    else:
        print("Directory: " + userInput + " does not exist!")

if (__name__ == "__main__"):
    main()
