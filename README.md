# pyECC_practise
An ECC crypto library based upon python native library.

## install pre-require
```
pip install -r requirements.txt
``` 

## What are implemented

### low level (common)
- EC Point class (in ecp.py, including affine coordinate and jacobian coordinate)
- EC Curve class and Point Operation on curve

### ECC application standard
- NIST: secp256k1/secp256r1
- SM: sm2

## Application demo:
- Signature gen/verify (NIST and SM)
- EDCH (NIST and SM)
- Message encryption/decryption (SM so far)

## How to run full unit tests
```shell
cd path_of_project
# usage: python pyECC.py affine|jacobian iteration(int) timing_measure(true/false) verbose(true|false)
# example:
python pyECC.py affine 1 false true

```

## config
find the config parameters in config.py

### switch-over between affine coordinate and jacobian coordinate
```shell
USE_JCB = True   # jacobian coordinate
USE_JCB = False  # affine coordinate
```
### enable/disable the timing test
```shell
TIMING_MEASURE = True  # enable(True)/disable(False) timing test
```
---

# Aplication level test
goto subfolder app
```shell
cd app
```
## SM2 encryption / decryption test

### step0: keypair generating: 

```shell
$ python sm2_app.py kg c1c3c2
[WARN]: This is the UNIT Point!
[INFO]: EC Curve: sm2 init done
Your priv key (never disclose it to anybody): 0x877694242664addd858218bc02a631726e6b5cc1d878806ca4a22fe0df1b7f5e
Your pub key:
[DEBG]: Point.x(affine): 0x9422d67f6a13fd62e1adf22207b3a99f5e6051d1c2d981b32f7d0de7672a1b18
[DEBG]: Point.y(affine): 0xebfe7dc7df13845fd9dfbb86c6ed8c72d0ff9d95f9c2bcb383958ecdfc89a54d
```

### step1: message encryption: 
```shell
$ python sm2_app.py en c1c3c2
[WARN]: This is the UNIT Point!
[INFO]: EC Curve: sm2 init done
please input the receiver's public key x (hex with '0x' prefix): 0x9422d67f6a13fd62e1adf22207b3a99f5e6051d1c2d981b32f7d0de7672a1b18
please input the receiver's public key y (hex with '0x' prefix): 0xebfe7dc7df13845fd9dfbb86c6ed8c72d0ff9d95f9c2bcb383958ecdfc89a54d

please input the message you want to encrypted by using sm2:我是一只小鸭子，咿呀咿呀哟!
Your encrypted message (hex): 0454ce1d8a874de01a102b843d8fb0c2c20df57976bfa8dacd809c5aa3354672f9c1e3ba0c7b823c7d24c228d471a193fb109fdd1d214bbd017c7991c6c3a336ba052b4aa60f4f465e5843cae7da7c1e30e0b2bd12057c6a32de454c13f5edcec2f798945112b7b99d2bb0cc299fb8dd6d32a3dc480aee9b4723a36a3d5f38aa4ba35b2e4dafa7c98f
```

### step2: message decryption: 
```shell
$ python sm2_app.py de c1c3c2
[WARN]: This is the UNIT Point!
[INFO]: EC Curve: sm2 init done
please paste the encrypted message you want to do decryption here (hex):  0454ce1d8a874de01a102b843d8fb0c2c20df57976bfa8dacd809c5aa3354672f9c1e3ba0c7b823c7d24c228d471a193fb109fdd1d214bbd017c7991c6c3a336ba052b4aa60f4f465e5843cae7da7c1e30e0b2bd12057c6a32de454c13f5edcec2f798945112b7b99d2bb0cc299fb8dd6d32a3dc480aee9b4723a36a3d5f38aa4ba35b2e4dafa7c98f
please input the your priv key (hex with '0x' prefix): 0x877694242664addd858218bc02a631726e6b5cc1d878806ca4a22fe0df1b7f5e
Your decrypted message: 我是一只小鸭子，咿呀咿呀哟!
```

## a ZKP demo based on ECC
```shell
$ python zkp.py 
Prover Honest test--> 10 rounds: 
total 10 rounds test, zkp dis-honest count = 0, Prover dishonest probability = 0
Prover DisHonest test--> 10 rounds: 
total 10 rounds test, zkp dis-honest count = 4, Prover dishonest probability = 0.9375
Prover Honest test--> 10 rounds: honest count = 10
Prover DisHonest test--> 10 rounds: honest count = 0
```

