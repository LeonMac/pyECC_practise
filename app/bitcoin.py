class BitCoin():
    '''Bitcoin Address Generator
       This is only for study but NOT for production
    '''
    def __init__(self):
        self.sk1 = E.ECC_Curve(E.SECP256K1)

    def KeyPair_Gen(self, priv_key = None ):
        priv = priv_key if priv_key != None else rand.randint( 1, self.sk1.n-1 ) 

        Pb   = self.sk1.PubKey_Gen(priv, False)

        print('Your priv key (never disclose it to anybody):', "0x{:064x}".format(priv))
        print('Your pub key:')
        Pb.print_point('hex')