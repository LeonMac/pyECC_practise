# https://arxiv.org/pdf/1107.1626.pdf
# a saimple zkp demo implementation based on ECC

# 3.1 Zero Knowledge Proof of Discrete Logarithm with Coin Flip
import pyECC as ECC
from random import SystemRandom
rand = SystemRandom()


class zkp_tool():
    def __init__(self, cid:int, interaction: int = 1):
        self.cuv = ECC.ECC_Curve(cid)
        self.rnd = interaction
        pass
    
    def Gen_Point (self, k=None): # x = None: simulate a dishonest Prover:
        
        if k == None: 
            k_ = rand.randint( 1, self.cuv.n-1 )
        else: k_ = k

        B = self.cuv.curve.Point_Mult(k_, self.cuv.G)
        return k_ , B
    
    # def Gen_A (self):
    #     r   = rand.randint( 1, self.cuv.n-1 )
    #     A   = self.cuv.curve.Point_Mult(r, self.cuv.G)
    #     return r, A

    # def Gen_Point (self):
    #     k   = rand.randint( 1, self.cuv.n-1 )
    #     P   = self.cuv.curve.Point_Mult(k, self.cuv.G)
    #     return k, P

    def Gen_m (self, x, r):
        return (x + r) % self.cuv.n

    

def ZKP_DLwCF(cid:int, round:int):
    tool = zkp_tool(cid)
    x, B = tool.Gen_Point(None)  # B is known by both Prover and Verifier

    for rnd in range (round):
        r, A = tool.Gen_Point(None)
        flip_coin = rand.randint( 0, 1 )
        if flip_coin: # HEAD
            # if A == P in 
            pass



if __name__ == '__main__':
    cid = int(ECC.SECP256K1)

    ZKP_DLwCF(cid, 1)