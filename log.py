
class txtcol:
    '''output format: color setup'''
    BLU = '\033[94m'
    YEL = '\033[93m'
    CYA = '\033[96m'
    GRE = '\033[92m'
    RED = '\033[91m'
    RST = '\033[0m'

def print_devider (method: str, n):
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

def log (level: str, msg: str ):
    '''simple log output w/ different color'''
    if   level == 'i':
        print(txtcol.GRE + '[INFO]: ' + msg + txtcol.RST)
    elif level == 'd':
        print(txtcol.CYA + '[DEBG]: ' + msg + txtcol.RST)      
    elif level == 'w':
        print(txtcol.YEL + '[WARN]: ' + msg + txtcol.RST)
    elif level == 'e':
        print(txtcol.RED + '[ERRO]: ' + msg + txtcol.RST)
    pass

