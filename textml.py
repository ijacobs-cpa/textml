#!/usr/bin/env python3

import sys
import os

class Metadata:
    version = "v0.1.5"

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

    pos = file.find('/') 
    while pos != -1:        # Removing input directory from filename if its in a directory                            
        file = file[pos + 1:]
        pos = file.find('/') 


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
    limiter = 0
    while line:
        # print(len(line.rstrip('\n')))
        if (len(line.rstrip('\n')) > 0):                        # Checking for empty line
            fw.write("  <p>" + line.rstrip('\n') + "</p>\n")    # Writing line of text as HTML
            limiter = 0
        elif limiter == 0:
            fw.write("  <br />\n")        # Replacing empty line with <br> (limiting to 1 per double newline)
            limiter = 1
            
        line = fo.readline()
    
    fw.write("</body>\n")
    fw.write("</html>\n")

    fo.close()      # Closing filestreams
    fw.close()

# function for handling arguments
def command_args(usrArg):
    if usrArg == "-v" or usrArg == "--version":   
        md = Metadata()
        print("\ntextml " + Metadata.version)
    elif usrArg == "-h" or usrArg == "--help":        
        print("textml " + Metadata.version)
        print("\nUsage:\n python main.py [file/directory] <commands> [command-argument]\n     or\n python main.py <commands>\n")   
        print("Optional Commands:")
        print("------------------")
        print("-v,--version - Prints the current version of the program")
        print("-h,--help - Prints a help message for the program")
        print("-o,--output <output_folder> - Sets the output path of html files to the specified folder (Creates folder if doesnt exist)")
        print("     Ex. python main.py myFile.txt --output outDir/\n")

    else:
        print("\nInvalid arguments provided!\nUse --help or -h flag for more info")

# process MD files
def write_MD_to_html(new_content, new_title): # this provides the layout of the html with an editable title, content and css style

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{new_title}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
  {new_content}
</body>
</html>"""
    

    return html_content

def markdownfeat(input_filename):
    with open(input_filename, 'r') as input_file:
        # Read the content of the input file
        lines = input_file.readlines()


    # Initialize an empty list to store modified lines
    modified_lines = []

    for line in lines:
        # Remove leading and trailing whitespace from each line
        line = line.strip()

        if line.startswith('#'):
            if line.startswith('##'):
                modified_lines.append(f'<h2>{line[2:].strip()}</h2>')
            else:
                modified_lines.append(f'<h1>{line[1:].strip()}</h1>')

        # Check if the line starts with '['
        elif line.startswith('[') or line.startswith('*') or line.startswith('**') or line.startswith('#') or line.startswith('##'):
            modified_lines.append(line)  # Append the line as is (if it does not meet the conditions)
        else:
            # Check if the line is empty
            if not line:
                modified_lines.append('<br>')  # Insert a single <br> tag for empty lines
            else:
                # Wrap the line with <p> tags and append it to the modified_lines list
                modified_lines.append(f'<p>{line}</p>')
        

    # Join the modified lines with line breaks
    content = '\n'.join(modified_lines)

    # Convert double ** to bold
    content = content.replace('**', '<strong>', 1)
    content = content.replace('**', '</strong>', 1)

    # Convert single * to italics
    content = content.replace('*', '<em>', 1)
    content = content.replace('*', '</em>', 1)

    # Convert links format with HTML links (you need to define the markdown_to_html_links function)
    content = markdown_to_html_links(content)

    
    return content

def markdown_to_html_links(content):
    # Find and replace links and format with HTML links
    while '[' in content and ']' in content:
        start_index = content.find('[') # finds the first intance of the symol and assignt it in the start index
        end_index = content.find(']') # finds the first intance of the symol and assignt it in the end index

        if start_index < end_index:
            link_text = content[start_index + 1:end_index] #extract the text substring and place it as the text link
            link_url = content[end_index + 1:]#extract the text substring and place it as the link url

            link_url = link_url.strip('[]') #removes the text between []

            link_html = f'<a href="{link_url}">{link_text}</a>' # creates the syntax

            content = content[:start_index] + link_html + content[end_index + len(link_url) + 2:] # assign the syntaxt to the content
        else:
            content = content.replace(']', '', 1) #replace the end syntax with a space

    return content

def extract_thet_title(input_md_file):

    with open(input_md_file, "r") as fo:
        lines = fo.readlines()

           
    title = ""     # This will find the first non empty line in the document
    for line in lines[:3]:
        line = line.strip()  # Remove all of the leading/trailing whitespace
        if line:
            title = line
            break

    return title

def convertMD(userInput, outDir):
    # Create the output directory if it doesn't exist
    if not os.path.exists(outDir):
        os.makedirs(outDir)

    # Define the input Markdown file path
    input_md_file = userInput

    
    fil__name_noEx = extract_thet_title(input_md_file) # extract the title from the document

    # Define the output HTML file path by replacing the extension
    output_html_file = os.path.join(outDir, os.path.splitext(os.path.basename(userInput))[0] + '.html')

    # Call your Markdown to HTML conversion function
    body = markdownfeat(input_md_file)

    # Convert the Markdown body to HTML and write it to the output HTML file
    content = write_MD_to_html(body, fil__name_noEx)

    with open(output_html_file, 'w') as output_file:
        output_file.write(content)

        
def main():
    if len(sys.argv) == 1:                                              # Invalid or missing arguments handling 
        raise Exception("ERROR!: No agruments passed to the program")

    done = False
    userInput = sys.argv[1]      
    outDir = "textml/"              # Setting default output directory

    # Checking for any additional flags besides text file/folder
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
        elif ".md" in userInput:                                #if the file is md and output in the right directory
            convertMD(userInput, outDir)
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
            elif ".md" in file:                                  # Checking if each file's type is supported before converting
                convertMD(userInput + file, outDir) 
                done = True    
            else: 
                print("Error!: Invalid file type for: " + file)

    if done != True:            # If not a found file or directory check for supported argument 
        command_args(userInput)

if (__name__ == "__main__"):
    main()