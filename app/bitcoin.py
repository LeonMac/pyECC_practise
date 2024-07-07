##  generate a bitcoin address  ##
# ref https://medium.com/coinmonks/how-to-generate-a-bitcoin-address-step-by-step-9d7fcbf1ad0b
'''Note this is not good example as it implicitly add \n after for all the string before doing hash!!'''
test_seed = "this is a group of words that should not be considered random anymore so never use this to generate a private key\n"
print(f"address seed: {test_seed}")

import sys, os
root_path = os.path.dirname(os.getcwd ())
sys.path.append(root_path)

from random import SystemRandom
rand = SystemRandom()
# from ecp import ECP_AFF as ECP
from hash_lib import hash_256
import pyECC as E

class BitCoinAddr():
    '''Bitcoin Address Generator
       This is only for study but NOT for production, use it carefully
    '''
    def __init__(self):
        self.sk1 = E.ECC_Curve(E.SECP256K1)

    def GenKeyPair(self, priv_key = None ):
        priv = priv_key if priv_key != None else rand.randint( 1, self.sk1.n-1 ) 

        Pb   = self.sk1.PubKey_Gen(priv, False)
        if priv_key == None :
            print("A random private key is generated as you do not provide a private key!")
        else:
            print("A private key is provided.")

        print('ECDSA Private Key:', "0x{:064x}".format(priv))
        print('ECDSA Public  Key:')
        Pb.print_point('hex')

        return Pb.hex_str(format='x', compress=True)
    
    def Hash(compressed_pub_str:str):
        PubSha256 = hash_256(compressed_pub_str, 'str', 'hex', 'sha256')
        PubRipemd160 = hash_256(PubSha256, 'str', 'hex', 'sha256')
        


    def __call__(self, priv_key = None):
        self.GenKeyPair(priv_key)



if __name__ == '__main__':   
    # btc_key = BitCoinAddr()
    # btc_key()
    # print("\n")

    print(f"address seed: {test_seed}")
    sha256 = hash_256(test_seed, 'str', 'hex', 'sha256')
    # print(f"private key : {hex(sha256)}")

    btc_key = BitCoinAddr()
    btc_key(sha256)



    
