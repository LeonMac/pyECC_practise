# import modulo
# from ecc import ECP, UNIT

# class JCB_ECP():
#     ''' EC point class, jacobian coordinate, inherited from ECP '''
#     def __init__(self, x, y, z, p):
#         self.X = x
#         self.Y = y
#         self.Z = z
#         self.p = p

#         # calcuate in advanced
#         self.Z2 = (self.Z  * self.Z) % self.p
#         self.Z3 = (self.Z2 * self.Z) % self.p

#     def get_x(self):
#         ''' x = X / Z^2 % p '''
#         Z2_inv = modulo.modular_inverse(self.Z2, self.p)
#         return (self.X * Z2_inv) % self.p

#     def get_y(self):
#         ''' y = Y / Z^3 % p '''
#         Z3_inv = modulo.modular_inverse(self.Z3, self.p)
#         return (self.Y * Z3_inv) % self.p
	
#     def get_z(self):
#         return self.Z % self.p

#     def get_ecp(self):
#         return ECP( (self.get_x() , self.get_y()) )

#     def is_Unit_Point(self):
#         '''JCB point Unit point (p, 0, no_matter) ? why'''
#         if self.X == self.p and self.Y == 0:
#             return True
#         else:
#             return False
    
#     def neg_point(self):
#         return JCB_ECP(self.X, (self.p - self.Y) % self.p, self.Z, self.p)

#     def print_point(self, method): 
#         if self.is_Unit_Point():
#             print("A Jacobian Identity Point (.x=p) nothing print")
#         elif (method == 'affine') :
#             x_a = self.get_x()
#             y_a = self.get_y()
#             print("Point.x(affine): ", hex( x_a ) )
#             print("Point.y(affine): ", hex( y_a ) )

#             print ("\n")
#             return ECP ( (x_a, y_a) )

#         else:
#             print("Point.X(Jacob):  ", hex( self.X ) )
#             print("Point.Y(Jacob):  ", hex( self.Y ) )
#             print("Point.Z(Jacob):  ", hex( self.Z ) )
#             print ("\n")
#             return (self.X , self.Y , self.Z, self.p)

class JCB_ECC():
    def __init__(self, a, b, n, p, G:JCB_ECP, curve_id, name):
        pass