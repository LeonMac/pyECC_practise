''' python version need > 3.5'''

from random import SystemRandom
#from xmlrpc.client import boolean 
rand = SystemRandom()   # cryptographic random byte generator

import helper
import modulo
import ecc

class ECC_Curve ():
    ''' instance implement of ECC libarary '''
    # secp256k1 parameters
    def __init__(self, curve_id):
        if (curve_id == 714): # openssl curve_id for secp256k1
            self.a  = 0
            self.b  = 7
            self.n  = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

            self.Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
            self.Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8

            self.p  = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
            self.name = "secp256k1"

        elif (curve_id == 415): # openssl curve_id for secp256r1=prime256v1
            self.a  = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFC
            self.b  = 0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B
            self.n  = 0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551

            self.Gx = 0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296
            self.Gy = 0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5

            self.p  = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF
            self.name = "secp256r1"
        else:
            print ("Un-support curve!")
            return

        self.G  = ecc.ECP( (self.Gx, self.Gy) )
        self.U  = ecc.Unit

        self.curve = ecc.ECC(self.a,self.b,self.n,self.p,self.G, curve_id, self.name)
    
    def PubKey_Gen(self, k, verb: bool):
        Pubkey = self.curve.Point_Mult(k, self.curve.G_, 0)
        if (verb):
            print("given privkey = 0x%064x" %(k) )
            print("Generated Pubkey:" )
            Pubkey.print_point('hex')
        
        return Pubkey

    def Sig_Gen(self, priv_key, randk, sh256_dig, formt:str, verb: bool):
        '''Input:  priv_key, randk, sha256_dig, pub_key format (comp|non-comp)'''
        '''Output: sig_r, sig_s, dig, pub_key_x, pub_key_y'''
        assert not priv_key  > self.curve.n_ , "Provided private key > curve n!"
        assert not randk > self.curve.n_ , "Provided randomk > curve n!"
        #assert not sh256_dig <= self.curve.n_ , "Provided digest > curve n!"
        if sh256_dig >= self.curve.n_ :
            z = sh256_dig - self.curve.n_
        else:
            z = sh256_dig

        pub_key = self.PubKey_Gen(priv_key, verb)

        rx = 0
        s  = 0
        while not rx and not s:
            R  = self.PubKey_Gen(randk, verb)
            rx = R.x_
            ry = R.y_
            s = ((z + rx * priv_key) * modulo.modular_inverse(randk, self.curve.n_)) % self.curve.n_

        '''todo: low-x here rx is possibly > n? in such case do we need reduce rx by rx-n?'''
        '''todo: low-s here s is possibly > n/2?'''
        return (rx, s, z, pub_key.x_, pub_key.y_)
    
    def Signature_Verify(self, r, s, z, pub_x, pub_y):
        s_inv = modulo.modular_inverse (s, self.curve.n_)

        u1 = (z * s_inv) % self.curve.n_
        u2 = (r * s_inv) % self.curve.n_

        u1G = self.curve.Point_Mult(u1, self.curve.G_, 0)
        u2P = self.curve.Point_Mult(u2, ecc.ECP((pub_x, pub_y)), 0)

        R = self.curve.Point_Add_General(u1G, u2P)

        ret = ( r  == (R.x_ % self.curve.n_) ) ## signature verify pass/fail
        return ret

    ###############################################
    def ECDH (self, self_priv_key, counter_part_PubKey: ecc.ECP):
        assert self.curve.ECP_on_curve(counter_part_PubKey) , "Provided Pubkey is not on curve!"
        assert not self_priv_key  > self.curve.n_ , "Provided private key > curve n!"

        Q = self.curve.Point_Mult(self_priv_key, counter_part_PubKey, 0)
        return Q


    ###############################################

    def Encryption(self, Msg:str, Pub:ecc.ECP ):
        assert self.curve.ECP_on_curve(Pub) , "Provided Pubkey is not on curve!"

        dP = self.U
        while (dP == self.U):
            d  = rand.randint(1, self.curve.n_ )
            dP = self.curve.Point_Mult(d, self.curve.G_, 0)

        R  = self.Unit
        while (R == self.U):
            k = rand.randint(1, self.curve.n_ )
            R = self.curve.Point_Mult(k, self.curve.G_, 0)
        

        pass

    def Decryption():
        pass

