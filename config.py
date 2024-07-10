
### Global Config
import sys

LOG_SHOW_CFG = {
'LOG_I' : False,     #INFO
'LOG_M' : False,     #MESSAGE,
'LOG_D' : True,     #DEBUG
'LOG_W' : True,     #WARNING
'LOG_E' : True,     #ERROR
}

def py_version_good():
    ver = sys.version_info
    return (ver[0] == 3 and ver[1] > 7)


def setup(jcb_or_affine: str = 'affine', timing_measure: bool = True, verbose: bool = False, msg: str = 'system'):
    global USE_JCB # gobal config for jacobian (True) or affine (False) 

    global TIMING_MEASURE # config for Timing test (True) or Not (False) in support.py

    global DEBUG # config for debug decorator in support.py

    USE_JCB = True if jcb_or_affine == 'jacobian' else False

    TIMING_MEASURE = timing_measure

    DEBUG = verbose

    print(f"{msg} config: USE_JCB[{USE_JCB}], TIMING_MEASURE[{TIMING_MEASURE}], DEBUG[{DEBUG}]")


setup('affine', True, False)

