import argparse
import sys
import tomli

class Metadata:
    version = "v0.1.7"

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

# Argument parsing below 
parser = argparse.ArgumentParser(description="Program accepts any .txt/.md file or a folder/directory of .txt/.md files and converts them to HTML files for use in webpages.")

parser.add_argument(
    '-v', '--version', 
    action='version', 
    version="textml " + Metadata.version
)
parser.add_argument(
    'input', 
    metavar='input', 
    type=str, 
    help="The provided .txt/.md file or a folder/directory of .txt/.md files to be converted"
)
parser.add_argument(
    '-o','--output', 
    metavar='output', 
    type=str, 
    default="til/", 
    help="Optionally specifies a directory to save converted HTML files (Creates folder if one does not exist"
)
parser.add_argument(
    '-l','--lang', 
    metavar='lang', 
    type=str, 
    default="en-CA", 
    help="Specifies a language for the <html lang=...> element in the <html> root element"
)
parser.add_argument(
    '-c','--config', 
    metavar='config', 
    type=str, 
    help="Allows to specify all the options in a TOML formatted configuration file instead of having to pass them all as command line arguments every time."
)

args = parser.parse_args()

if args.config is not None:
        args = read_config_file(args, args.config)
