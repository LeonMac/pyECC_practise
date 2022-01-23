
class ECP:
    ''' EC point class, affine coordinate'''
    def __init__(self, x, y):
        self.x_ = x
        self.y_ = y
        #self.p_ = p

    def print_point(self ):
        print("Point.x(affine): ", hex( self.x_ ) )
        print("Point.y(affine): ", hex( self.y_ ) )


class ECC:
    '''EC curve'''
    
    def __init__(self, a, b, n, p, G:ECP, c_id, name):
        self.a_ = a
        self.b_ = b
        self.p_ = p
        self.n_ = n
        self.G_ = G
        self.id_= c_id
        self.name = name

        ### todo: check valid ###

        if not self.ECP_on_curve(G):
            print ("EC Curve ", self.name, "init done" )


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

G = ECP(Gx, Gy)
secp256k1_curve = ECC(a,b,n,p,G,714,"secp256k1" )
