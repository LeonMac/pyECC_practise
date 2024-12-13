import hashlib
from pysmx.SM3 import SM3   # https://gitee.com/snowlandltd/snowland-smx-python

###########################################################

def hash_256(message , msg_fmt = 'str', return_fmt = 'hex', sha_type = 'sha256'):

    """Returns the SHA256 hash of the provided message (str or byte str)"""
    assert msg_fmt == 'str' or msg_fmt == 'bytes', f"not supported msg format = {msg_fmt}"
    assert return_fmt == 'hex' or return_fmt == 'bytes', f"not supported return format = {return_fmt}"
    assert sha_type == 'sha256' or sha_type == 'sm3', f"not supported sha type = {sha_type}"

    if sha_type == 'sha256':
        
        dig = hashlib.sha256()
    else:
        
        dig = SM3()
    
    if msg_fmt == 'str':
        msg = message.encode("utf-8")   # convert str to bytes
    else:
        msg = message    # if it is already bytes string           

    # log('i', f"msg = {msg}, type {type(msg)}")
    dig.update( msg )   # hash digest

    if return_fmt == 'hex':
        return int(dig.hexdigest(), 16)
    else :
        return dig.digest()


def hash_512(message: str):

    """Returns the SHA256 hash of the provided message string."""
    dig = hashlib.sha512()
    dig.update( message.encode() ) # convert str to bytes
    z = int(dig.hexdigest(), 16)
    return z

def hash_test(msg):
    '''sha256 can be checked directly by linux command line '''
    '''for exp echo -n msg | sha256sum '''
    dig = hash_256(msg)
    print ("msg = ", msg  )
    print ("dig = 0x%064x" %(dig) )

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
    msg = bytes.fromhex(hex(hex_)[2:])
    dig_test  = hex(hash_256 (msg, 'bytes', 'hex', 'sm3'))
    dig_test_actual = dig_test[2:]
    log('i', f"msg = {msg}, type {type(msg)}")
    log('i', f"dig_test_actual = {dig_test_actual}")