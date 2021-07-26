import os
import sys



is_windows = os.name == 'nt'
is_mac = sys.platform == 'darwin'
is_linux = sys.platform == 'linux'

def is_python_file(file):
    return file.endswith('.py')

def is_json_file(file):
    return file.endswith('.json')

