from cx_Freeze import setup, Executable
import os.path

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

options = {
    'build_exe': {
        'include_files':[
            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),
         ],
    },
}

setup(
    options=options,
    name="Daily Log Generator",
    version="1.0",
    description="MyEXE",
    executables=[Executable("AG/Daily_Log_Generator/Generator.py", base="Win32GUI")],
    )
# https://stackoverflow.com/questions/10592913/how-do-i-convert-a-python-program-to-a-runnable-exe-windows-program/34242025#34242025?newreg=35eb818df64b45b381ddf1cc69e5a753
# https://stackoverflow.com/questions/35533803/keyerror-tcl-library-when-i-use-cx-freeze
