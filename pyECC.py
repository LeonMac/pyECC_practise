
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
	g, x = half_extended_gcd(a, m)
	if g != 1:
		raise ValueError
	return x % m

###################################################
class ECP:
    ''' EC point class, affine coordinate'''
    def __init__(self, x, y):
        self.x_ = x
        self.y_ = y
        if self.is_infinite_point():
            print ("You get infinite point!")

    def is_infinite_point(self):
        if self.x_ == 0 and self.x_ == 0:
            return True
        else:
            return False

    def print_point(self ):
        print("Point.x(affine): ", hex( self.x_ ) )
        print("Point.y(affine): ", hex( self.y_ ) )


class ECC:
    '''EC curve'''
    def __init__(self, a, b, n, p, G:ECP, c_id, name):
        self.a_ = a
        self.b_ = b
        self.n_ = n

        self.p_ = p
        self.G_ = G
        self.id_= c_id
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
            P.print_point()

        return on_curve

################################################
## main ##

# secp256k1 parameters
a  = 0
b  = 7
n  = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8

p  = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F

#Quick verify if (Gx, Gy) is on secp256k1 curve:
Gy**2 % p == (Gx**3 + Gx*a + b) % p

G = ECP(Gx, Gy)
secp256k1_curve = ECC(a,b,n,p,G,714, "secp256k1")
