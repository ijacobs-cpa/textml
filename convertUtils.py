import os

def convertText(filePath, outDir):
    fo = open(filePath, "r")    # Opening file to process for writing 

    file = os.path.basename(filePath)                   # Getting basename of file
    newHTMLFile = os.path.splitext(file)[0] + ".html"   # Renaming new file to .html
    writePath = os.path.join(outDir, newHTMLFile)       # Getting new output directory

    fw = open(writePath, 'w')      # Writing new html file to output directory

    HTMLContent = ""
    title = parseTitle(fo, newHTMLFile)         # Getting the title from the file if it exists

    if title != os.path.splitext(newHTMLFile)[0]:       # Writing the title if it is not the filename
        HTMLContent += (" <h1>" + title + "</h1>\n")

    line = fo.readline()
    limiter = 0
    while line:
        if (len(line.rstrip('\n')) > 0):                        # Checking for empty line
            HTMLContent += ("  <p>" + line.rstrip('\n') + "</p>\n")    # Writing line of text as HTML
            limiter = 0
        elif limiter == 0:
            HTMLContent += ("  <br />\n")        # Replacing empty line with <br> (limiting to 1 per double newline)
            limiter = 1
            
        line = fo.readline()    # Reading next line
    
    finishedFile = write_html_content(HTMLContent, title)
    fw.write(finishedFile)

    fo.close()      # Closing filestreams
    fw.close()

def parseTitle(openFile, fileName):
    title = ""
    parseTitle = openFile.readlines()[0:3]    # Reading first 3 lines for title

    if parseTitle[1] == '\n' and parseTitle[2] == '\n':
        title = parseTitle[0].rstrip('\n')   # Getting title
        openFile.seek(len(parseTitle[0]) + 2, 0)      # Reseting file position to right before title
    else:
        title = os.path.splitext(fileName)[0]   # Getting file name without extension for title
        openFile.seek(0, 0)

    return title

# process MD files
def write_html_content(new_content, new_title): # this provides the layout of the html with an editable title, content

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

def markdownfeat(filestream, input_filename):
    
    # Initialize an empty list to store modified lines
    modified_lines = []

    fileName = os.path.basename(input_filename)     # Getting the base file
    title = parseTitle(filestream, fileName)  

    if title != os.path.splitext(fileName):     # Writing the title element if it is not a file name
        modified_lines.append("<h1>" + title + '</h1>\n')   # Writing found title to html

    # Read the content of the input file
    lines = filestream.readlines()

    for line in lines:
        # Remove leading and trailing whitespace from each line
        line = line.strip()

        if line.startswith('#'):
            if line.startswith('##'):
                modified_lines.append(f'<h2>{line[2:].strip()}</h2>')
            else:
                modified_lines.append(f'<h1>{line[1:].strip()}</h1>')

        # Check if the line starts with markdown prefixes
        elif line.startswith('[') or line.startswith('*') or line.startswith('**') or line.startswith('#') or line.startswith('##') or line.startswith("<h1>"):
            modified_lines.append(line)  # Append the line as is (if it does not meet the conditions)
        else:
            # Check if the line is empty
            if not line:
                modified_lines.append('<br/>')  # Insert a single <br> tag for empty lines
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

def convertMD(userInput, outDir):
    # Create the output directory if it doesn't exist
    if not os.path.exists(outDir):
        os.makedirs(outDir)

    # Define the input Markdown file path
    input_md_file = userInput

    # Define the output HTML file path by replacing the extension
    output_html_file = os.path.join(outDir, os.path.splitext(os.path.basename(userInput))[0] + '.html')
    # print(output_html_file)

    with open(input_md_file, 'r') as input_file:
        # Parse title name from html file
        title = parseTitle(input_file, input_md_file)
        # Call your Markdown to HTML conversion function
        body = markdownfeat(input_file, input_md_file)
        # Convert the Markdown body to HTML and write it to the output HTML file

    content = write_html_content(body, title)

    with open(output_html_file, 'w') as output_file:
        output_file.write(content)