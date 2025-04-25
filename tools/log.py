
class txtcol:
    '''output format: color setup'''
    BLU = '\033[94m'
    YEL = '\033[93m'
    CYA = '\033[96m'
    GRE = '\033[92m'
    RED = '\033[91m'
    RST = '\033[0m'

def print_divider (method: str, n:int):
    '''helper format, add seperator line '''
    i = 0
    while i<n :
        if method == 'line':
            print (txtcol.RST + "-----------------------------------------")
            # print (txtcol.disable(), end ='')
        elif method == 'double':
            print (txtcol.RST + "=========================================")
        i+=1
    pass

from config import LOG_SHOW_CFG as scfg
def log (level: str, msg: str ):
    '''simple log output w/ different color'''
    if   level == 'i':
        if scfg['LOG_I']:
            print(txtcol.RST + '[INFO]: ' + msg + txtcol.RST)
    elif level == 'd':
        if scfg['LOG_D']:
            print(txtcol.CYA + '[DEBG]: ' + msg + txtcol.RST)      
    elif level == 'w':
        if scfg['LOG_W']:
            print(txtcol.YEL + '[WARN]: ' + msg + txtcol.RST)
    elif level == 'e':
        if scfg['LOG_E']:
            print(txtcol.RED + '[ERRO]: ' + msg + txtcol.RST)
    elif level == 'm':
        if scfg['LOG_M']:
            print(txtcol.GRE + '[MESG]: ' + msg + txtcol.RST)
    else:
        assert False, f"incorrect log level {level}, please double check!"
    pass

def hex_show(msg: str, C: str, hex_N:int = 8):
    l = len(C)
    log('d', f"{msg}")
    print(txtcol.CYA + "\t", end = '')
    for i in range (l):
        print(C[i], end='')
        if (i+1) % hex_N == 0:
            print(' ', end ='')
            if (i+1) % (hex_N*8) == 0:
                print('\n\t', end ='')

    print(txtcol.RST + "\n")