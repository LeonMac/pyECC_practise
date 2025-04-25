import timeit
import functools

from tools.log import log

from decimal import Decimal
from config import TIMING_MEASURE, DEBUG


## timing decorator
def timing_log(func):
    """Decorator to measure and log function execution time."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not TIMING_MEASURE:
            return func(*args, **kwargs)

        start = timeit.default_timer()
        result = func(*args, **kwargs)
        duration = timeit.default_timer() - start
        d = Decimal(str(duration)).quantize(Decimal("0.001"), rounding="ROUND_HALF_UP")
        print(f"{func.__name__} took {d} seconds")
        return result

    return wrapper

## debug_decorator
def debug_control(func):
    """decoration for debug stuff"""

    if DEBUG:

        def do_debug_stuff(self, *args, **kwargs):
            func(self, *args, **kwargs)
            pass

        return do_debug_stuff
    
    else:
        pass

# https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-56Cr2.pdf
# pip install bitstring if not 
# https://bitstring.readthedocs.io/en/latest/walkthrough.html

def show_detail(m:str):
    print(f"str = {m}, type(str) = {type(m)}, bytelen(str) = {len(m)}")

def NIST_KDM(Z:bytes, L: int, FixedInfo:bytes) -> int:
    """Key Derivate Method NIST.SP.800-56Cr2
        Using option1 (no salt), Using hash256
        return big uint
    """
    assert L>0, f"Privided L value {L} is invalid, must be >0"
    log('w', f"This function is not yet been tested!!!")

    from bitstring import Bits
    from core.hash_lib import hash_256
    H_outputBits    = 256       # given we use hash256
    max_H_inputBits = 512-56       # restric input length to one hash

    reps = int(L / H_outputBits)   # L shall not exceed H_outputBits × (2^32 –1).
    if reps > ( 1<<32 -1 ):
        print( f"given L value is too big that up(L/256): {reps} > (2^32-1)")
        return 0

    c = Bits('uint:32=0')

    z_enc = bytes(Z, encoding="utf-8")
    z = Bits(bytes=z_enc)

    f_enc = bytes(FixedInfo, encoding="utf-8")
    f = Bits(bytes=f_enc)

    concat= c + z + f
    #.append(counter).append(z).append(f)

    if len(concat) > max_H_inputBits:
        print("error, concat string byte len ={len} > max_H_inputBits {max_H_inputBits}")
        return 0

    R = Bits(0)
    i = 1
    while i <= reps:
        c_int = c.uint + 1
        concat = Bits(uint=c_int, length=32) + z + f
        concat_bytes = concat.bytes
        K = hash_256(concat_bytes, msg_fmt = 'bytes')
        R = R + Bits(uint=K, length=K.bit_length())
        
        i += 1

    msb = len(R) - 1
    lsb = len(R) - L
    result = R[lsb:msb].uint

    return result


def SM2_KDF(Z, klen: int, dgest_type = 'sha256', input_fmt = 'str', return_fmt = 'hex'):
    """key derivation function of SM2 spec. 5.4.3"""
    assert input_fmt  == 'str' or input_fmt == 'bytes',  f"not supported input format = {input_fmt}"
    # assert return_fmt == 'hex' or return_fmt == 'bytes' or return_fmt == 'bits', f"not supported return format = {return_fmt}"
    assert return_fmt == 'hex' or return_fmt == 'bits', f"not supported return format = {return_fmt}"
    
    v = 256  # digest bit length
    assert klen < (pow(2, 32) - 1 )*v
    last_nbit = klen % v
    if (klen % 8) != 0 and return_fmt == 'hex':
        assert False, f"given (klen % 8) = {(klen % 4)}, but requested return format = {return_fmt}"

    
    from bitstring import Bits
    from core import hash_lib as hash
    import struct

    if input_fmt == 'str':
        Z_byte = bytes(Z, encoding='UTF-8')  # convert Z string to byte
    else:
        Z_byte = bytes.fromhex(Z)

    n = klen // v

    if  last_nbit == 0:
        n_iter = n
    else:
        n_iter = n + 1
   
    # print(f"n_iter= {n_iter}, last_nbit = {last_nbit}")
    # print(f"Z_byte= {Z_byte}")
    ct=int(0x1)  # init count (int32)
    dgst = []
    for i in range(n_iter):
        ct_byte = struct.pack('>L', ct) # pack ct to byte (>: big Endian, L: unsigned long)
        msg_byte = Z_byte + ct_byte     # concatenate Z_byte and ct_byte

        dgst_i = hash.hash_256(msg_byte, 'bytes', 'bytes', dgest_type)
        # print(f"msg_byte= {msg_byte}")
        # print(f"dgst[{i}] in hex = {dgst_i.hex()}")

        if i == n_iter-1 and last_nbit: # the very last iteration
            if return_fmt == 'hex':
                last_nbyte = last_nbit // 8 
                dgst.append ( dgst_i[0:last_nbyte] )
            elif return_fmt == 'bits':
                temp_dgst = Bits( bytes = dgst_i)
                last_bits = temp_dgst[0:last_nbit]
                # dgst.append (last_dgst.bytes)

            # print(f"The last iter: #{i}, last_nbit = {last_nbit}")
        else:
            dgst.append ( dgst_i )
            last_bits = ''
        
        ct = ct+1

    len_ = len(dgst)
    K_bytes = b''
    for l in range (len_):
        K_bytes = K_bytes + dgst[l]
    
    # print(f"K_bytes = {K_bytes}")

    if return_fmt == 'hex':
        #K_bits = Bits( bytes= K_bytes )
        return K_bytes.hex()
    
    else: 
        K_bits = Bits( bytes= K_bytes ) + last_bits
        return K_bits

if __name__ == '__main__':
    log('i', "KDF function test:")
    # test vector from sm3 spec. Part4, P8
    # 坐标x 2 ：
    # 64D20D27 D0632957 F8028C1E 024F6B02 EDF23102 A566C932 AE8BD613 A8E865FE
    # 坐标y 2 ：
    # 58D225EC A784AE30 0A81A2D4 8281A828 E1CEDF11 C4219099 84026537 5077BF78
    # 消息M 的比特长度klen=152
    # 计算t=KDF (x 2 ∥y 2 , klen)：
    # 006E30 DAE231B0 71DFAD8A A379E902 64491603

    x2 = '64D20D27D0632957F8028C1E024F6B02EDF23102A566C932AE8BD613A8E865FE'
    y2 = '58D225ECA784AE300A81A2D48281A828E1CEDF11C4219099840265375077BF78'
    
    #Z  = bytes.fromhex (x2) + bytes.fromhex (y2)
    #Z  = bytes.fromhex (x2)[::-1] + bytes.fromhex (y2)[::-1]    # Endian convert
    klen = 152
    Z   = x2 + y2

    t = SM2_KDF(Z, klen, 'sm3', 'bytes', 'hex')

    log('i', f"klen = {klen}")
    log('i', f"K = {t}")

    klen = 150

    t = SM2_KDF(Z, klen, 'sm3', 'bytes', 'bits')

    log('i', f"klen = {klen}")
    log('i', f"K = {t}")


