''' python version need > 3.5'''

from random import SystemRandom # cryptographic random byte generator
rand = SystemRandom()

## common lib

# From http://rosettacode.org/wiki/Modular_inverse#Python
def half_extended_gcd(aa, bb):
	lastrem, rem = abs(aa), abs(bb)
	x, lastx = 0, 1
	while rem:
		lastrem, (quotient, rem) = rem, divmod(lastrem, rem)
		x, lastx = lastx - quotient*x, x
	return lastrem, lastx 

def modular_inverse(a, m):
    ''' compute the multiplicative inverse, i.e. for x*a = a*x = 1 (mod m), return x '''
    assert a>0 , "The operator value a must be >0 for this pllication"
    g, x = half_extended_gcd(a, m)
    if g != 1:
        raise ValueError
    
    return x % m

def modular_exp_inv(a, m):
	''' compute the multiplicative inverse, by doing python native modulo exponentiation'''
	return pow(a, m-2, m)

def mod_inv_unittest (iteration):
    x = rand.randint(1, (1<<256)-1 )
    m = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F

    iter = 0
    pass_test = 0
    while iter < iteration:
        mod0 = modular_inverse (x, m)
        mod1 = modular_exp_inv (x, m)
        same = (mod0 == mod1)
        if not same:
            print("iteration #", iter, "fail: " )
            print("x   : 0x%064x" %(x) )
            print("m   : 0x%064x" %(m) )
            print("mod0: 0x%064x" %(mod0) )
            print("mod1: 0x%064x" %(mod1) )  

            print("  " )
        else: pass_test += 1
        iter += 1

    return pass_test

###################################################

class ECP:
    ''' EC point class, affine coordinate'''
    def __init__(self, P):
        "P must be tuple of (x, y)"
        self.x_ = P[0]
        self.y_ = P[1]
        if self.is_Unit_Point():
            print ("This is the Unit Point!")

    def is_Unit_Point(self):
        if self.x_ == 0 and self.y_ == 0:
            return True
        else:
            return False

    def is_reverse(self, Q, p):
        if (self.x_ == Q.x_) and (self.y_ == p - Q.y_):
            return True
    
    def neg_point(self, mod):
        ret = (self.x_, mod - self.y_)
        return ECP(ret)

    def print_point(self, mode):
        if mode == 'hex':
            print("Point.x(affine): ", hex( self.x_ ) )
            print("Point.y(affine): ", hex( self.y_ ) )
        elif mode == 'dec':
            print("Point.x(affine): ", self.x_ ) 
            print("Point.y(affine): ", self.y_ )

Unit = ECP ( (0,0) )

class ECC:
    '''EC curve'''
    def __init__(self, a, b, n, p, G:ECP, curve_id, name):
        self.a_ = a
        self.b_ = b
        self.n_ = n

        self.p_ = p
        self.G_ = G

        self.id_= curve_id
        self.name = name

        ### todo: check valid ###
        if (4* self.a_**3 + 27* self.b_**2) == 0:
            print ("Provided a and b not fit EC curve definition! ")

        if self.ECP_on_curve(G):
            print ("EC Curve: ", self.name, "init done" )

    def ECP_on_curve(self, P: ECP):
        left  = (P.y_** 2) % self.p_
        right = (P.x_** 3 + self.a_ * P.x_ + self.b_ ) % self.p_
        on_curve = (left == right)
        if not on_curve:
            print ("Priovided Point is NOT on curve: ")
            P.print_point('hex')

        return on_curve
    
    # def cal_slope0():
    #     '''when P and Q are same points, i.e. for Point double'''

    def Point_Dbl (self, P: ECP):
        '''calculate R = P + P = 2P'''
        x = P.x_
        y = P.y_

        # slope m
        m = ( 3*x**2    ) % self.p_
        m = (m + self.a_) % self.p_
        div = modular_inverse(2*y, self.p_)
        m = m*div % self.p_

        xo = (m**2 - x - x)    % self.p_
        yo = (y + m*(xo - x) ) % self.p_
        Point_Out = (xo, yo)
        T = ECP( Point_Out )
        R = T.neg_point(self.p_)
        return R

    def Point_Add (self, P: ECP, Q: ECP):
        '''calculate R = P + Q, when P != Q '''
        if Q.is_Unit_Point():
            return P
        if P.is_Unit_Point():
            return Q
        if Q.is_reverse(P, self.p_):
            return Unit

        # slope m
        m = ( P.y_ - Q.y_  ) % self.p_
            
        t2 = (P.x_ - Q.x_) % self.p_
        if t2 < 0:
            div = modular_inverse(t2+self.p_, self.p_)
        else:
            div = modular_inverse(t2, self.p_)
        
        m = m*div % self.p_
        
        xo = (m**2 - P.x_ - Q.x_)    % self.p_
        yo = (P.y_ + m*(xo - P.x_) ) % self.p_

        Point_Out = (xo, yo)
        T = ECP( Point_Out )
        R = T.neg_point(self.p_)
        return R

    def Point_Add_General (self, P: ECP, Q: ECP):
        '''calculate R = P + Q, for whatever P and Q (acceptable for P==Q) '''
        if Q.is_Unit_Point():
            return P
        if P.is_Unit_Point():
            return Q
        if Q.is_reverse(P, self.p_):
            return Unit
        
        if P == Q:
        # slope m for Dbl
            m = ( 3 * P.x_**2  ) % self.p_
            m = ( m + self.a_  ) % self.p_
            div = modular_inverse(2*P.y_, self.p_)
            m = m*div % self.p_

        else: 
        # slope m for Add
            # t1 = ( P.y_ - Q.y_  ) % self.p_
            # if t1 < 0:
            #     m = t1 + self.p_
            # else:
            #     m = t1
            m = ( P.y_ - Q.y_  ) % self.p_
            
            t2 = (P.x_ - Q.x_) % self.p_
            if t2 < 0:
                div = modular_inverse(t2+self.p_, self.p_)
            else:
                div = modular_inverse(t2, self.p_)
            m = m*div % self.p_

        # common for Output point:
        xo = ( m**2 - P.x_ - Q.x_  ) % self.p_
        if xo < 0:
            xo += self.p_
        yo = (P.y_ + m*(xo - P.x_) ) % self.p_
        if yo < 0:
            yo += self.p_

        Point_Out = (xo, yo)
        T = ECP( Point_Out )
        R = T.neg_point(self.p_)
        return R
        
    def Point_Mult(self, k, Pin: ECP, method):
        ''' Point multiply by scalar k'''
        assert not k < 0 , "Provided k < 0 !"
        assert self.ECP_on_curve(Pin) , "Provided Pin is not on curve!"

        if (k % self.n_) == 0 or Pin.is_Unit_Point():
            return Unit

        i = k
        R = Unit
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

    

