''' python version need > 3.5'''

from random import SystemRandom
rand = SystemRandom()   # cryptographic random byte generator

import modulo
from log import log
from ecp import ECP, JCB_ECP


class ECC:
    '''EC curve class'''
    def __init__(self, a:int, b:int, n:int, p:int, G:ECP, curve_id:int, name:str, jcb:bool = False):
        '''
        a, b, n, p, G: ECC domain parameters
        curve_id: for identify curve (secp256k1/p1, sm2)
        name: str of curve name
        jcb : bool, ECP is affine(default) or Jacobian
        '''
        self.a_ = a
        self.b_ = b
        self.n_ = n

        self.p_ = p
        self.G_ = G

        self.id_= curve_id
        self.name = name

        self.jcb = jcb

        assert ((4* self.a_**3 + 27* self.b_**2) != 0), "Provided a and b not fit EC curve definition! "

        assert (self.ECP_on_curve(G) ), "Provided Base Point G is not on curve! "

        if self.jcb:
            self.UNIT = ECP ( (0,0,1), self.p_ )
        else:
            self.UNIT = ECP ( (0,0), self.p_ )
        
        log('i', f"EC Curve: {self.name} init done" )

    def ECP_on_curve(self, P: ECP) -> bool:
        if self.jcb:
            x = P.get_x()
            y = P.get_y()

        else:
            x = P.x_
            y = P.y_

        y2 = (y*y)  % self.p_
        x2 = (x*x)  % self.p_
        x3 = (x2*x) % self.p_
        ax = (self.a_ * x) % self.p_

        left  = y2
        right = (x3 + ax + self.b_) % self.p_

        # left  = (P.y_** 2) % self.p_
        # right = (P.x_** 3 + self.a_ * P.x_ + self.b_ ) % self.p_

        on_curve = (left == right)
        if not on_curve:
            log('e', "Provided Point is NOT on curve: ")
            P.print_point('hex')

        return on_curve
    
    def Point_Dbl (self, P: ECP) -> ECP:
        '''calculate R = P + P = 2P'''
        x = P.x_
        y = P.y_

        # slope m
        m = ( 3*x**2    ) % self.p_
        m = (m + self.a_) % self.p_
        div = modulo.modular_inverse(2*y, self.p_)
        m = m*div % self.p_

        xo = (m**2 - x - x)    % self.p_
        yo = (y + m*(xo - x) ) % self.p_

        Rneg = ECP( (xo, yo), self.p_ )
        R = Rneg.neg_point(self.p_)
        return R

    def Point_Add (self, P: ECP, Q: ECP) -> ECP:
        '''calculate R = P + Q, when P != Q '''
        if Q.is_Unit_Point():
            return P
        if P.is_Unit_Point():
            return Q
        if Q.is_reverse(P):
            return self.UNIT

        # slope m
        m = ( P.y_ - Q.y_  ) % self.p_
            
        t2 = (P.x_ - Q.x_) % self.p_
        if t2 < 0:
            div = modulo.modular_inverse(t2+self.p_, self.p_)
        else:
            div = modulo.modular_inverse(t2, self.p_)
        
        m = m*div % self.p_
        
        xo = (m**2 - P.x_ - Q.x_)    % self.p_
        yo = (P.y_ + m*(xo - P.x_) ) % self.p_

        Rneg = ECP( (xo, yo), self.p_ )
        R = Rneg.neg_point(self.p_)
        return R

    def Point_Add_General (self, P: ECP, Q: ECP) -> ECP:
        '''calculate R = P + Q, for whatever P and Q (acceptable for P==Q) '''
        if Q.is_Unit_Point():
            return P
        if P.is_Unit_Point():
            return Q
        if Q.is_reverse(P):
            return self.UNIT
        
        if P.is_equal(Q):
        # slope m for Dbl
            m = ( 3 * P.x_**2  ) % self.p_
            m = ( m + self.a_  ) % self.p_
            div = modulo.modular_inverse(2*P.y_, self.p_)
            m = m*div % self.p_

        else: 
            m = ( P.y_ - Q.y_  ) % self.p_
            
            t2 = (P.x_ - Q.x_) % self.p_
            if t2 < 0:
                div = modulo.modular_inverse(t2+self.p_, self.p_)
            else:
                div = modulo.modular_inverse(t2, self.p_)
            m = m*div % self.p_

        # common for Output point:
        xo = ( m**2 - P.x_ - Q.x_  ) % self.p_
        if xo < 0:
            xo += self.p_
        yo = (P.y_ + m*(xo - P.x_) ) % self.p_
        if yo < 0:
            yo += self.p_

        Rneg = ECP( (xo, yo) , self.p_)
        R = Rneg.neg_point(self.p_)
        return R
        
    def Point_Mult(self, k:int, Pin: ECP, method = 1) -> ECP:
        ''' Point multiply by scalar k'''
        assert not k < 0 , "Provided k < 0 !"
        assert self.ECP_on_curve(Pin) , "Provided Pin is not on curve!"

        if (k % self.n_) == 0 or Pin.is_Unit_Point():
            return self.UNIT

        i = k
        R = self.UNIT
        P = Pin
        if method == 0:
            while i:
                if i & 0x1: # when i[bit0] == 1
                    R = self.Point_Add(P, R)

                P = self.Point_Dbl(P)
                i >>= 1

        if method == 1:
            while i:
                if i & 0x1: # when i[bit0] == 1
                    R = self.Point_Add_General(P, R)

                P = self.Point_Add_General(P, P)
                i >>= 1       

        return R
