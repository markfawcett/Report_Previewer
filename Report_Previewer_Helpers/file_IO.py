# Standard library imports
from datetime import datetime
import os
from pathlib import Path
import webbrowser
from distutils import dir_util

# 3rd party imports
from lxml import html

# Local libraries
from . import feedback_v2 as feedback
from .settings import REQUIRED as Required


# Constants
OUTPUT_FOLDER = datetime.now().strftime('%Y-%b-%d @ %H-%M-%S')


# Functions
def check_requirements():

    error_message = "Can't run. Required files and/or folders are missing:\n\n   "
    missing_paths = ''

    for key, value in Required.items():

        if not Path(value).exists():
            # on posix systems especialy we may not be able to find relative paths if the
            # script is run from a directory other than the parent of the main script.
            # Next line will attempt to find the paths via first finding the path to
            # this script and then going from there.
            script_dir_plus_relative_path = Path(
                os.path.dirname(__file__)).parent.joinpath(value)
            if script_dir_plus_relative_path.exists():
                # update dictionary
                Required[key] = str(script_dir_plus_relative_path)
            else:
                missing_paths += '\u2022   ' + value + '\n\n   '

    if missing_paths:
        # feedback.writeln(error_message + missing_paths)
        feedback.error(error_message + missing_paths)
        exit()


def set_up(input_file):
    # create the output folder next t the input file
    output_folder = Path(input_file).parent.absolute()

    global OUTPUT_FOLDER
    OUTPUT_FOLDER = str(output_folder)



def write_html(htmlRoot, file_name, open_in_browser=True):
    # html.tostring can accept an encoding option. Default is 'None' which means for example that a non-breaking space is coded as '&#160;'


    output_file_path = Path(OUTPUT_FOLDER).joinpath(file_name)
    try:
        temp_string = html.tostring(htmlRoot, doctype='<!DOCTYPE html>')  # should be DOCTYPE
        output_file = open(output_file_path, 'w')
        output_file.write(temp_string.decode(encoding='UTF-8'))
        output_file.close()

    except Exception as err:
        feedback.writeln("Error:\twrite_html()\except0")

    try:
        if open_in_browser:
            if os.name == 'posix':
                webbrowser.open('file://' + str(output_file_path))
            else:
                webbrowser.open(str(output_file_path))
    except:
        pass


def copy_css_etc():
    try:
        Required['templates_dir']
        dir_util.copy_tree(Required['templates_dir'], OUTPUT_FOLDER)
    except:
        pass