################################################
## main ##

# unit test: modular inverse 
iter = 100
ret = mod_inv_unittest(iter)
print ("modular inv unit test: total %d iteration, pass %d " %(iter, ret) )
print ("=====================================")

# secp256k1 parameters
a  = 0
b  = 7
n  = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8

p  = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F

#Quick verify if (Gx, Gy) is on secp256k1 curve:
Gy**2 % p == (Gx**3 + Gx*a + b) % p

#init the curve:
pG = (Gx, Gy)
G = ECP(pG)
pI = (0, 0)
I = ECP(pI)

secp256k1 = ECC(a,b,n,p,G,714, "secp256k1")

#unit test: Point Double
print ("Point Double unit test: dG = G+G")
dG = secp256k1.Point_Dbl(G)
# dG.print_point('hex')
dG.print_point('dec')
print ("=====================================")

#unit test: Point Add: 
print ("Point Add unit test: tG = dG+G")
tG = secp256k1.Point_Add(dG, G)
# tG.print_point('hex')
tG.print_point('dec')
print ("=====================================")

#unit test: Point Add:
print ("Point Add unit test: Unit(0,0) = tG+tGn")
tGn = tG.neg_point(p)
U = secp256k1.Point_Add(tG, tGn)
U.print_point('hex')
# Unit.print_point('dec')
print ("=====================================")

#unit test: Point Add General: 
print ("Point Add General unit test 0: dG = G + G")
dG = secp256k1.Point_Add_General(G, G)
dG.print_point('dec')
print ("Point Add General unit test 1: tG = dG + G")
tG = secp256k1.Point_Add_General(dG, G)
tG.print_point('dec')
print ("Point Add General unit test 2: tG = tG + Uint")
tG_plus_I = secp256k1.Point_Add_General(tG, I)
tG_plus_I.print_point('dec')
print ("Point Add General unit test 3: Unit = tG + tGn")
tGn = tG.neg_point(p)
tG_plus_tGn = secp256k1.Point_Add_General(tG, tGn)
tG_plus_tGn.print_point('dec')
print ("=====================================")

#unit test: Point Multiply:
k = 111
method = 0
print ("Point Mult unit test 0: kG，k = %d, method = %d" %(k, method) )
kG = secp256k1.Point_Mult(k, G, method)
kG.print_point('dec')

method = 1
print ("Point Mult unit test 0: kG，k = %d, method = %d" %(k, method) )
kG = secp256k1.Point_Mult(k, G, method)
kG.print_point('dec')

# k = 8
# print ("Point Mult unit test 1: kG，k = %d" %(k) )
# kG = secp256k1.Point_Mult(k, G)
# kG.print_point('dec')

# P = 8G
# Px = 21262057306151627953595685090280431278183829487175876377991189246716355947009
# Py = 41749993296225487051377864631615517161996906063147759678534462689479575333124

# P = ECP( (Px, Py) )

# nineG = secp256k1.Point_Add_General(P, G)
# nineG.print_point('dec')
# print ("=====================================")

# nineG = secp256k1.Point_Add(P, G)
# nineG.print_point('dec')
# print ("=====================================")

# k = rand.randint(1, p )
# print ("Point Mult unit test 2: k random ")
# print ("k = 0x%064x" %(k) )
# print ("k = 0d%d" %(k) )
# kG = secp256k1.Point_Mult(k, G)
# kG.print_point('dec')

print ("=====================================")