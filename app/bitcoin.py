##  generate bitcoin address  ##
## bitcoin address type explained : https://unchained.com/blog/bitcoin-address-types-compared/
## plan to implement P2PKH, P2WPKH, P2SH, P2WSH


DISCLAIM = 'This is purely for personal fun; never use it for generating any address for your money transferring.'

import sys, os
from typing import Any
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
    def __init__(self, addr_ver = 'P2PKH'):
        self.sk1 = E.ECC_Curve(E.SECP256K1)
        assert addr_ver in support_ver, f"unsupport address version {addr_ver}"
        self.addr_ver = addr_ver

    def GenKeyPair(self, priv_key = None, compressed:bool = True):
        priv = priv_key if priv_key != None else rand.randint( 1, self.sk1.n-1 ) 

        Pb   = self.sk1.PubKey_Gen(priv, False)
        # if priv_key == None :
        #     print("A random private key is generated as you do not provide a private key!")
        # else:
        #     print("A private key is provided.")

        # print('ECDSA Private Key:', "0x{:064x}".format(priv))
        # print('ECDSA Public  Key:')
        Pb.print_point('hex')

        return Pb.hex_str(format='x', compress=True) if compressed else Pb.hex_str(format='xy', compress=False) 
    
    
    def Hash160(self, input_:str):
        """do ripemd160(sha256(input_)) """
        # pdb.set_trace()
        if self.addr_ver == 'P2PKH':
            dig_sha256 = hash_256(hexstr2byte(input_), 'bytes', 'hex', 'sha256')
        elif self.addr_ver == 'P2SH':
            dig_sha256 = hash_256(input_, 'str', 'hex', 'sha256')

        dig_rip160 = hash_256(hexstr2byte(hex(dig_sha256)), 'bytes', 'hex', 'ripemd160')

        return dig_rip160

    def Base58encode_check(self, input_str:str):
        base58_code = base58.b58encode_check(hexstr2byte(input_str))
        BTC_ADDR_STR = base58_code.decode()
        return BTC_ADDR_STR
    
    def DoubleSha256(self, input_:str):
        """do Sha256(sha256(input_)) """
        #pdb.set_trace()
        #print(f"DoubleSha256: input = {input_}")
        dig_sha2561 = hash_256(hexstr2byte(input_), 'bytes', 'hex', 'sha256')
        #print(f"dig_sha1st: {hex(dig_sha2561)}")
        dig_sha2562 = hash_256(hexstr2byte(hex(dig_sha2561)), 'bytes', 'hex', 'sha256')
        #print(f"dig_sha1st: {hex(dig_sha2562)}")
        return dig_sha2562
    
    def Base58encode(self, input_str:str):
        base58_code = base58.b58encode(hexstr2byte(input_str))
        BTC_ADDR_STR = base58_code.decode()
        return BTC_ADDR_STR

    def base58codeccheck(self, input_ = None):
        print(f"construct address by using base58encode_check directly")
        BTC_ADDR_STR = None

        if self.addr_ver == 'P2PKH':
            compressed_pub_str = self.GenKeyPair(input_)
            pkh_byte = self.Hash160(compressed_pub_str)
            BTC_ADDR_STR = self.Base58encode_check('00'+ hex(pkh_byte)[2:])
        
        elif self.addr_ver == 'P2SH':
            assert input_ != None, f"you need input your reedeem_script for [{self.addr_ver}]"
            pksh_hash_byte = self.Hash160(input_)
            BTC_ADDR_STR = self.Base58encode_check('05'+ hex(pksh_hash_byte)[2:])

        elif self.addr_ver == 'P2WPKH':
            print(f"Not implemented yet for [{self.addr_ver}]")
            # sha_2nd_str = '0014'+ hex(pkh_byte)[2:]
            # print(f"sha_2nd_str = {sha_2nd_str}")

            # sha_byte = self.DoubleHash(sha_2nd_str)

            # BTC_ADDR_STR = self.Base58Codec('05'+ hex(sha_byte)[2:])
        elif self.addr_ver == 'P2WSH':
            print(f"Not implemented yet for [{self.addr_ver}]")
        
        print(f'final address [{self.addr_ver }]: {BTC_ADDR_STR}')

        return BTC_ADDR_STR
    
    def base58codec(self, input_ = None):
        """construct by using checksum"""
        print(f"construct address by using checksum")
        BTC_ADDR_STR = None

        if self.addr_ver == 'P2PKH':
            compressed_pub_str = self.GenKeyPair(input_)
            first_part = self.Hash160(compressed_pub_str)
            first_byte = hexstr2byte('00'+ hex(first_part)[2:])
            second_part = self.DoubleSha256(first_byte.hex())
            checksum_byte = hexstr2byte(hex(second_part)[2:10])
            BTC_ADDR_STR = self.Base58encode((first_byte+checksum_byte).hex())
        
        elif self.addr_ver == 'P2SH':
            assert input_ != None, f"for [{self.addr_ver}], need input your reedeem_script, can not be None"
            first_part = self.Hash160(input_)
            first_byte = hexstr2byte('05'+ hex(first_part)[2:])
            # print(f"first_byte = {first_byte.hex()}")
            second_part = self.DoubleSha256(first_byte.hex())
            checksum_byte = hexstr2byte(hex(second_part)[2:10])
            # print(f"checksum_byte: {checksum_byte.hex()}")
            BTC_ADDR_STR = self.Base58encode((first_byte+checksum_byte).hex())
            # BTC_ADDR_STR = self.Base58encode('05'+ hex(first_part)[2:])

        elif self.addr_ver == 'P2WPKH':
            print(f"Not implemented yet for [{self.addr_ver}]")
            # sha_2nd_str = '0014'+ hex(pkh_byte)[2:]
            # print(f"sha_2nd_str = {sha_2nd_str}")

            # sha_byte = self.DoubleHash(sha_2nd_str)

            # BTC_ADDR_STR = self.Base58Codec('05'+ hex(sha_byte)[2:])
        elif self.addr_ver == 'P2WSH':
            print(f"Not implemented yet for [{self.addr_ver}]")
        
        print(f'final address [{self.addr_ver }]: {BTC_ADDR_STR}')

        return BTC_ADDR_STR
    
    def __call__(self, input_ = None):
        self.base58codeccheck(input_)
        self.base58codec(input_)


