''' python version need > 3.5'''

from random import SystemRandom
rand = SystemRandom()   # cryptographic random byte generator

import modulo
from log import log

###################################################
## ECP = EC Point
class ECP:
    ''' EC point class, affine coordinate'''
    def __init__(self, P):
        '''P must be tuple of (x, y)'''
        assert (P[0] >= 0 ), "ECP.x must be >0"
        assert (P[1] >= 0 ), "ECP.y must be >0"

        self.x_ = P[0]
        self.y_ = P[1]

        if self.is_Unit_Point():
            log('w', "This is the UNIT Point!")

        self.y_even = (self.y_ & 0b1) # ry odd (1) even (0)

    def is_Unit_Point(self):
        if self.x_ == 0 and self.y_ == 0:
            return True
        else:
            return False

    def is_reverse(self, P, p):
        if (self.x_ ==P.x_) and (self.y_ == p - P.y_):
            return True

    def is_equal(self, P):
        if (self.x_ == P.x_) and (self.y_ == P.y_):
            return True
    
    def neg_point(self, mod):
        ret = (self.x_, mod - self.y_)
        return ECP(ret)

    def print_point(self, format:str = 'hex'):
        if format == 'hex':
            log('d', f"Point.x(affine): {hex( self.x_ )}" )
            log('d', f"Point.y(affine): {hex( self.y_ )}" )
        elif format == 'dec':
            log('d', f"Point.x(affine): {self.x_ }") 
            log('d', f"Point.y(affine): {self.y_ }")
    
    def hex_str(self, format='xy', compress = False):
        if   format == 'xy':
            ret = "{:064x}".format(self.x_) + "{:064x}".format(self.y_)
        elif format == 'x':
            ret = "{:064x}".format(self.x_)
        elif format == 'y':
            ret = "{:064x}".format(self.y_)

        if compress:
            if self.y_even:
                PC = '03'
            else:
                PC = '02'
        elif compress == False:
            PC = '04'
        elif compress == None:
            PC = ''
        
        return PC + ret

# define Global constant UNIT Point by using (0,0)
UNIT = ECP ( (0,0) )

# ECC = EC Curve
class ECC:
    '''EC curve class'''
    def __init__(self, a, b, n, p, G:ECP, curve_id, name):
        self.a_ = a
        self.b_ = b
        self.n_ = n

        self.p_ = p
        self.G_ = G

        self.id_= curve_id
        self.name = name

        assert ((4* self.a_**3 + 27* self.b_**2) != 0), "Provided a and b not fit EC curve definition! "

        assert (self.ECP_on_curve(G) ), "Provided Base Point G is not on curve! "
        
        log('i', f"EC Curve: {self.name} init done" )

    def ECP_on_curve(self, P: ECP):
        left  = (P.y_** 2) % self.p_
        right = (P.x_** 3 + self.a_ * P.x_ + self.b_ ) % self.p_
        on_curve = (left == right)
        if not on_curve:
            log('e', "Provided Point is NOT on curve: ")
            P.print_point('hex')

        return on_curve
    
    def Point_Dbl (self, P: ECP):
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

        Rneg = ECP( (xo, yo) )
        R = Rneg.neg_point(self.p_)
        return R

    def Point_Add (self, P: ECP, Q: ECP):
        '''calculate R = P + Q, when P != Q '''
        if Q.is_Unit_Point():
            return P
        if P.is_Unit_Point():
            return Q
        if Q.is_reverse(P, self.p_):
            return UNIT

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

        Rneg = ECP( (xo, yo) )
        R = Rneg.neg_point(self.p_)
        return R

    def Point_Add_General (self, P: ECP, Q: ECP):
        '''calculate R = P + Q, for whatever P and Q (acceptable for P==Q) '''
        if Q.is_Unit_Point():
            return P
        if P.is_Unit_Point():
            return Q
        if Q.is_reverse(P, self.p_):
            return UNIT
        
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

        Rneg = ECP( (xo, yo) )
        R = Rneg.neg_point(self.p_)
        return R
        
    def Point_Mult(self, k:int, Pin: ECP, method = 1):
        ''' Point multiply by scalar k'''
        assert not k < 0 , "Provided k < 0 !"
        assert self.ECP_on_curve(Pin) , "Provided Pin is not on curve!"

        if (k % self.n_) == 0 or Pin.is_Unit_Point():
            return UNIT

        i = k
        R = UNIT
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
