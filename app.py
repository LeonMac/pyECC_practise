# this is a playgound for using the ecc library
# 
from random import SystemRandom
rand = SystemRandom()
from ecc import ECP
import pyECC as E
from log import log, hex_show

cuv = E.ECC_Curve(E.SM2_CV_ID)

def KeyPair_Gen():

    priv = rand.randint( 1, cuv.n-1 )
    Pb   = cuv.PubKey_Gen(priv, False)

    print('Your priv key (never disclose it to anybody):', "0x{:064x}".format(priv))
    print('Your pub key:')
    Pb.print_point()


def Encryption(fmt:str ='c1c3c2'):
    assert fmt in ('c1c2c3', 'c1c3c2'), f"incorrect output format :{fmt}"
    x_hexstr = input("please input the receiver's public key x (hex with '0x' prefix):")
    y_hexstr = input("please input the receiver's public key y (hex with '0x' prefix):")
    Pb = ECP((int(x_hexstr, 16), int(y_hexstr, 16)))
    #Pb.print_point()

    M = input("please input the message you want to encrypted by using sm2:")

    C  = cuv.SM2_Encryption(M, Pb, None, fmt, False)

    print('Your encrypted message (hex):', C)

    return C

def Decryption(fmt:str ='c1c3c2'):
    assert fmt in ('c1c2c3', 'c1c3c2'), f"incorrect output format :{fmt}"

    C = input("please paste the encrypted message you want to do decryption here (hex):")
    priv_hexstr = input("please input the your priv key (hex with '0x' prefix):")
    priv = int(priv_hexstr, 16)
    #print('Your priv key (never disclose it to anybody):', "{:064x}".format(priv))
    M_ = cuv.SM2_Decryption(C, priv, fmt, False)
    print('Your decrypted message:', M_)


################################################
if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print(f"usage: python {sys.argv} operation ( kg | en | de | full ), format( c1c2c3 | c1c3c2 )")
        print(f"kg = keygen, en = encryption, de = decryption, full = run all")
        assert False, f'only accept one arguments. you input {len(sys.argv)} args!'
    
    opt = sys.argv[1] 
    assert opt in ('kg','en','de','full'), f"incorrect operation args input {opt}" 
    
    fmt = sys.argv[2]
    assert fmt in ('c1c2c3','c1c3c2'), f"incorrect format args input {fmt}" 

    if opt == 'kg': 
        KeyPair_Gen()
    elif opt == 'en':
        Encryption(fmt)
    elif opt == 'de':
        Decryption(fmt)
    else:
        KeyPair_Gen()
        Encryption(fmt)
        Decryption(fmt)

