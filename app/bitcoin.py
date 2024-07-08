##  generate a bitcoin address  ##
# ref https://medium.com/coinmonks/how-to-generate-a-bitcoin-address-step-by-step-9d7fcbf1ad0b
'''Note this is not good example as it implicitly add \n after for all the string before doing hash!!'''
test_seed = "this is a group of words that should not be considered random anymore so never use this to generate a private key\n"
print(f"address seed: {test_seed}")

import sys, os
import base58
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
    
    # def Hash(compressed_pub_str:str):
    #     PubSha256 = hash_256(compressed_pub_str, 'str', 'hex', 'sha256')
    #     PubRipemd160 = hash_256(PubSha256, 'str', 'hex', 'sha256')
        


    def __call__(self, priv_key = None):
        compress_pun_key_str = self.GenKeyPair(priv_key)
        print(f"compressed pubkey: {compress_pun_key_str}")
        dig_sha256 = hash_256(bytes.fromhex(compress_pun_key_str), 'bytes', 'hex', 'sha256')
        print(f"dig_sha256: {hex(dig_sha256)}")
        dig_rip160 = hash_256(bytes.fromhex(hex(dig_sha256)[2:]), 'bytes', 'hex', 'ripemd160')
        print(f"dig_rip160: {hex(dig_rip160)}")
        pk2pkh_str = f"00{hex(dig_rip160)[2:]}" 
        print(f"P2PKH string: {pk2pkh_str}")
        pk2pkh_b58 = base58.b58encode_check(bytes.fromhex(pk2pkh_str))
        print(f'final address: {pk2pkh_b58.decode()}')

def base58test(input_str: str = None):
    hex_str = '003a38d44d6a0c8d0bb84e0232cc632b7e48c72e0e' if input_str == None else input_str

    byte_data = bytes.fromhex(hex_str)
    encoded = base58.b58encode_check(byte_data)  # bitcoin base58 with checksum
    print(encoded.decode())

    ### native base58 with bitcoin doulbe sha256 attached as checksum implementation

    sha_1st = hash_256(bytes.fromhex(hex_str), 'bytes', 'hex', 'sha256')
    print(f"dig_sha1st: {hex(sha_1st)}")
    sha_2nd = hash_256(bytes.fromhex(hex(sha_1st)[2:]), 'bytes', 'hex', 'sha256')
    print(f"dig_sha2nd: {hex(sha_2nd)}")
    checksum = bytes.fromhex(hex(sha_2nd)[2:10])
    print(f"checksum: {checksum.hex()}")
    final_byte = byte_data + checksum
    encoded1 = base58.b58encode(final_byte)  # bitcoin base58 with checksum
    print(encoded1.decode())

if __name__ == '__main__':   

    base58test()

    print(f"address seed: {test_seed}")
    sha256 = hash_256(test_seed, 'str', 'hex', 'sha256')
    # print(f"private key : {hex(sha256)}")

    btc_key = BitCoinAddr()
    btc_key(sha256)





    