def base58testvector(input_str: str = None):
    hex_str = '003a38d44d6a0c8d0bb84e0232cc632b7e48c72e0e' if input_str == None else input_str

    byte_data = hexstr2byte(hex_str)
    encoded = base58.b58encode_check(byte_data)  # bitcoin base58 with checksum
    print(encoded.decode())

    ### native base58 with bitcoin doulbe sha256 attached as checksum implementation

    sha_1st = hash_256(hexstr2byte(hex_str), 'bytes', 'hex', 'sha256')
    print(f"dig_sha1st: {hex(sha_1st)}")
    sha_2nd = hash_256(hexstr2byte(hex(sha_1st)), 'bytes', 'hex', 'sha256')
    print(f"dig_sha2nd: {hex(sha_2nd)}")
    checksum = hexstr2byte(hex(sha_2nd)[2:10])
    print(f"checksum: {checksum.hex()}")
    final_byte = byte_data + checksum
    print(f"final_byte= {final_byte}, type {type(final_byte)}")
    encoded1 = base58.b58encode(final_byte)  # bitcoin base58 with checksum
    print(encoded1.decode())

if __name__ == '__main__':   
    print(DISCLAIM)
    # input_hex_str= '003a38d44d6a0c8d0bb84e0232cc632b7e48c72e0e' #P2PKH TV
    # input_hex_str= '0582c11b43b312851b9813908ca3bda358794275f4' #P2SH TV
    # base58testvector(input_hex_str)
    # ref https://medium.com/coinmonks/how-to-generate-a-bitcoin-address-step-by-step-9d7fcbf1ad0b # not a fully correct blog, just take the test vector
    '''Note this is not good example as it implicitly add \n after for all the string before doing hash!!'''
    test_seed = "this is a group of words that should not be considered random anymore so never use this to generate a private key\n"

    # print(f"for P2PKH we use this seed to create a ECC private key: {test_seed}")
    sha256_p2pkh = hash_256(test_seed, 'str', 'hex', 'sha256')

    p2pkh = BitCoinAddr(addr_ver = 'P2PKH')
    p2pkh(sha256_p2pkh)
    print('**'*20)

    # #################################################

    reedeem_script = "this is a mock up transaction script, on priciple this would be something like '2 PubKey1 PubKey2 PubKey3 PubKey4 PubKey5 5 OP_CHECKMULTISIG', detail see https://www.oreilly.com/library/view/mastering-bitcoin/9781491902639/ch05.html#p2sh" 
    print(f"P2SH reedeem_script: {reedeem_script}")

    p2sh = BitCoinAddr(addr_ver = 'P2SH')
    p2sh(reedeem_script)

    # p2wpkh  = BitCoinAddr(addr_ver = 'P2WPKH')
    # p2wpkh(None)









    