###########################################################
def Sig_Verify_unit_test(curve_id, test_round):
    ''' signature generate and verify test '''
    helper.print_devider('line', 1)
    print ("Signature generate+signature verify test, plan to run %d" %(test_round))
    curve_ins = ECC_Curve(curve_id)

    i = 0
    test_pass = 0
    msg = "This is a masterpiece from Tiger.Tang"
    dig = helper.hash_256(msg)

    while i < test_round: 

        priv_key = rand.randint(1, curve_ins.n )
        randk    = rand.randint(1, curve_ins.n )

        pub_key  = curve_ins.PubKey_Gen(priv_key, False)
        r,s,z,x,y = curve_ins.Sig_Gen(priv_key, randk, dig, 'non-compress', False )
        if curve_ins.Signature_Verify(r,s,z,x,y):
            test_pass+=1
        
        i+=1
    
    print ("Signature generate+signature verify test round %d, %d pass" %(test_round, test_pass))
    helper.print_devider('line', 1)

    return test_pass


def ECDH_unit_test(curve_id, test_round):
    ''' ECDH test '''
    print ("ECDH test, plan to run %d" %(test_round))
    curve_ins = ECC_Curve(curve_id)

    i = 0
    test_pass = 0
    while i < test_round:
        # Alice private key and Pubkey
        da = rand.randint(1, curve_ins.n )
        Pa = curve_ins.PubKey_Gen(da, False)

        # Bob private key and Pubkey
        db = rand.randint(1, curve_ins.n )
        Pb = curve_ins.PubKey_Gen(db, False)

        # Alice Pubkey sent to Bob, Bob calculate Share secret
        S_bob = curve_ins.ECDH(db, Pa)

        # Bob Pubkey sent to Alice, Alice calculate Share secret
        S_alice = curve_ins.ECDH(da, Pb)

        if S_bob.is_equal(S_alice):
            test_pass += 1

        i += 1
    
    print ("EDCH test round %d, %d pass" %(test_round, test_pass))
    helper.print_devider('line', 1)

    return test_pass
   


####################################################
## ECC unit test
## this website can generate test vector and comapre with our result
## http://www-cs-students.stanford.edu/~tjw/jsbn/ecdh.html
def ECC_unit_test (curve_id):
    '''do unit test for Point_Add Point_Double print test vector
       compare the result with http://www-cs-students.stanford.edu/~tjw/jsbn/ecdh.html
    '''
    curve_ins = ECC_Curve(curve_id)
    #unit test: Point Double
    helper.log('i', "Point Double unit test: dG = G+G")
    dG = curve_ins.curve.Point_Dbl(curve_ins.G)
    # dG.print_point('hex')
    dG.print_point('dec')
    helper.print_devider('line',1)

    #unit test: Point Add: 
    helper.log('i', "Point Add unit test: tG = dG+G")
    tG = curve_ins.curve.Point_Add(dG, curve_ins.G)
    # tG.print_point('hex')
    tG.print_point('dec')
    helper.print_devider('line',1)

    #unit test: Point Add:
    helper.log ('i',"Point Add unit test: Unit(0,0) = tG+tGn")
    tGn = tG.neg_point(curve_ins.p)
    U = curve_ins.curve.Point_Add(tG, tGn)
    U.print_point('hex')
    # Unit.print_point('dec')
    helper.print_devider('line',1)

    #unit test: Point Add General: 
    helper.log ('i', "Point Add General unit test 0: dG = G + G")
    dG = curve_ins.curve.Point_Add_General(curve_ins.G, curve_ins.G)
    dG.print_point('dec')
    helper.log ('i', "Point Add General unit test 1: tG = dG + G")
    tG = curve_ins.curve.Point_Add_General(dG, curve_ins.G)
    tG.print_point('dec')
    helper.log ('i', "Point Add General unit test 2: tG = tG + Uint")
    tG_plus_I = curve_ins.curve.Point_Add_General(tG, curve_ins.U)
    tG_plus_I.print_point('dec')
    helper.log ('i', "Point Add General unit test 3: Unit = tG + tGn")
    tGn = tG.neg_point(curve_ins.p)
    tG_plus_tGn = curve_ins.curve.Point_Add_General(tG, tGn)
    tG_plus_tGn.print_point('dec')
    helper.print_devider('line',1)

    #unit test: Point Multiply:
    k = 111
    method = 0
    helper.log ('i', "Point Mult unit test 0: kG，k = %d, method = %d" %(k, method) )
    kG = curve_ins.curve.Point_Mult(k, curve_ins.G, method)
    kG.print_point('dec')

    method = 1
    helper.log ('i', "Point Mult unit test 0: kG，k = %d, method = %d" %(k, method) )
    kG = curve_ins.curve.Point_Mult(k, curve_ins.G, method)
    kG.print_point('dec')
    helper.print_devider('line',1)

    k = rand.randint(1, curve_ins.n )
    helper.log ('i', "Point Mult unit test 2: k random ")
    print ("k = 0x%064x" %(k) )
    print ("k = 0d%d" %(k) )
    kG0 = curve_ins.curve.Point_Mult(k, curve_ins.G, 0)
    kG0.print_point('dec')

    kG1 = curve_ins.curve.Point_Mult(k, curve_ins.G, 1)
    kG1.print_point('dec')
    helper.print_devider('line',1)

