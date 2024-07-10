from random import SystemRandom
rand = SystemRandom()   # cryptographic random byte generator

import modulo
from log import log
from support import debug_control

###################################################

def log_point(log_msg: str, data:int, data_format:str='hex'):
    if data_format == 'hex':
        log('d', f"{log_msg}: {hex( data )}" )
    elif data_format == 'dec':
        log('d', f"{log_msg}: { data }" )
    else:
        log('w', f"[log_point]: unkown format signature {data_format}")

def print_aff_point(x:int, y:int, data_format):
    log_point("Point.x(affine)", x, data_format)
    log_point("Point.y(affine)", y, data_format)
    print ("\n")


def print_jcb_point(X:int, Y:int, Z:int, data_format):
    log_point("Point.X(Jacob)", X, data_format)
    log_point("Point.Y(Jacob)", Y, data_format)
    log_point("Point.Z(Jacob)", Z, data_format)
    print ("\n")

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

    # @debug_control
    def print_point(self, cord_format='aff', data_format:str = 'hex'):
        print_aff_point(self.x_, self.y_, data_format)

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
    
#todo jacobian mode timing is higher than affine, some operation need to be optimized
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

    # @debug_control
    def print_point(self, cord_format='aff', data_format='hex'): 
        if (cord_format == 'aff') :
            x_a = self.get_x()
            y_a = self.get_y()
            print_aff_point(x_a, y_a, data_format)
        elif (cord_format == 'jcb'):
            print_jcb_point(self.X, self.Y, self.Z, data_format)
        else:
            log('w', f"unkown format signature {cord_format}")


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