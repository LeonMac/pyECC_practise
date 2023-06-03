
### Global Config
import sys


USE_JCB = True  # gobal config for jacobian (True) or affine (False)

TIMING_MEASURE = True # gobal config for Timing test (True) or Not (False)

# DEBUG = False

LOG_SHOW_CFG = {
'LOG_I' : True,     #INFO
'LOG_D' : True,     #DEBUG
'LOG_W' : True,     #WARNING
'LOG_E' : True,     #ERROR
'LOG_M' : True,     #MESSAGE, 
}

def py_version_good():
    ver = sys.version_info
    return (ver[0] == 3 and ver[1] > 6)