#####
def Curve_unit_test (curve_id):
    '''do unit test for curve unit test '''
    curve_ins = ECC_Curve(curve_id)

    k = rand.randint(1, curve_ins.n )
    helper.log ('i', "Pubkey gen unit test:")
    print ("PrivKey = 0d%d" %(k) )
    Pubkey = curve_ins.PubKey_Gen(k, True)
    helper.print_devider('line', 1)
    
    pass


def Point_Addition_HE_test (curve_id, test_round):
    '''Point Add homomorphic encryption test '''
    print ("Point Add homomorphic encryption test, plan to run %d" %(test_round))
    curve_ins = ECC_Curve(curve_id)

    i = 0
    test_pass = 0
    while i < test_round:  

        k1 = rand.randint(curve_ins.n -10, curve_ins.n )
        #k1 = i+1
        #print ("k1 = 0d%d" %(k1) )
        k1G = curve_ins.PubKey_Gen(k1, False)

        k2 = rand.randint(curve_ins.n - i*10, curve_ins.n )
        #k2 = 2*i+3

        #print ("k2 = 0d%d" %(k2) )
        k2G = curve_ins.PubKey_Gen(k2, False)

        kG_0  = curve_ins.curve.Point_Add_General(k1G, k2G)

        k = (k1 + k2) % curve_ins.n

        kG_1  = curve_ins.PubKey_Gen(k, False)

        if kG_0.is_equal(kG_1) :
            test_pass +=1
        else:
            print ("Test round %d of %d fail" %(i, test_round))
            kG_0.print_point('hex')
            kG_1.print_point('hex')

        i+=1
    print ("Total test round %d, %d pass" %(test_round, test_pass))
    helper.print_devider('line', 1)

    return test_pass
   
   

################################################
## main ##

# curve_id, same as openssl
curve_id_sk1 = 714 # secp256k1
curve_id_sr1 = 415 # secp256r1

# ecc library test
ECC_unit_test(curve_id_sk1)
helper.print_devider('double', 1)
ECC_unit_test(curve_id_sr1)
helper.print_devider('double', 1)
#####################################

# Curve test
Curve_unit_test (curve_id_sk1)
helper.print_devider('double', 1)
Curve_unit_test (curve_id_sr1)
helper.print_devider('double', 1)

#####################################
# Point_Addition_HE test
Point_Addition_HE_test(curve_id_sk1, 100)
helper.print_devider('double', 1)

#####################################
# signature gen/ verify test
Sig_Verify_unit_test(curve_id_sk1, 100)
helper.print_devider('double', 1)
Sig_Verify_unit_test(curve_id_sr1, 100)
helper.print_devider('double', 1)

#####################################
# ECDH test

ECDH_unit_test(curve_id_sk1, 100)
helper.print_devider('double', 1)
ECDH_unit_test(curve_id_sr1, 100)
helper.print_devider('double', 1)