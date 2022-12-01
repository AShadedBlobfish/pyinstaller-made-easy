def show_exception_and_exit(exc_type, exc_value, tb):
    import traceback
    traceback.print_exception(exc_type, exc_value, tb)
    input("Press ENTER to exit...")
    sys.exit(-1)

def catch():
    input("Press ENTER to exit...")
    sys.exit(-1)

def build(file):
    if sys.platform == 'win32' or sys.platform == 'darwin':
        job = subprocess.run(str('pyinstaller -F -i "NONE" '+file))
    else:
        job = subprocess.run(str("pyinstaller -F "+file))
    return job.returncode

import shutil
import subprocess
from subprocess import DEVNULL
from subprocess import STDOUT
import sys
import os
# Prevents the program from exiting when an exception occurs
sys.excepthook = show_exception_and_exit

# Checks if pyinstaller is installed correctly
try:
    subprocess.run(["pyinstaller", "--version"], stdout=DEVNULL, stderr=STDOUT)
except:
    print("\npyinstaller is not installed or is installed incorrectly.\nInstall it using 'pip install pyinstaller' in command prompt as administrator")
    catch()

# Checks if working directory is suitable for building
if os.path.exists("build") or os.path.exists("dist"):
    print("Current working directory contains files from a previous build job, please remove them and try again")
    catch()

# Input validation
loop = True
while loop == True:
    in1 = input("Enter file name: ")
    filename = os.path.splitext(in1)[0]
    extension = os.path.splitext(in1)[1]
    try:
        if not os.path.exists(in1):
            print("Input file does not exist")
        elif not extension == '.py' and not extension == '.pyw':
            print(f"'{in1}' is not a valid python script")
        else:
            loop = False
    except:
        print(f"'{in1}' is not a valid python script")
        


# Compiles the file and catches any exceptions during build
if build(in1) != 0:
    catch()


# Deletes all spec files in the working directory then recompiles the file. This is the easiest way to fix a weird error which causes windows to purge the compiled file because it thinks it's a virus
print("Verifying exe integrity...")
files = os.listdir()
for i in files:
    if os.path.splitext(i)[1] == ".spec":
        os.remove(i)
if build(in1) != 0:
    catch()

# Asks the user if they want to clean up the files i.e Purge the 'build' dir and spec file
clean = input("Remove clutter? (This will not affect the function of your exe, but you will not be able to view the build logs)\n(Y/n) ")

# Cleans up the files
if clean == 'Y':
    shutil.rmtree("build")
    os.remove(filename+".spec")
    print("Log files and clutter purged. The compilied file can be found in the 'dist' directory")
else:
    print("The compilied file can be found in the 'dist' directory")



input("\nPress ENTER to exit...")
