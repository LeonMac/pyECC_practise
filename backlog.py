# https://crypto.stanford.edu/pbc/notes/ep/
# Generating Random Points

# https://cr.yp.to/antiforgery.html#sqroot

#################################################
# for some history debug code
# def SM2_encryption():
    # 待加密的消息M ：encryption standard
    # 消息M 的16进制表示：656E63 72797074 696F6E20 7374616E 64617264
    # 私钥d B ：
    # 1649AB77 A00637BD 5E2EFE28 3FBF3535 34AA7F7C B89463F2 08DDBC29 20BB0DA0
    # 公钥P B =(x B ,y B )：
    # 坐标xB ：
    # 435B39CC A8F3B508 C1488AFC 67BE491A 0F7BA07E 581A0E48 49A5CF70 628A7E0A
    # 坐标yB ：
    # 75DDBA78 F15FEECB 4C7895E2 C1CDF5FE 01DEBB2C DBADF453 99CCF77B BA076A42

    # 加密各步骤中的有关值：
    # 产生随机数k：
    # 4C62EEFD 6ECFC2B9 5B92FD6C 3D957514 8AFA1742 5546D490 18E5388D 49DD7B4F
    # 计算椭圆曲线点C1 =[k]G=(x1 ,y1 )：
    # 坐标x1 ：
    # 245C26FB 68B1DDDD B12C4B6B F9F2B6D5 FE60A383 B0D18D1C 4144ABF1 7F6252E7
    # 坐标y1 ：
    # 76CB9264 C2A7E88E 52B19903 FDC47378 F605E368 11F5C074 23A24B84 400F01B8

    # 在 此C1 选 用 未 压 缩 的 表 示 形 式， 点 转 换 成 字 节 串 的 形 式 为P C∥x 1 ∥y 1 ， 其 中P C为 单 一 字 节
    # 且P C=04，仍记为C 1 。
    # 计算椭圆曲线点[k]P B =(x 2 ,y 2 )：
    # 坐标x 2 ：
    # 64D20D27 D0632957 F8028C1E 024F6B02 EDF23102 A566C932 AE8BD613 A8E865FE
    # 坐标y 2 ：
    # 58D225EC A784AE30 0A81A2D4 8281A828 E1CEDF11 C4219099 84026537 5077BF78
    # 消息M 的比特长度klen=152
    # 计算t=KDF (x 2 ∥y 2 , klen)：
    # 006E30 DAE231B0 71DFAD8A A379E902 64491603

    # 计算C2 =M ⊕t：
    # 650053 A89B41C4 18B0C3AA D00D886C 00286467

    # 计算C3 =Hash(x 2 ∥ M ∥ y 2 )：
    # x 2 ∥ M ∥ y 2 ：
    # 64d20d27 d0632957 f8028c1e 024f6b02 edf23102 a566c932 ae8bd613 a8e865fe
    # 64D20D27 D0632957 F8028C1E 024F6B02 EDF23102 A566C932 AE8BD613 A8E865FE
    # 656e6372 79707469 6f6e2073 74616e64 61726458 d225eca7 84ae300a 81a2d482 81a828e1cedf11c4219099840265375077bf78
    # 656E6372 79707469 6F6E2073 74616E64 61726458 D225ECA7 84AE300A 81A2D482
    # 81A828E1 CEDF11C4 21909984 02653750 77BF78
    # C3 ：
    # 9C3D7360 C30156FA B7C80A02 76712DA9 D8094A63 4B766D3A 285E0748 0653426D
    # 输出密文C = C 1 ∥C 2 ∥C 3 ：

    # 04245C26 FB68B1DD DDB12C4B 6BF9F2B6 D5FE60A3 83B0D18D 1C4144AB F17F6252
    # E776CB92 64C2A7E8 8E52B199 03FDC473 78F605E3 6811F5C0 7423A24B 84400F01
    # B8650053 A89B41C4 18B0C3AA D00D886C 00286467 9C3D7360 C30156FA B7C80A02
    # 76712DA9 D8094A63 4B766D3A 285E0748 0653426D
    #cid = SM2_TV_ID

    # M_Byte = M.encode()
    # # M_Byte = bytes.fromhex (M.encode())
    # print(f"M_Byte= {M_Byte}, hex format : {M_Byte.hex()}")

    # Pub  = cuv.PubKey_Gen(priv, True)
    # k  = 0x4C62EEFD6ECFC2B95B92FD6C3D9575148AFA17425546D49018E5388D49DD7B4F
    # C1 = cuv.curve.Point_Mult(k, cuv.G)
    # log('d', f"given k_rand = 0x%064x" %(k) )
    # log('d', "Generated Point C1:" )
    # C1.print_point('hex')

    # kPb = cuv.curve.Point_Mult(k, Pub)
    # log('d', "Generated Point kPb:" )
    # kPb.print_point('hex')

    # x2 = kPb.hex_str('x', None)
    # y2 = kPb.hex_str('y', None)
    # Z_kdf  = kPb.hex_str('xy', None)

    # klen = len(M_Byte)*8
    # print(f"Z = {Z_kdf}", {type(Z_kdf)})
    # import support
    # t  = support.SM2_KDF(Z_kdf, klen, 'sm3', 'bytes', 'bits')
    # log('d', f"klen = {klen}")
    # log('d', f"t = {t}")

    # C2 = M_Byte ^ t
    # log('d', f"C2 = {C2}, {type(C2)}")


    # import hash_lib as hash
    # Z = x2 + M_Byte.hex() + y2 # (x2 ∥ M ∥ y2 )
    # print(f"x2 ∥ M ∥ y2 hex = {Z}")
    # Z_bytes = bytes.fromhex(Z)
    # print(f"x2 ∥ M ∥ y2 hex byte = {Z_bytes}")

    # # C3 =Hash(x2 ∥ M ∥ y2 )

    # C1_hex = C1.hex_str()
    # print(f"C1_hex = {C1_hex}, type: {type(C1_hex)} ")

    # C2_hex = C2.bytes.hex()
    # log('d', f"C2_hex = {C2_hex}, {type(C2_hex)}")
    
    # C3_hex = hex(hash.hash_256(Z_bytes, 'bytes', 'hex', 'sm3'))[2:]
    # log('d', f"C3_hex = {C3_hex}")

    # C = C1_hex + C2_hex + C3_hex # C = C1 ∥ C2 ∥ C3
    # # log('d', f"final C = {C}")
    # hex_show('Final C:', C, 8)