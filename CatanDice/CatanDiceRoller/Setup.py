import cx_Freeze
import sys
import os

#python setup.py bdist_msi

os.environ['TCL_LIBRARY'] = r"C:\ProgramData\Anaconda3\tcl\tcl8.6"
os.environ['TK_LIBRARY'] = r"C:\ProgramData\Anaconda3\tcl\tk8.6"
include_files = [r"C:\ProgramData\Anaconda3\DLLs\tcl86t.dll",
                r"C:\ProgramData\Anaconda3\DLLs\tk86t.dll",
                "sounds\\"]

base = None
if sys.platform == 'win32':
    base = "Win32GUI"

executables = [cx_Freeze.Executable("CatanDiceRoller.py", base=base)]

cx_Freeze.setup(
    name = "Catan Dice Stat Tracker",
    options = {"build_exe": {"packages":["tkinter", "gtts", "playsound"], "include_files":include_files}},
    version = "0.4",
    description = "Tracks stats for Catan Dice",
    author = "Your friendly neighborhood hu.man",
    executables = executables
    )
