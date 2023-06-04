import sys, os
root_path = os.path.dirname(os.getcwd ())
sys.path.append(root_path)

from random import SystemRandom
rand = SystemRandom()
from ecc import ECP
import pyECC as E

class BitCoin():
    '''Bitcoin Address Generator
       This is only for study but NOT for production
    '''
    def __init__(self):
        self.sk1 = E.ECC_Curve(E.SECP256K1)

    def KeyPair_Gen(self, priv_key = None ):
        priv = priv_key if priv_key != None else rand.randint( 1, self.sk1.n-1 ) 

        Pb   = self.sk1.PubKey_Gen(priv, False)

        print('ECDSA Private Key:', "0x{:064x}".format(priv))
        print('ECDSA Public  Key:')
        Pb.print_point('hex')


    def __call__(self):
        self.KeyPair_Gen()
        

if __name__ == '__main__':

    btc_key = BitCoin()
    btc_key()