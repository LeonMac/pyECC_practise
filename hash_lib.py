
# import pysmx
from pysmx.SM3 import SM3   # https://gitee.com/snowlandltd/snowland-smx-python
import hashlib
from  rmd160 import ripemd160
# print(hashlib.algorithms_available)
from support import hexstr2byte

def hash_256(message , msg_fmt = 'str', return_fmt = 'hex', sha_type = 'sha256'):
    """Not a good name--consider to change"""

    """Returns the SHA256 hash of the provided message (str or byte str)"""
    assert msg_fmt == 'str' or msg_fmt == 'bytes', f"not supported msg format = {msg_fmt}"
    assert return_fmt == 'hex' or return_fmt == 'bytes', f"not supported return format = {return_fmt}"
    assert sha_type in ['sha256', 'sm3', 'ripemd160'], f"not supported sha type = {sha_type}"

    if msg_fmt == 'str':
        msg = message.encode("utf-8")   # convert str to bytes
    else:
        msg = message    # if it is already bytes string    

    if sha_type in ['sha256', 'sm3']:
        if sha_type == 'sha256':
            dig = hashlib.sha256()
        # elif sha_type == 'ripemd160':
        #     # dig = hashlib.rmd160() # does not work on some openssl version, use bitcoin script.
        else:
            dig = SM3()
               
        # log('i', f"msg = {msg}, type {type(msg)}")
        dig.update( msg )   # hash digest
        if return_fmt == 'hex':
            return int(dig.hexdigest(), 16)
    
        else :
            return dig.digest()

    elif sha_type == 'ripemd160':
        dig = ripemd160(msg)
        if return_fmt == 'hex':
            return int(dig.hex(), 16)
        else :
            return dig


def hash_512(message: str):
    """Returns the SHA512 hash of the provided message string."""
    dig = hashlib.sha512()
    dig.update( message.encode() ) # convert str to bytes
    z = int(dig.hexdigest(), 16)
    return z


def hash_test(msg:str, msg_fmt = 'str', return_fmt = 'hex', sha_type:str='sha256'):
    '''sha256 can be checked directly by linux command line '''
    '''for exp echo -n msg | sha256sum '''
    dig = hash_256(msg, msg_fmt, return_fmt, sha_type )
    print ("msg str = ", msg  )
    if sha_type in['sha256', 'sm3']:
        sha_len = 256//4
    elif  sha_type == 'ripemd160':
        sha_len = 160//4
    elif sha_type == 'sha512':
        sha_len = 512//4
    else: pass

    print (f"dig[{sha_type}] = 0x%0{sha_len}x" %(dig) )

if __name__ == '__main__':
    # https://docs.python.org/3/library/subprocess.html#subprocess.run
    # https://the-x.cn/hash/ShangMi3Algorithm.aspx
    
    import random
    import subprocess
    from log import log
    msg_dict = ['I love you', 'blablabla', 'abc', str(random.randint(1, 1<<256 -1))]
    test_cnt = len(msg_dict)
    pass_cnt = 0

    log('i', f"sha256 test, compare with command line result-->")
    for msg in msg_dict:
        
        dig_test  = hex(hash_256 (msg))
        dig_test_actual = dig_test[2:]
        
        command   = "echo -n " + msg + "| sha256sum"
        dig_shell = (subprocess.check_output(command, shell=True)).decode()
        log('i', f"msg = {msg}")
        log('i', f"dig_test_actual = {dig_test_actual}")
        log('i', f"dig_shell       = {dig_shell}")
        if dig_test_actual in dig_shell:
            pass_cnt += 1

    log('i', f"total hash256 test case = {test_cnt}, pass_cnt = {pass_cnt}, test passed: {test_cnt == pass_cnt}")
    log('i', f"\nsm3 test-->")

    for msg in msg_dict:
        dig_test  = hex(hash_256 (msg, 'str', 'hex', 'sm3'))
        dig_test_actual = dig_test[2:]
        log('i', f"msg = {msg}")
        log('i', f"dig_test_actual = {dig_test_actual}")
    
    log('i', f"sm3 test vector from spec.-->")
    hex_ = 0x64d20d27d0632957f8028c1e024f6b02edf23102a566c932ae8bd613a8e865fe656e6372797074696f6e207374616e6461726458d225eca784ae300a81a2d48281a828e1cedf11c4219099840265375077bf78
    msg = hexstr2byte(hex(hex_)[2:])
    dig_test  = hex(hash_256 (msg, 'bytes', 'hex', 'sm3'))
    dig_test_actual = dig_test[2:]
    log('i', f"msg = {msg}, type {type(msg)}")
    log('i', f"dig_test_actual = {dig_test_actual}")

    # ref https://medium.com/coinmonks/how-to-generate-a-bitcoin-address-step-by-step-9d7fcbf1ad0b
    '''Note this is not good example as it implicitly add \n after for all the string before doing hash!!'''
    test_seed = "this is a group of words that should not be considered random anymore so never use this to generate a private key\n"

    hash_test(test_seed, 'str', 'hex', 'sha256')

    compress_pun_key_str = "023cba1f4d12d1ce0bced725373769b2262c6daa97be6a0588cfec8ce1a5f0bd09"

    hash_test(hexstr2byte(compress_pun_key_str), 'bytes', 'hex', 'sha256')

    hashed_compress_key_str = '8eb001a42122826648e66005a549fc4b4511a7ad3fc378221aa1c73c5efe77ef'

    hash_test(hexstr2byte(hashed_compress_key_str), 'bytes', 'hex', 'ripemd160')
