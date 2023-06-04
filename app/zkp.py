# https://arxiv.org/pdf/1107.1626.pdf
# a saimple zkp demo implementation based on ECC

import sys, os
root_path = os.path.dirname(os.getcwd ())
sys.path.append(root_path)

# 3.1 Zero Knowledge Proof of Discrete Logarithm with Coin Flip
import pyECC as ECC
from ecc import ECP
from random import SystemRandom
rand = SystemRandom()

import hash_lib as hash


class zkp_tool():
    def __init__(self, cid:int, interaction: int = 1):
        self.cuv = ECC.ECC_Curve(cid)
        self.rnd = interaction
        self.G   = self.cuv.G
        self.p   = self.cuv.p
        pass

    def gen_rand(self):
        return rand.randint( 1, self.cuv.n-1 )
    
    def Mul_Point (self, k=None, P=None): # x = None: simulate a dishonest Prover:
        
        if k == None: 
            k_ = self.gen_rand()
        else: k_ = k

        if P == None: 
            P_ = self.cuv.G
        else: P_ = P

        B = self.cuv.curve.Point_Mult(k_, P_)
        return k_ , B
    
    def Add_Point(self, P:ECP, Q:ECP) -> ECP:
        return self.cuv.curve.Point_Add_General(P, Q)

    def Gen_m (self, x, r):
        return (x + r) % self.cuv.n

    


def ZKP_DLwCF(cid:int, round:int, prover_honest:bool = True ):
    tool = zkp_tool(cid)
    x, B = tool.Mul_Point(None)  # B is known by both Prover and Verifier, x is secrete

    dishonest_count = 0

    for rnd in range (round):
        if prover_honest:            
            r,A = tool.Mul_Point(None)  # Prover generates random r point A = r.G , A is sent to Verifier
            #m   = tool.Gen_m(x,r)
        else:                           # if Prover is dis-honest, means he/she does not know x
            m   = tool.gen_rand()       # he prepares for TAILS 1). generate a random m, 2). compute A = m · G − B
            _, tempP  = tool.Mul_Point(m, tool.G) 
            # A   = tool.Add_Point(tempP, B.neg_point(tool.p))
            A   = tool.Add_Point(tempP, B.neg_point())
            r   = tool.gen_rand()       # but he does not able to easily get r from the A, so get a rand r

        flip_coin = rand.randint( 0, 1 )  # Verifier flip the coin

        if flip_coin:                # In case of HEADS Prover sends r to Verifier 
            _, A_ = tool.Mul_Point(r)
            if not A.is_equal(A_):       # Veififier checks that r · G = A
                dishonest_count += 1

        else:                       # In case of TAILS Prover sends m = x + r(mod n) to Verifier who checks that m · G = (x + r) · G = x · G + r · G = A + B
            if prover_honest:  
                m   = tool.Gen_m(x,r)


            _, mG  = tool.Mul_Point(m, tool.G) # Veififier checks that m · G = (x + r) · G = x · G + r · G = A + B
            ApB = tool.Add_Point(A, B)
            if not mG.is_equal(ApB):    
                dishonest_count += 1

    prob = 1 - pow(2, -1*dishonest_count) 

    print (f"total {round} rounds test, zkp dis-honest count = {dishonest_count}, Prover dishonest probability = {prob}")

    return dishonest_count


def ZKP_DLwCF_test(cid, round):
    print(f"Prover Honest test--> {round} rounds: ")
    ZKP_DLwCF(cid, round, True)
    print(f"Prover DisHonest test--> {round} rounds: ")
    ZKP_DLwCF(cid, round, False)

#####################################################################

def ZKP_Schnorr(cid:int, prover_honest:bool = True ):
    tool = zkp_tool(cid)
    G =   tool.G   
    x, B = tool.Mul_Point(None)  # B is known by both Prover and Verifier, x is secrete

    OK = False

    if prover_honest:
        r,A = tool.Mul_Point(None)  # Prover generates random r point A = r.G , A is sent to Verifier
        M_hex = G.hex_str('xy', None) + B.hex_str('xy', None) + A.hex_str('xy', None)
        c = hash.hash_256(M_hex, 'str', 'hex', 'sm3') #Verifier computes random c = HASH(G, B, A) and sends c to Prover 
        m = (r + c * x) % tool.cuv.n # Prover computes m = r + c · x(mod n) and sends m to Verifier 

    else:                           # if Prover is dis-honest, means he/she does not know x
        r,A = tool.Mul_Point(None)  # Prover generates random r point A = r.G , A is sent to Verifier
        M_hex = G.hex_str('xy', None) + B.hex_str('xy', None) + A.hex_str('xy', None)
        c = hash.hash_256(M_hex, 'str', 'hex', 'sm3') #Verifier computes random c = HASH(G, B, A) and sends c to Prover 
        # prover does not know x, have to generate a random x
        x = rand.randint( 1, tool.cuv.n-1 )
        m = (r + c * x) % tool.cuv.n # 

    _, mG  = tool.Mul_Point(m, tool.G) # Verifier checks that P = m · G − c · B = (r + c · x)· G − c · B = r · G + c · x · G − c · x · G = r · G = A
    _, cB  = tool.Mul_Point(c, B)
    P = tool.Add_Point(mG, cB.neg_point())

    if P.is_equal(A):
        OK = True

    return OK
                                    

def ZKP_Schnorr_test(cid, round):
    honest = 0

    for i in range(round):
        if ZKP_Schnorr(cid, True):
            honest += 1
    print(f"Prover Honest test--> {round} rounds: honest count = {honest}")

    honest = 0
    for i in range(round):
        if ZKP_Schnorr(cid, False):
            honest += 1

    print(f"Prover DisHonest test--> {round} rounds: honest count = {honest}")

if __name__ == '__main__':
    cid = int(ECC.SECP256K1)
    ZKP_DLwCF_test(cid, 10)
    ZKP_Schnorr_test(cid, 10)



