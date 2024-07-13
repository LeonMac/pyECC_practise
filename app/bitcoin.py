##  generate bitcoin address  ##
## bitcoin address type explained : https://unchained.com/blog/bitcoin-address-types-compared/
## plan to implement P2PKH, P2WPKH, P2SH

# ref https://medium.com/coinmonks/how-to-generate-a-bitcoin-address-step-by-step-9d7fcbf1ad0b
DISCLAIM = 'This is purely personal fun, NEVER use it for generating a address for your money transfering'

'''Note this is not good example as it implicitly add \n after for all the string before doing hash!!'''
test_seed = "this is a group of words that should not be considered random anymore so never use this to generate a private key\n"

import sys, os
import base58
root_path = os.path.dirname(os.getcwd ())
sys.path.append(root_path)

from random import SystemRandom
rand = SystemRandom()

from hash_lib import hash_256
from support import hexstr2byte
import pyECC as E

import pdb

support_ver = ['P2PKH', 'P2WPKH', 'P2SH']

class BitCoinAddr():
    '''Bitcoin Address Generator
       This is only for study but NOT for production, use it carefully
    '''
    def __init__(self):
        self.sk1 = E.ECC_Curve(E.SECP256K1)

    def GenKeyPair(self, priv_key = None, compressed:bool = True):
        priv = priv_key if priv_key != None else rand.randint( 1, self.sk1.n-1 ) 

        Pb   = self.sk1.PubKey_Gen(priv, False)
        if priv_key == None :
            print("A random private key is generated as you do not provide a private key!")
        else:
            print("A private key is provided.")

        print('ECDSA Private Key:', "0x{:064x}".format(priv))
        print('ECDSA Public  Key:')
        Pb.print_point('hex')

        return Pb.hex_str(format='x', compress=True) if compressed else Pb.hex_str(format='xy', compress=False) 
    
    def Hashes(self, compressed_pub_key_str:str, address_ver:str='P2PKH'):
        # pdb.set_trace()

        dig_sha256 = hash_256(hexstr2byte(compressed_pub_key_str), 'bytes', 'hex', 'sha256')
        dig_rip160 = hash_256(hexstr2byte(hex(dig_sha256)), 'bytes', 'hex', 'ripemd160')

        if address_ver == 'P2PKH':
            return f"00{hex(dig_rip160)[2:]}" 
        elif address_ver == 'P2WPKH':
            return f"0014{hex(dig_rip160)[2:]}" 

    def Base58Codec(self, sha_str:str):
        pk2pkh_b58 = base58.b58encode_check(hexstr2byte(sha_str))
        BTC_ADDR_STR = pk2pkh_b58.decode()
        return BTC_ADDR_STR


    def __call__(self, priv_key = None, address_ver:str='P2PKH'):
        assert address_ver in address_ver, f"unsupport address version {address_ver}"

        compressed_pub_str = self.GenKeyPair(priv_key)

        sha_str = self.Hashes(compressed_pub_str, address_ver)

        BTC_ADDR_STR = self.Base58Codec(sha_str)
        print(f'final address [{address_ver}]: {BTC_ADDR_STR}')

        return BTC_ADDR_STR



def base58test(input_str: str = None):
    hex_str = '003a38d44d6a0c8d0bb84e0232cc632b7e48c72e0e' if input_str == None else input_str

    byte_data = hexstr2byte(hex_str)
    encoded = base58.b58encode_check(byte_data)  # bitcoin base58 with checksum
    print(encoded.decode())

    ### native base58 with bitcoin doulbe sha256 attached as checksum implementation

    sha_1st = hash_256(hexstr2byte(hex_str), 'bytes', 'hex', 'sha256')
    print(f"dig_sha1st: {hex(sha_1st)}")
    sha_2nd = hash_256(hexstr2byte(hex(sha_1st)[2:]), 'bytes', 'hex', 'sha256')
    print(f"dig_sha2nd: {hex(sha_2nd)}")
    checksum = hexstr2byte(hex(sha_2nd)[2:10])
    print(f"checksum: {checksum.hex()}")
    final_byte = byte_data + checksum
    encoded1 = base58.b58encode(final_byte)  # bitcoin base58 with checksum
    print(encoded1.decode())

if __name__ == '__main__':   
    print(DISCLAIM)

    # base58test()

    print(f"address seed: {test_seed}")
    sha256 = hash_256(test_seed, 'str', 'hex', 'sha256')
    # print(f"private key type : {type(sha256)}")

    # btc_key = BitCoinAddr()
    # btc_key(sha256)

    #######################
    # priv_add_str = '60cf347dbc59d31c1358c8e5cf5e45b822ab85b79cb32a9f3d98184779a9efc2'
    # priv_int = int(priv_add_str, 16)
    # print
    # btc_key(priv_int)
   
    # compressed_pub_str = btc_add.GenKeyPair(sha256)
    # print(f"compressed pubkey: {compressed_pub_str}")
    # hash_str = btc_add.Hashes(compressed_pub_str, 'P2PKH')
    # print(f"P2PKH string: {hash_str}")
    # print('-'*20)

    btc_add = BitCoinAddr()
    btc_add(sha256, address_ver='P2PKH')









    
