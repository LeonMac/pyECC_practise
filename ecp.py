from random import SystemRandom
rand = SystemRandom()   # cryptographic random byte generator

import modulo
from log import log

###################################################

class ECP_AFF:
    ''' EC point class, affine coordinate'''
    def __init__(self, P, p:int):
        '''P EC affine point: tuple of (x, y)
           p : curve prime 
        '''
        assert (P[0] >= 0 ), "ECP.x must be >=0"
        assert (P[1] >= 0 ), "ECP.y must be >=0"

        self.x_ = P[0] % p
        self.y_ = P[1] % p
        self.p  = p

        # if self.is_Unit_Point():
        #     log('i', "This is the UNIT Point!")

        self.y_even = (self.y_ & 0b1) # ry odd (1) even (0)

    def is_Unit_Point(self):
        return ( self.x_ == 0 and self.y_ == 0 )

    def is_reverse(self, P):
        return (self.x_ == P.x_ and self.y_ == self.p - P.y_)

    def is_equal(self, P):
        return (self.x_ == P.x_ and self.y_ == P.y_)

    def neg_point(self):
        ret = (self.x_, self.p - self.y_)
        return ECP_AFF(ret, self.p)

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
    

class ECP_JCB():
    ''' EC point class, Jacobian coordinate '''
    def __init__(self, P, p):
        '''P EC Jacobian point: tuple of (x, y, z)
           p : curve prime 
        '''
        assert (P[0] >= 0 ), "ECP.x must be >=0"
        assert (P[1] >= 0 ), "ECP.y must be >=0"
        assert (P[2] >= 0 ), "ECP.z must be >=0"
        assert (p > 0 ), "p must be >0"

        self.X = P[0] % p
        self.Y = P[1] % p
        self.Z = P[2] % p
        self.p = p

        # calcuate in advanced
        self.Z2 = (self.Z  * self.Z) % self.p
        self.Z3 = (self.Z2 * self.Z) % self.p
        self.y_even = (self.get_y() & 0b1) # ry odd (1) even (0)

    def get_x(self):
        ''' x = X / Z^2 % p '''
        Z2_inv = modulo.modular_inverse(self.Z2, self.p)
        return (self.X * Z2_inv) % self.p

    def get_y(self):
        ''' y = Y / Z^3 % p '''
        Z3_inv = modulo.modular_inverse(self.Z3, self.p)
        return (self.Y * Z3_inv) % self.p
	
    def get_z(self):
        return self.Z

    def get_ecp(self):
        return ECP_AFF( (self.get_x() , self.get_y()), self.p )

    def is_Unit_Point(self):
        '''JCB point Unit point'''
        # if self.X % self.p == 0 and self.Y % self.p == 0:
        return ( (self.get_x() == 0 ) and  (self.get_y() ==  0)  )

    def is_reverse(self, P):
        return ( self.get_x() == P.get_x() and (self.get_y() == self.p - P.get_y()) )
        
    def is_equal(self, P):
        return ( self.get_x() == P.get_x() and self.get_y() == P.get_y() )
        
    def neg_point(self):
        return ECP_JCB( (self.X, (self.p - self.Y) % self.p, self.Z), self.p)

    def print_point(self, method='affine'): 
        if self.is_Unit_Point():
            print("this is an Unit Point!")

        if (method == 'affine') :
            x_a = self.get_x()
            y_a = self.get_y()
            print("Point.x(affine): ", hex( x_a ) )
            print("Point.y(affine): ", hex( y_a ) )

            print ("\n")
            return ECP_AFF ( (x_a, y_a) , self.p)

        elif (method == 'jacobian'):
            print("Point.X(Jacob):  ", hex( self.X ) )
            print("Point.Y(Jacob):  ", hex( self.Y ) )
            print("Point.Z(Jacob):  ", hex( self.Z ) )
            print ("\n")
            return ECP_JCB ((self.X , self.Y , self.Z), self.p)

    def hex_str(self, format='xy', compress = False):
        if   format == 'xy':
            ret = "{:064x}".format(self.get_x()) + "{:064x}".format(self.get_y())
        elif format == 'x':
            ret = "{:064x}".format(self.get_x())
        elif format == 'y':
            ret = "{:064x}".format(self.get_y())

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