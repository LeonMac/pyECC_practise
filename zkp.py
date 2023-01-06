# https://arxiv.org/pdf/1107.1626.pdf
# a saimple zkp demo implementation based on ECC

# 3.1 Zero Knowledge Proof of Discrete Logarithm with Coin Flip
import pyECC as ECC
from random import SystemRandom
rand = SystemRandom()


class zkp_tool():
    def __init__(cid:int, interaction: int = 1):
        cuv = ECC.ECC_Curve(cid)
        rnd = interaction
        pass
    
    def Gen_B (self, x): # x = None: simulate a dishonest Prover:
        
        if x == None: 
            act_x = rand.randint( 1, self.cuv.n-1 )
        else: act_x = x

        B = self.cuv.curve.Point_Mult(act_x, self.cuv.G)
        return B
    
    def Gen_A (self):
        r   = rand.randint( 1, self.cuv.n-1 )
        A   = self.cuv.curve.Point_Mult(r, self.cuv.G)
        return r, A

    def Gen_m (self, x, r):
        return (x + r) % self.cuv.n

def ZKP_DLwCF(cid):
    tool = zkp_tool(ECC.SECP256K1)
    r, A = tool.Gen_A()
    pass


