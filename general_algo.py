from log import log

#https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-56Cr2.pdf
# pip install bitstring if not 
# https://bitstring.readthedocs.io/en/latest/walkthrough.html

def show_detail(m:str):
    print(f"str = {m}, type(str) = {type(m)}, bytelen(str) = {len(m)}")

def KDM(Z:bytes, L: int, FixedInfo:bytes) -> int:
    """Key Derivate Method NIST.SP.800-56Cr2
        Using option1 (no salt), Using hash256
        return big uint
    """
    assert L>0, f"Privided L value {L} is invalid, must be >0"

    from bitstring import Bits
    from hash_lib import hash_256
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

