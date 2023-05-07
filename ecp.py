from random import SystemRandom
rand = SystemRandom()   # cryptographic random byte generator

import modulo
from log import log

###################################################

class ECP:
    ''' EC point class, affine coordinate'''
    def __init__(self, P):
        '''P must be tuple of (x, y)'''
        assert (P[0] >= 0 ), "ECP.x must be >=0"
        assert (P[1] >= 0 ), "ECP.y must be >=0"

        self.x_ = P[0]
        self.y_ = P[1]
        # self.p  = p

        # if self.is_Unit_Point():
        #     log('i', "This is the UNIT Point!")

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
    

class JCB_ECP():
    ''' EC point class, jacobian coordinate '''
    def __init__(self, P, p):
        '''P must be tuple of (x, y, z)'''
        assert (P[0] >= 0 ), "ECP.x must be >=0"
        assert (P[1] >= 0 ), "ECP.y must be >=0"
        assert (P[2] >= 0 ), "ECP.z must be >=0"

        self.X = P[0]
        self.Y = P[1]
        self.Z = P[2]
        self.p = p

        # calcuate in advanced
        self.Z2 = (self.Z  * self.Z) % self.p
        self.Z3 = (self.Z2 * self.Z) % self.p

    def get_x(self):
        ''' x = X / Z^2 % p '''
        Z2_inv = modulo.modular_inverse(self.Z2, self.p)
        return (self.X * Z2_inv) % self.p

    def get_y(self):
        ''' y = Y / Z^3 % p '''
        Z3_inv = modulo.modular_inverse(self.Z3, self.p)
        return (self.Y * Z3_inv) % self.p
	
    def get_z(self):
        return self.Z % self.p

    def get_ecp(self):
        return ECP( (self.get_x() , self.get_y()) )

    def is_Unit_Point(self):
        '''JCB point Unit point (p, 0, no_matter) ? why'''
        if self.X == self.p and self.Y == 0:
            return True
        else:
            return False
    
    def neg_point(self):
        return JCB_ECP(self.X, (self.p - self.Y) % self.p, self.Z, self.p)

    def print_point(self, method): 
        if self.is_Unit_Point():
            print("A Jacobian Identity Point (.x=p) nothing print")
        elif (method == 'affine') :
            x_a = self.get_x()
            y_a = self.get_y()
            print("Point.x(affine): ", hex( x_a ) )
            print("Point.y(affine): ", hex( y_a ) )

            print ("\n")
            return ECP ( (x_a, y_a) )

        else:
            print("Point.X(Jacob):  ", hex( self.X ) )
            print("Point.Y(Jacob):  ", hex( self.Y ) )
            print("Point.Z(Jacob):  ", hex( self.Z ) )
            print ("\n")
            return (self.X , self.Y , self.Z, self.p)
