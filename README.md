# pyECC_practise
An ECC crypto library based upon python native library.

## What are implemented

### low level (common)
- EC Point class
- EC Curve class and Point Operation on curve

### ECC application standard
- NIST: secp256k1/secp256r1
- SM: sm2

## Application demo:
- Signature gen/verify (NIST and SM)
- EDCH (NIST and SM)
- Message encryption/decryption (SM so far)

## How to run demo
```shell
cd path_of_project
python pyECC.py
```


