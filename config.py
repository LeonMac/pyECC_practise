
### Config for log show, control log.log
import sys

LOG_SHOW_CFG = {
'LOG_I' : True,    #INFO
'LOG_D' : True,    #DEBUG
'LOG_W' : True,     #WARNING
'LOG_E' : True,     #ERROR
'LOG_M' : True,     #MESSAGE, 
}

def py_version_good():
    ver = sys.version_info
    return (ver[0] == 3 and ver[1] > 6)

