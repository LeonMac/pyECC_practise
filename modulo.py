''' python version need > 3.5'''
## reverse modular
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

from random import SystemRandom
rand = SystemRandom()   # cryptographic random byte generator

def mod_inv_unittest (iteration):
    # import helper as hlp
    x = rand.randint(1, (1<<256)-1 )
    m = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
    import log as hlp
    iter = 0
    pass_test = 0
    while iter < iteration:
        mod0 = modular_inverse (x, m)
        mod1 = modular_exp_inv (x, m)
        if (mod0 != mod1):

            print(hlp.txtcol.RED + "iteration #", iter, "fail: " + hlp.txtcol.RST)
            print("x   : 0x%064x" %(x) )
            print("m   : 0x%064x" %(m) )
            print("mod0: 0x%064x" %(mod0) )
            print("mod1: 0x%064x" %(mod1) )  

            print("  " )
        else: pass_test += 1
        iter += 1

    return pass_test

if __name__ == '__main__':
# unit test: modular inverse 
    iter = 100
    ret = mod_inv_unittest(iter)
    print ("modular inv unit test: total %d iteration, pass %d " %(iter, ret) )
