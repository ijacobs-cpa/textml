# textml
Convert textual notes into usable html.

# Features

Program accepts any .txt file or a folder/directory of .txt files and converts them to .html files for use in webpages.

More features to be included

# How to Install 

**In command line:**

Make sure python is installed:

`$ python --version`

Clone the Repo

```
$ git clone https://github.com/ijacobs-cpa/textml.git
$ cd textml/ 
```

run the program 

`$ python main.py <options> `

or

`$ python main.py [file/directory]`


## Examples
---

Converting a file:

`$ python main.py myfile.txt`

Converting all files in a directory:

`$ python main.py mydirectory/`

Running Commands:

`$ python main.py -v`

NOTE: Current version is still a WIP

# Command Flags

<!-- Available command options:
```
-v,--version - Displays the version of the program
-h,--help - Displays a help message
``` -->

| Command   | Description |
| --------- | ----------- |
| -v, --version | Displays version of the program |
| -h, --help | Displays a help message |

# Changelog

**0.1.3:**

- Now accepts folders passed without a "/"
- Added feature: *Title parsing*
    - Updates `<title></title>` & creates `<h1></h1>` based on title in txt document (title must be in the first line and have 2 newlines right after)
- Reduced amount of `<br/>` lines created

0.1.2:

- Updated help message
- Improved the defaultDirSetup() to accept custom directories for future features

0.1.1 - Fixed an Issue with relative filenames

0.1.0 - Initial Commit of project 

# License
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)




