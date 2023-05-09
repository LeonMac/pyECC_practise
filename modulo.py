''' python version need > 3.5'''
# square root modular.
# From https://rosettacode.org/wiki/Tonelli-Shanks_algorithm#Python

def legendre(a, p):
    return pow(a, (p - 1) // 2, p)

def tonelli(n, p):
    '''return r for r^2 % p = 1'''
    assert legendre(n, p) == 1, "not a square (mod p)"
    q = p - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1
    if s == 1:
        return pow(n, (p + 1) // 4, p)
    for z in range(2, p):
        if p - 1 == legendre(z, p):
            break
    c = pow(z, q, p)
    r = pow(n, (q + 1) // 2, p)
    t = pow(n, q, p)
    m = s
    t2 = 0
    while (t - 1) % p != 0:
        t2 = (t * t) % p
        for i in range(1, m):
            if (t2 - 1) % p == 0:
                break
            t2 = (t2 * t2) % p
        b = pow(c, 1 << (m - i - 1), p)
        r = (r * b) % p
        c = (b * b) % p
        t = (t * c) % p
        m = i
    return r

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
    assert a>0 , f"a={a}: The operator value a must be >0 for this appllication"
    g, x = half_extended_gcd(a, m)
    if g != 1:
        raise ValueError
    
    return x % m

def modular_exp_inv(a, m):
	''' compute the multiplicative inverse, by doing python native modulo exponentiation'''
	return pow(a, m-2, m)

from random import SystemRandom
rand = SystemRandom()   # cryptographic random byte generator

def mod_sqrt_unittest (iteration):
    
    m = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
    import log as hlp
    iter = 0
    pass_test = 0
    while iter < iteration:
        x   = rand.randint(1, m -1 )
        x2  = x**2 % m
        r = tonelli(x2, m)

        if (r**2 % m != x2):

            print(hlp.txtcol.RED + "iteration #", iter, "fail: " + hlp.txtcol.RST)
            print("x   : 0x%064x" %(x) )
            print("m   : 0x%064x" %(m) )
            print("x^2 : 0x%064x" %(x2) )
            print("r   : 0x%064x" %(r) )  

            print("  " )
        else: pass_test += 1
        iter += 1

    return pass_test


def mod_inv_unittest (iteration):
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
    ret = mod_inv_unittest (iter)
    print ("modular inv unit test: total %d iteration, pass %d " %(iter, ret) )

    ret = mod_sqrt_unittest (iter)
    print ("modular sqrt unit test: total %d iteration, pass %d " %(iter, ret) )
