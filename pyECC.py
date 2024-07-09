#!/usr/bin/env python3
import sys

#import random
from random import SystemRandom
rand = SystemRandom()   # cryptographic random byte generator

from log import log, hex_show
from log import print_divider as log_div
from support import hexstr2byte

import modulo

from ecc import ECC
from support import timing_log

from config import USE_JCB

if USE_JCB:
    from ecp import ECP_JCB as ECP
    log_method = 'jacobian' # 'affine'
else:
    from ecp import ECP_AFF as ECP
    log_method = 'hex' # 'dec'

SECP256K1 = 714 # openssl curve_id for secp256k1
SECP256R1 = 415 # openssl curve_id for secp256r1=prime256v1
SM2_CV_ID = 123 # openssl curve_id for sm2, to be confirmed
SM2_TV_ID = 124 # a temp assigned curve id for sm2 test vector


class ECC_Curve ():
    ''' instance implement of ECC libarary '''
    def __init__(self, curve_id):
        if (curve_id == SECP256K1): # openssl curve_id for secp256k1
            self.a  = 0
            self.b  = 7
            self.n  = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

            self.Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
            self.Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8

            self.p  = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
            self.h  = 0x1
            self.name = "secp256k1"
            self.family = "NIST"

        elif (curve_id == SECP256R1): # openssl curve_id for secp256r1=prime256v1
            self.a  = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFC
            self.b  = 0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B
            self.n  = 0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551

            self.Gx = 0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296
            self.Gy = 0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5

            self.p  = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF
            self.h  = 0x1
            self.name = "secp256r1"
            self.family = "NIST"

        elif (curve_id == SM2_CV_ID): 
            self.a  = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
            self.b  = 0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
            self.n  = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123

            self.Gx = 0x32c4ae2c1f1981195f9904466a39c9948fe30bbff2660be1715a4589334c74c7
            self.Gy = 0xbc3736a2f4f6779c59bdcee36b692153d0a9877cc62a474002df32e52139f0a0

            self.p  = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
            self.h  = 0x1
            self.name = "sm2"
            self.family = "SM2"

        elif (curve_id == SM2_TV_ID): 
            self.a  = 0x787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498
            self.b  = 0x63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A
            self.n  = 0x8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7

            self.Gx = 0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D
            self.Gy = 0x0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2

            self.p  = 0x8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3
            self.h  = 0x1
            self.name = "sm2_test"
            self.family = "SM2"

        else:
            assert False, f"Un-support curve id {curve_id}!"
        if USE_JCB:
            self.G  = ECP( (self.Gx, self.Gy, 1), self.p )
        else:
            self.G  = ECP( (self.Gx, self.Gy), self.p )
        
        self.curve = ECC(self.a, self.b, self.n, self.p, self.G, curve_id, self.name, USE_JCB)

        
    
    def PubKey_Gen(self, k:int, verb: bool = False):
        '''Input: scalar k
           Output kG '''
        Pubkey = self.curve.Point_Mult(k, self.G, 1)
        if (verb):
            log('d', f"given privkey = 0x%064x" %(k) )
            log('d', "Generated Pubkey:" )
            Pubkey.print_point(log_method)
        
        return Pubkey

    def NIST_Sig_Gen(self, priv_key, randk, sh256_dig, formt:str, verb: bool):
        ''' Elliptic Curve Digital Signature Algorithm (ECDSA)
        Input:  priv_key, randk, sha256_dig, pub_key format (comp|non-comp)
        Output: sig_r, sig_s, dig, pub_key_x, pub_key_y
        '''
        assert self.family != "SM2", f"this config is NOT for NIST"
        assert priv_key  < self.n , "Provided private key >= curve n!"
        assert randk < self.n , "Provided randomk >= curve n!"
        #assert not sh256_dig <= self.n , "Provided digest > curve n!"
        if sh256_dig >= self.n :
            z = sh256_dig - self.n
        else:
            z = sh256_dig

        pub_key = self.PubKey_Gen(priv_key, verb)

        rx = 0
        s  = 0
        while not rx and not s:
            R  = self.PubKey_Gen(randk, verb)
            if USE_JCB:
                rx = R.get_x()
                pub_x = pub_key.get_x()
                pub_y = pub_key.get_y()

            else:    
                rx = R.x_
                pub_x = pub_key.x_
                pub_y = pub_key.y_
            
            s = ((z + rx * priv_key) * modulo.modular_inverse(randk, self.n)) % self.n

        '''todo: low-x here rx is possibly > n? in such case do we need reduce rx by rx-n?'''
        '''todo: low-s here s is possibly > n/2?'''
        return (rx, s, z, pub_x, pub_y)

    def SigBody_Validate(self, r, s, z, x, y):
        assert r < self.n , "Provided sig.s >= curve n!"
        assert s < self.n , "Provided sig.r >= curve n!"
        assert z < self.n , "Provided sig.z >= curve n!"
        assert x < self.p , "Provided pub.x >= curve p!"
        assert y < self.p , "Provided pub.y >= curve p!"

    def NIST_Sig_Verify(self, r, s, z, pub_x, pub_y):
        assert self.family != "SM2", f"this config is NOT for NIST"

        self.SigBody_Validate(r, s, z, pub_x, pub_y)

        s_inv = modulo.modular_inverse (s, self.n)

        u1 = (z * s_inv) % self.n
        u2 = (r * s_inv) % self.n

        u1G = self.curve.Point_Mult(u1, self.G, 0)

        if USE_JCB:
            u2P = self.curve.Point_Mult(u2, ECP((pub_x, pub_y, 1), self.p), 0)
        else:
            u2P = self.curve.Point_Mult(u2, ECP((pub_x, pub_y), self.p), 0)

        R = self.curve.Point_Add_General(u1G, u2P)
        if USE_JCB:
            ret = ( r  == (R.get_x() % self.n) ) 
        else: 
            ret = ( r  == (R.x_ % self.n) )
        return ret
    
    def SM2_Sig_Gen(self, priv_key, randk, ZaM, formt:str, verb: bool):
        ''' SM2 Spec, Part 2, 6.1 '''
        assert self.family != "NIST", f"this config is NOT for SM2"

        e = 0
        if (ZaM >= self.n):
            e = self.n
        else: 
            e = ZaM   
        
        r = 0
        s = 0
        da = priv_key

        k_temp = rand.randint(1, self.n-1 )
        

        Pub = self.curve.Point_Mult(da, self.G, 0)

        if USE_JCB:
            pub_x, pub_y = Pub.get_x(), Pub.get_y() 
        else:
            pub_x, pub_y = Pub.x_, Pub.y_


        del k_temp

        while s == 0 :
            while r == 0 :
                if randk == 0:
                    k = rand.randint(1, self.n-1 )
                else:
                    k = randk

                kG = self.curve.Point_Mult(k, self.G, 0)
                if USE_JCB:
                    r = (e + kG.get_x()) % self.n
                else:
                    r = (e + kG.x_) % self.n
            #print("x1      : 0x%064x" %(x1) )
            rda   = ( r * da ) % self.n
            k_rda = ( k - rda) % self.n
            da1_inv = modulo.modular_inverse(da+1, self.n)
            s = ( da1_inv * k_rda ) % self.n

        return (r, s, e, pub_x, pub_y) 

    def SM2_Sig_Verify(self, r, s, e, p_x, p_y):
        ''' SM2 Spec, Part 2, 6.2 '''
        assert self.family != "NIST", f"this config is NOT for SM2"

        self.SigBody_Validate(r, s, e, p_x, p_y)
        if USE_JCB:
            P = ECP((p_x, p_y, 1), self.p)
        else:
            P = ECP((p_x, p_y), self.p)

        if not  self.curve.ECP_on_curve(P):
            print ("provided pubkey is not on curve")
            return False

        t = (r + s) % self.n
        
        if t==0:
            print ("r + s == 0")
            return False


        # e = ZaM
        
        sG = self.curve.Point_Mult(s, self.G, 0)
        tP = self.curve.Point_Mult(t, P, 0)

        R = self.curve.Point_Add_General (sG, tP)
        if USE_JCB:
            rv = (e + R.get_x()) % self.n
        else:
            rv = (e + R.x_) % self.n

        if rv == r:
            print("signature verify Pass")
            return True
        else:
            print("signature verify Fail")
            return False



    ###############################################

    def ECDH (self, self_priv_key, counter_part_PubKey: ECP):
        assert self.curve.ECP_on_curve(counter_part_PubKey) , "Provided Pubkey is not on curve!"
        assert not self_priv_key  > self.n , "Provided private key > curve n!"

        Q = self.curve.Point_Mult(self_priv_key, counter_part_PubKey, 0)
        return Q


    ###############################################


    def NIST_Encryption(self, Msg:str, Pub:ECP ):
        '''not yet done, TBD
        Elliptic Curve Integrated Encryption Scheme (ECIES)
        '''
        assert self.curve.ECP_on_curve(Pub) , "Provided Pubkey is not on curve!"

        M = bytes(Msg, encoding="utf-8")

        Q = self.curve.UINT
        while (Q == self.curve.UINT):
            d  = rand.randint(1, self.n-1 )            # priv key
            Q  = self.curve.Point_Mult(d, self.G, 0) # pub  key

        R  = self.curve.UINT
        while (R == self.curve.UINT):
            k = rand.randint(1, self.n-1 )
            R = self.curve.Point_Mult(k, self.G, 0)
        

        pass

    def NIST_Decryption():
        pass

    def SM2_Encryption(self, M:str, Pb, k_in, ver: str ='c1c3c2', verb: bool = False):
        '''SM2 spec., Part 4, 6.1'''
        assert ver in ('c1c2c3', 'c1c3c2'), f"incorrect output format :{ver}"
        import support
        import hash_lib as hash

        if k_in == None:
            k = rand.randint( 1, self.n-1 )   # A1
        else :
            k = k_in

        M_Byte = M.encode('utf-8')
        
        C1 = self.curve.Point_Mult(k, self.G)   #A2
        C1_hex = C1.hex_str()
        
        Pub = Pb   #A3, h = 1
        kPb = self.curve.Point_Mult(k, Pub)  #A4

        x2 = kPb.hex_str('x', None)
        y2 = kPb.hex_str('y', None)
        Z_kdf  = kPb.hex_str('xy', None)
        klen = len(M_Byte)*8

        t  = support.SM2_KDF(Z_kdf, klen, 'sm3', 'bytes', 'bits')    #A5

        C2 = M_Byte ^ t         #A6
        C2_hex = C2.bytes.hex()

        Z = x2 + M_Byte.hex() + y2 # (x2 ∥ M ∥ y2 )
        Z_bytes =hexstr2byte(Z)
        C3_hex = '{:064x}'.format(hash.hash_256(Z_bytes, 'bytes', 'hex', 'sm3')) #A7
        
        if ver == 'c1c2c3':
            C = C1_hex + C2_hex + C3_hex # C = C1 ∥ C2 ∥ C3     #A8
        else:
            C = C1_hex + C3_hex + C2_hex # C = C1 ∥ C3 ∥ C2     #A8

        if verb:
            log('d', f"Message (bit_length = {klen}) to be encrypted: {M}")
            hex_show('Msg Hex: ', M_Byte.hex())
            log('d', f"given k_rand = 0x%064x" %(k) )
            log('d', "Generated Point C1:" )
            C1.print_point(log_method)
            log('d', "Generated Point kPb:" )
            kPb.print_point(log_method)
            # print(f"x2 ∥ M ∥ y2 hex byte = {Z_bytes}")
            # hex_show(f"x2 ∥ M ∥ y2 hex byte = ", Z_bytes.hex())
            hex_show(f"Z_kdf type {type(Z_kdf)}", Z_kdf)
            hex_show(f"KDF: ", t.bytes.hex())
            hex_show(f"C2 type {type(C2_hex)}: ", C2_hex)
            hex_show(f"x2 ∥ M ∥ y2 hex = ", Z)
            hex_show(f"C1", C1_hex)
            hex_show(f"C2", C2_hex)
            hex_show(f"C3", C3_hex)
            hex_show(f"[Encryption][format: {ver}] final C: ", C)

        return C
   
    def SM2_Decryption(self, C:str, d: int, ver: str ='c1c3c2', verb: bool = False):
        assert ver in ('c1c2c3', 'c1c3c2'), f"incorrect output format :{ver}"
        import support
        from bitstring import Bits
        import hash_lib as hash

        key_byte_len = 256 // 8 # 32bytes
        C_byte_len = len(C) // 2

        assert C_byte_len >= (key_byte_len*3 + 1), f"Given C length = {C_byte_len}"
        klen = (C_byte_len - 3*key_byte_len - 1)*8

        C1_x = C[2 : 2*(key_byte_len)+2]
        C1_y = C[2*key_byte_len+2 : 4*key_byte_len+2]

        if USE_JCB:
            C1 = ECP ((int(C1_x,16), int(C1_y,16), 1), self.p)
        else:
            C1 = ECP ((int(C1_x,16), int(C1_y,16)), self.p)

        if not self.curve.ECP_on_curve(C1):
            assert False, f"recovered C1 point is not on curve"

        S = C1 # h = 1

        if S.is_Unit_Point():
            assert False, f"recovered C1 point is Unit Point"
        
        dC1 = self.curve.Point_Mult(d, C1)

        x2 = dC1.hex_str('x', None)
        y2 = dC1.hex_str('y', None)
        Z_kdf  = dC1.hex_str('xy', None)
        
        t  = support.SM2_KDF(Z_kdf, klen, 'sm3', 'bytes', 'bits')
        if ver == 'c1c2c3':
            C2 = C[4*key_byte_len+2 : 4*key_byte_len+2+klen//4]
            C3 = C[4*key_byte_len+2 + klen//4:]
        else:
            C3 = C[4*key_byte_len+2 : 4*key_byte_len+2+64]  # sm3 hash fixed 256bit/4 = 64 hex
            C2 = C[4*key_byte_len+2+64 :]

        M_ =  int(C2, 16) ^ int(t.hex, 16)
        M_str = hex(M_)[2:]

        Z = x2 + M_str + y2 # (x2 ∥ M ∥ y2 )
        Z_bytes =hexstr2byte(Z)
        
        u = '{:064x}'.format(hash.hash_256(Z_bytes, 'bytes', 'hex', 'sm3')) 


        Decyption = (u == C3)

        if verb or (not Decyption):
            hex_show(f"[Decryption][format:{ver}] input C, C byte_length: {C_byte_len} C bit_length:{C_byte_len*8}, Message bit_len (klen) = {klen}", C)
            hex_show(f"C1", C1_x+C1_y)
            hex_show(f"C2", C2)
            hex_show(f"C3", C3)
            hex_show(f"C1, length = {len(C1_x)}", C1_x)
            hex_show(f"C2, length = {len(C1_y)}", C1_y)
            C1.print_point(log_method)
            log('d', "Generated Point dC1:" )
            dC1.print_point(log_method)
            hex_show(f"t, type {type(t)} ", t.bytes.hex())
            hex_show(f"C2, type {type(C2)} ", C2)
            hex_show(f"M_ type {type(M_str)} ", M_str)
            hex_show(f"u ", u)

            log('d', f"Does u == C3 ? {u == C3}")

        if Decyption:
            M_byte_array = bytearray.fromhex(M_str)
            M_ret = M_byte_array.decode()
            return M_ret
        else:
            return None
    

###########################################################
@timing_log
def Sig_Verify_unit_test(curve_id:int, test_round:int, ):
    ''' signature generate and verify test '''
    from hash_lib import hash_256 as sha256
    log_div('line', 1)
    log('m', f"Signature generate+signature verify test, plan to run {test_round} rounds")
    curve_ins = ECC_Curve(curve_id)

    i = 0
    test_pass = 0
    # msg = "This is a masterpiece from Tiger.Tang"
    # dig = sha256(msg)

    while i < test_round: 
        msg = str(rand.randint(1, curve_ins.n-1 ))
        dig = sha256(msg)

        priv_key = rand.randint(1, curve_ins.n-1 )
        randk    = rand.randint(1, curve_ins.n-1 )

        if curve_id == SM2_CV_ID or curve_id == SM2_TV_ID:
            r,s,z,x,y = curve_ins.SM2_Sig_Gen(priv_key, randk, dig, 'non-compress', False )
            if curve_ins.SM2_Sig_Verify(r,s,z,x,y):
                test_pass+=1
        else:
            r,s,z,x,y = curve_ins.NIST_Sig_Gen(priv_key, randk, dig, 'non-compress', False )
            if curve_ins.NIST_Sig_Verify(r,s,z,x,y):
                test_pass+=1

        # pub_key  = curve_ins.PubKey_Gen(priv_key, verb=False)
        # P = (x,y)
        # if not pub_key.is_equal(ECP(P, curve_ins.p)):
        #     log('w', "Pubkey is different!")
        
        i+=1
    
    log('m', f"Signature generate+signature verify test round %d, %d pass" %(test_round, test_pass))
    log_div('line', 1)

    return test_pass

@timing_log
def ECDH_unit_test(curve_id, test_round):
    ''' ECDH test '''
    log('m', f"ECDH test, plan to run {test_round} rounds")
    curve_ins = ECC_Curve(curve_id)

    i = 0
    test_pass = 0
    while i < test_round:
        # Alice private key and Pubkey
        da = rand.randint(1, curve_ins.n-1 )
        Pa = curve_ins.PubKey_Gen(da, False)

        # Bob private key and Pubkey
        db = rand.randint(1, curve_ins.n-1 )
        Pb = curve_ins.PubKey_Gen(db, False)

        # Alice Pubkey sent to Bob, Bob calculate Share secret
        S_bob = curve_ins.ECDH(db, Pa)

        # Bob Pubkey sent to Alice, Alice calculate Share secret
        S_alice = curve_ins.ECDH(da, Pb)

        if S_bob.is_equal(S_alice):
            test_pass += 1

        i += 1
    
    log('m', f"EDCH test round %d, %d pass" %(test_round, test_pass))
    log_div('line', 1)

    return test_pass
   


####################################################
## ECC unit test
## this website can generate test vector and comapre with our result
## http://www-cs-students.stanford.edu/~tjw/jsbn/ecdh.html
CURVE_LIST = [SECP256K1, SECP256R1, SM2_CV_ID]

@timing_log
def ECC_unit_test (curve_id:int, format = log_method):
    '''unit test for Point_Add Point_Double
       result can be compared with http://www-cs-students.stanford.edu/~tjw/jsbn/ecdh.html
    '''
    assert curve_id in CURVE_LIST, log('e', f"priovided curve_id ={curve_id} is not supported!")
    
    curve_ins = ECC_Curve(curve_id)
    #unit test: Point Double
    log('m', "Point Double unit test: dG = G+G")
    dG = curve_ins.curve.Point_Dbl(curve_ins.G)
    dG.print_point(format)
    log_div('line',1)

    #unit test: Point Add: 
    log('m', "Point Add unit test: tG = dG+G")
    tG = curve_ins.curve.Point_Add(dG, curve_ins.G)
    tG.print_point(format)
    log_div('line',1)

    #unit test: Point Add:
    log('m',"Point Add unit test: Unit(0,0) = tG+tGn")
    tGn = tG.neg_point()
    U = curve_ins.curve.Point_Add(tG, tGn)
    U.print_point(format)
    log_div('line',1)

    #unit test: Point Add General: 
    log('m', "Point Add General unit test 0: dG = G + G")
    dG = curve_ins.curve.Point_Add_General(curve_ins.G, curve_ins.G)
    dG.print_point(format)
    log('m', "Point Add General unit test 1: tG = dG + G")
    tG = curve_ins.curve.Point_Add_General(dG, curve_ins.G)
    tG.print_point(format)
    log('m', "Point Add General unit test 2: tG = tG + Uint")
    tG_plus_I = curve_ins.curve.Point_Add_General(tG, curve_ins.curve.UNIT)
    tG_plus_I.print_point(format)
    log('m', "Point Add General unit test 3: Unit = tG + tGn")
    tGn = tG.neg_point()
    tG_plus_tGn = curve_ins.curve.Point_Add_General(tG, tGn)
    tG_plus_tGn.print_point(format)
    log_div('line',1)

    #unit test: Point Multiply:
    k = 111
    method = 0
    log('m', "Point Mult unit test 0: kG, k = %d, method = %d" %(k, method) )
    kG = curve_ins.curve.Point_Mult(k, curve_ins.G, method)
    kG.print_point(format)

    method = 1
    log('m', "Point Mult unit test 0: kG, k = %d, method = %d" %(k, method) )
    kG = curve_ins.curve.Point_Mult(k, curve_ins.G, method)
    kG.print_point(format)
    log_div('line',1)

    k = rand.randint(1, curve_ins.n-1 )
    log('m', "Point Mult unit test 2: kG, k random ")
    log('d', f"k = 0x%064x" %(k) )
    log('d', f"k = 0d%d" %(k) )
    kG0 = curve_ins.curve.Point_Mult(k, curve_ins.G, 0)
    kG0.print_point(format)

    kG1 = curve_ins.curve.Point_Mult(k, curve_ins.G, 1)
    kG1.print_point(format)
    log_div('line',1)

#####
def Curve_unit_test (curve_id):
    '''do unit test for curve unit test '''
    assert curve_id in CURVE_LIST, log('i', f"priovided curve_id ={curve_id} is not supported!")
    curve_ins = ECC_Curve(curve_id)

    k = rand.randint(1, curve_ins.n-1 )
    log('m', "Pubkey gen unit test:")
    log('d', "PrivKey = 0d%d" %(k) )
    Pubkey = curve_ins.PubKey_Gen(k, True)
    log_div('line', 1)

@timing_log
def Point_Addition_HE_test (curve_id, test_round):
    '''Point Add homomorphic encryption test '''
    assert curve_id in CURVE_LIST, log('i', f"priovided curve_id = {curve_id} is not supported!")
    log('m', f"Point Add homomorphic encryption test, plan to run {test_round} rounds")
    curve_ins = ECC_Curve(curve_id)

    i = 0
    test_pass = 0
    while i < test_round:  

        k1 = rand.randint(curve_ins.n -10, curve_ins.n)
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
            log('e', f"Test round %d of %d fail" %(i, test_round))
            kG_0.print_point(log_method)
            kG_1.print_point(log_method)

        i+=1
    log('m', f"Total test round %d, %d pass" %(test_round, test_pass))
    log_div('line', 1)

    return test_pass
   
def show_signature(msg, r, s, z, Qx, Qy):
    print(msg)
    print("r    :  0x%064x" %(r) )
    print("s    :  0x%064x" %(s) )
    print("hash :  0x%064x" %(z) )
    print("Qx   :  0x%064x" %(Qx) )
    print("Qy   :  0x%064x" %(Qy) )
    print("")

def SM2_TV_Test():
    p = 0x5EF55F07DD5D65CD231C4842324694399E4DADC57F15A21E98CC8BC272C7AE13
    k = 0xB8BAAFCAA92BA3FDAC766683FB7950CEFE0E4A2B4461CA52C1D218E4937EB3D5
    z = 0x5F77158730334C649ACB4013E81E237085DC63EFBAC7A05011F7109FA69C8993

    curve_ins = ECC_Curve(123)
    r,s,z,x,y = curve_ins.SM2_Sig_Gen(p, k, z, 'non-compress', False )
    # P = curve_ins.curve.Point_Mult(p, curve_ins.G, 0)

    # show_signature("",r,s,z,P.x_,P.y_)
    
    # curve_ins.SM2_Sig_Verify(r,s,z,P.x_,P.y_)
    curve_ins.SM2_Sig_Verify(r,s,z,x,y)

@timing_log
def SM2_EN_DE_Test(cid:int, test_rounds: int = 1 , ver = 'c1c3c2', verb: bool = False):
    
    cuv = ECC_Curve(cid)
    if cid == SM2_TV_ID:
        priv = 0x1649AB77A00637BD5E2EFE283FBF353534AA7F7CB89463F208DDBC2920BB0DA0
        k    = 0x4C62EEFD6ECFC2B95B92FD6C3D9575148AFA17425546D49018E5388D49DD7B4F
        log('i', f"this is SM2 encryption+Decryption test by using SM2 test vector, format '{ver}': ")
        M = 'encryption standard'
        Pb = cuv.PubKey_Gen(priv, verb)
        C  = cuv.SM2_Encryption(M, Pb, k, ver, verb)

        if verb: log_div("double",1)

        M_ = cuv.SM2_Decryption(C, priv, ver, verb)

        if verb: log_div("double",1)
        
        log('i', f"Input plain text for encryption: {M}")
        log('i', f"Encrypted result: {C}")
        log('i', f"Decrypted plain text: {M_}")

        if M == M_:
            log('m', "test passed!")
        else:
            log('e', "test failed!")

    elif cid == SM2_CV_ID:
        test_pass = 0
        sm2_n = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
        log('i', f"this is SM2 Encryption+Decryption general test, will run {test_rounds} rounds, format '{ver}': ")
        for i in range(test_rounds):

            m_rnd = rand.randint( 1, pow(2,512) )
            M = hex(m_rnd)[2:]
            #log('i', f"Randomly gen message (byte) length = {len(M)}")
            priv  = rand.randint( 1, sm2_n-1 )

            Pb = cuv.PubKey_Gen(priv, verb)
            C  = cuv.SM2_Encryption(M, Pb, None, ver, verb)
            #log_div("double",1)
            M_ = cuv.SM2_Decryption(C, priv, ver, verb)
            if M == M_:
                test_pass = test_pass + 1
                log('m', f"test round {i+1}/{test_rounds} passed!")
            else:
                log('e', f"test round {i+1}/{test_rounds} failed!")

        log('m', f"total run {test_rounds}, pass {test_pass} rounds")


    

################################################
## main ##
if __name__ == '__main__':
    if len(sys.argv) != 5:
        print(f"usage: python {sys.argv[0]} affine|jacobian iteration(int) timing_measure(bool) verbose(bool)")
        assert False, f"only accept 5 arguments. you input {len(sys.argv)} args!"
    
    assert sys.argv[1] in ['affine','jacobian'], f'need 5 arguments. you input {len(sys.argv)} args!'
    cord_formt = sys.argv[1]

    try:
        iter = int(sys.argv[2])  # Attempt to convert the string to an integer
    except ValueError:
        print(f"Input is not a valid integer string {sys.argv[2]}")

    assert sys.argv[3] in ['true','false'], f'arg3 needs true or false, you input f{sys.argv[3] }!'
    timing_measure = sys.argv[3]
    assert sys.argv[4] in ['true','false'], f'arg4 needs true or false, you input f{sys.argv[3] }!'
    verbose = sys.argv[4]
    
    log('m', "For check deatil, enable LOG_I/LOG_D option in config.py, and compare the result with online tools : http://www-cs-students.stanford.edu/~tjw/jsbn/ecdh.html")

    # from config import USE_JCB
    import config
    config.setup(cord_formt, timing_measure, verbose)

    if cord_formt == 'jacobian':
        from ecp import ECP_JCB as ECP
        log_method = 'jacobian'
        USE_JCB = True
    else:
        from ecp import ECP_AFF as ECP
        log_method = 'affine'
        USE_JCB = False
 
    for cid in CURVE_LIST: # iterate all curves
        # ecc library test
        ECC_unit_test(cid)
        log_div('double', 1)

        # EC Curve test
        Curve_unit_test (cid)
        log_div('double', 1)

        # EC Point_Addition_HE test
        Point_Addition_HE_test(cid, iter)

        # signature gen/ verify test
        Sig_Verify_unit_test(cid, iter)
        log_div('double', 1)

        # ECDH test
        # begin    = timeit.default_timer()
        ECDH_unit_test(cid, iter)
        # duration = timeit.default_timer() - begin
        # log('m', f"total time {duration:.2f} seconds, average {(duration/iter):.2f} seconds per iteration")
        log_div('double', 1)

        SM2_EN_DE_Test(SM2_TV_ID)       # test by using test vector from SM2 spec.
        log_div('double', 1)

        SM2_EN_DE_Test(SM2_CV_ID, iter, 'c1c2c3', False)   # test by using random gen test vectors
        log_div('double', 1)

        SM2_EN_DE_Test(SM2_CV_ID, iter, 'c1c3c2', False)   # test by using random gen test vectors
        log_div('double', 1)

