from log import log

#https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-56Cr2.pdf
# pip install bitstring if not 
# https://bitstring.readthedocs.io/en/latest/walkthrough.html

# def show_detail(m:str):
#     print(f"str = {m}, type(str) = {type(m)}, bytelen(str) = {len(m)}")

# from bitstring import BitArray, BitStream
# def KDM(Z:bytes, L: int, FixedInfo:BitArray):
#     """Key Derivate Method NIST.SP.800-56Cr2
#         Using option1 (no salt), 
#         Using hash256
#     """
#     assert L>0, f"Privided L value {L} is invalid, must be >0"

#     H_outputBits    = 256       # given we use hash256
#     max_H_inputBits = 512-56       # restric input length to one hash

#     reps = L / H_outputBits
#     # L shall not exceed H_outputBits × (2^32 –1).
#     if reps > ( 1<<32 -1 ):
#         log('e', "given L value is too big that up(L/256): {reps} > (2^32-1)")
#         return None
    
#     counter = 0x0
#     len_counter_max = 
#     m_enc = bytes(Z, encoding="utf-8")
#     m_bit_len = len(m_enc)*8
#     fixinfo_bit_len = len(FixedInfo)