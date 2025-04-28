from random import SystemRandom
from core.prime import genPrime
from core.modulo import lcm, modular_inverse

from tools.support import timing_log

# https://en.wikipedia.org/wiki/RSA_cryptosystem


def _genPrimePair(bits_len:int, mr:int):
    assert bits_len >= 8 and mr >= 20

    p = genPrime(bit_len=bits_len, m=mr)
    q = genPrime(bit_len=bits_len, m=mr)

    while p == q:
        p = genPrime(bit_len=bits_len, m=mr)
    
    return p, q

def eulerCof(bits_len:int = 512, mr:int = 30):
    p, q  = _genPrimePair (bits_len, mr)

    return p*q, (p-1)*(q-1)  # N, phi(N)


def carmiCof(bits_len:int, mr:int):
    p, q  = _genPrimePair (bits_len, mr)

    carmi = lcm(p-1, q-1)   
    return p*q, carmi   # N, lmbda(N)


def genSecret(euler:bool=True):
    return eulerCof() if euler else carmiCof()

# N, phi = eulerCof()
# print(f"N={N}, phi={phi}")

# N, lbd = eulerCof()
# print(f"N={N}, lmbda={lbd}")


def genRSAKeyPair(rnd:bool = True, euler:bool = True):

    if rnd:
        pub = genPrime(bit_len=1024, m=40)
    else:
        pub = 65537
    
    N, mod = genSecret(euler)
    priv = modular_inverse(pub, mod)

    return N, pub, priv


def rsaDemo(M: str):
    print(f"Mesg: {M}")
    N, pub, priv = genRSAKeyPair()
    M_Byte = M.encode('utf-8')
    M_int = int.from_bytes(M_Byte, "big")
    m_len = len(M_Byte)
    C = pow(M_int, pub, N)
    print(f"ENC : {hex(C)}")
    e = pow(C, priv, N)
    recov_byte = e.to_bytes(m_len, 'big')
    M_recov = recov_byte.decode('utf-8')
    print(f"DEC : {M_recov}")


M = input("Input the message you want to encrypt by using RSA:")
recov = rsaDemo(M)
