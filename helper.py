
## helper func -- format print
class txtcol:
    BLU = '\033[94m'
    YEL = '\033[93m'
    CYA = '\033[96m'
    GRE = '\033[92m'
    RED = '\033[91m'
    RST = '\033[0m'

def print_devider (method: str, n):
    i = 0
    while i<n :
        if method == 'line':
            print (txtcol.BLU + "-----------------------------------------" + txtcol.RST)
            # print (txtcol.disable(), end ='')
        elif method == 'double':
            print (txtcol.BLU + "=========================================" + txtcol.RST)
        i+=1
    pass

def log (level: str, msg: str ):
    if   level == 'i':
        print(txtcol.GRE + msg + txtcol.RST)
    elif level == 'd':
        print(txtcol.CYA + msg + txtcol.RST)      
    elif level == 'w':
        print(txtcol.YEL + msg + txtcol.RST)
    elif level == 'f':
        print(txtcol.RED + msg + txtcol.RST)
    
    pass


import hashlib          # hash function
# hash function
def hash_256(message: str):
    """Returns the SHA256 hash of the provided message string."""
    dig = hashlib.sha256()
    dig.update( message.encode() ) # convert str to bytes
    z = int(dig.hexdigest(),16)
    return z

def hash_test(msg):
    '''sha256 can be checked directly by linux command line '''
    '''for exp echo -n msg | sha256sum '''
    dig = hash_256(msg)
    print ("msg = ", msg  )
    print ("dig = 0x%064x" %(dig) )

def hash_test():
    msg1 = "I love you"
    msg2 = "blablabla..."
    # msg3 = int( rand.randint(1, 1<<255 ), 16)
    hash_test(msg1)
    hash_test(msg2)
    # hash_test(msg3)