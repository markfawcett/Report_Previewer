# Standard library imports
import datetime
import os
import sys

# Constants
GUID = str(datetime.datetime.now()).replace(':', '-').replace('.', '-')
USERNAME = os.getlogin()
ONLINE_FEEDBACK_DIRECTORY = 'A:\\Document Drive WPU and TSO\\Report Timings\\'
OFFLINE_FEEDBACK_DIRECTORY = 'C:\\Users\\' + USERNAME + '\\report-script-feedback\\'


# classes
class bcolors:
    HEADER = '\033[95m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Functions
def warning(msg):

    print(f'{bcolors.WARNING}WARNING:{bcolors.ENDC}  {msg}')
    # messagebox.showerror("Error", error_text)


def error(msg):

    print(f'{bcolors.FAIL}EORROR:{bcolors.ENDC}  {msg}')
    if 'tkinter' in sys.modules:
        import tkinter as tk
        from tkinter import messagebox
        # supress root window
        root = tk.Tk()
        root.overrideredirect(1)
        root.withdraw()
        messagebox.showerror("Error", msg)
        exit()


def writeln(line_of_feedback):
    for directory in (OFFLINE_FEEDBACK_DIRECTORY, ONLINE_FEEDBACK_DIRECTORY):
        try:
            if os.name != 'posix':
                if not os.path.exists(directory):
                    os.mkdir(directory)
                feedback_file = open(directory + GUID + '.txt', 'a')
                feedback_file.write(str(datetime.datetime.now()) + "\t" + line_of_feedback + '\n')
        except:
            pass
    try:
        print(line_of_feedback)
    except:
        pass
