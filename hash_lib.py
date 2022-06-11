###########################################################

def hash_256(message: str):
    import hashlib
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

if __name__ == '__main__':
    #https://docs.python.org/3/library/subprocess.html#subprocess.run
    import random
    import subprocess
    from log import log
    msg_dict = ['I love you', 'blablabla', str(random.randint(1, 1<<256 -1))]
    test_cnt = len(msg_dict)
    pass_cnt = 0

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

    log('d', f"total hash256 test case = {test_cnt}, pass_cnt = {pass_cnt}, test passed: {test_cnt == pass_cnt}")
