
### Global Config
import sys


USE_JCB = True  # gobal config for jacobian (True) or affine (False)

TIMING_MEASURE = True # config for Timing test (True) or Not (False) in support.py

DEBUG = False # config for debug decorator in support.py

LOG_SHOW_CFG = {
'LOG_I' : False,     #INFO
'LOG_M' : False,     #MESSAGE,
'LOG_D' : False,     #DEBUG
'LOG_W' : True,     #WARNING
'LOG_E' : True,     #ERROR
}

def py_version_good():
    ver = sys.version_info
    return (ver[0] == 3 and ver[1] > 6)

