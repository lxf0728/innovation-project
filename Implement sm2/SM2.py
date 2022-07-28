from random import choice
from  math import ceil
import SM3

# 初始化椭圆曲线的参数
N=SM3.INT_16('FFFFFFFeFFFFFFFFFFFFFFFFFFFFFFFF7203dF6B21C6052B53BBF40939d54123')
p = SM3.INT_16('FFFFFFFeFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF')
G = '32c4ae2c1f1981195f9904466a39c9948fe30bbff2660be1715a4589334c74c7bc3736a2f4f6779c59bdcee36b692153d0a9877cc62a474002df32e52139f0a0'  # G点
a = SM3.INT_16('FFFFFFFeFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC')
b = SM3.INT_16('28e9Fa9e9d9F5e344d5a9e4BCF6509a7F39789F515aB8F92ddBCBd414d940e93')
a_3 = (a + 3) % p
Fp = 256
# kp运算
def kp(k, point,len_para):  
    point = '%s%s' % (point, '1')
    mask_str = '8'
    for i in range(len_para-1):
        mask_str += '0'
    mask = SM3.INT_16(mask_str)
    temp = point
    flag = False
    for n in range(len_para * 4):
        if (flag):
            temp = doublepoint(temp,len_para)
        if (k & mask) != 0:
            if (flag):
                temp = addpoint(temp, point,len_para)
            else:
                flag = True
                temp = point
        k = k << 1
    return convert(temp,len_para)
# 倍点
def doublepoint(point,len_para):  
    l = len(point)
    len_2 = 2 * len_para
    if l< len_para*2:
        return None
    else:
        x1 = SM3.INT_16(point[0:len_para])
        y1 = SM3.INT_16(point[len_para:len_2])
        if l == len_2:
            z1 = 1
        else:
            z1 = SM3.INT_16(point[len_2:])
        T6 = (z1 * z1) % p
        T2 = (y1 * y1) % p
        T3 = (x1 + T6) % p
        T4 = (x1 - T6) % p
        T1 = (T3 * T4) % p
        T3 = (y1 * z1) % p
        T4 = (T2 * 8) % p
        T5 = (x1 * T4) % p
        T1 = (T1 * 3) % p
        T6 = (T6 * T6) % p
        T6 = (a_3 * T6) % p
        T1 = (T1 + T6) % p
        z3 = (T3 + T3) % p
        T3 = (T1 * T1) % p
        T2 = (T2 * T4) % p
        x3 = (T3 - T5) % p

        if (T5 % 2) == 1:
            T4 = (T5 + ((T5 + p) >> 1) - T3) % p
        else:
            T4 = (T5 + (T5 >> 1) - T3) % p

        T1 = (T1 * T4) % p
        y3 = (T1 - T2) % p

        form = '%%0%dx' % len_para
        form = form * 3
        return form % (x3, y3, z3)
# 点加函数
def addpoint(p1, p2,len_para):  
    len_2 = 2 * len_para
    l1 = len(p1)
    l2 = len(p2)
    if (l1 < len_2) or (l2 < len_2):
        return None
    else:
        X1 =SM3.INT_16(p1[0:len_para])
        Y1 = SM3.INT_16(p1[len_para:len_2])
        if (l1 == len_2):
            Z1 = 1
        else:
            Z1 = SM3.INT_16(p1[len_2:])
        x2 = SM3.INT_16(p2[0:len_para])
        y2 = SM3.INT_16(p2[len_para:len_2])

        T1 = (Z1 * Z1) % p
        T2 = (y2 * Z1) % p
        T3 = (x2 * T1) % p
        T1 = (T1 * T2) % p
        T2 = (T3 - X1) % p
        T3 = (T3 + X1) % p
        T4 = (T2 * T2) % p
        T1 = (T1 - Y1) % p
        Z3 = (Z1 * T2) % p
        T2 = (T2 * T4) % p
        T3 = (T3 * T4) % p
        T5 = (T1 * T1) % p
        T4 = (X1 * T4) % p
        X3 = (T5 - T3) % p
        T2 = (Y1 * T2) % p
        T3 = (T4 - X3) % p
        T1 = (T1 * T3) % p
        Y3 = (T1 - T2) % p

        form = '%%0%dx' % len_para
        form = form * 3
        return form % (X3, Y3, Z3)

# 生成仿射坐标
def convert(point,len_para):
    len_2 = 2 * len_para
    x = SM3.INT_16(point[0:len_para])
    y = SM3.INT_16(point[len_para:len_2])
    z = SM3.INT_16(point[len_2:])
    z_inv = pow(z, p - 2, p)
    z_invsquar = (z_inv * z_inv) % p
    z_invQube = (z_invsquar * z_inv) % p
    x_new = (x * z_invsquar) % p
    y_new = (y * z_invQube) % p
    z_new = (z * z_inv) % p
    if z_new == 1:
        form = '%%0%dx' % len_para
        form = form * 2
        return form % (x_new, y_new)
    else:
        print ("point at infinity!!!!!!!!!!!!")
        return None

#密钥派生函数
def kdf(Z,klen):
    klen = int(klen)
    ct = 0x00000001
    rcnt = ceil(klen/32)
    Zin = SM3.hex2byte(Z)
    Ha = ""
    for i in range(rcnt):
        msg = Zin  + SM3.hex2byte('%08x'% ct)
        Ha = Ha + SM3.hash_msg(msg)
        ct += 1
    return Ha[0: klen * 2]

# 验签函数
def verify(sign, e, pa,len_para):
    r = SM3.INT_16(sign[0:len_para])
    s = SM3.INT_16(sign[len_para:2*len_para])
    e = SM3.INT_16(e)
    t = (r + s) % N
    if t == 0:
        return 0

    p1 = kp(s, G,len_para)
    p2 = kp(t, pa,len_para)

    if p1 == p2:
        p1 = '%s%s' % (p1, 1)
        p1 = doublepoint(p1,len_para)
    else:
        p1 = '%s%s' % (p1, 1)
        p1 = addpoint(p1, p2,len_para)
        p1 = convert(p1,len_para)

    x = SM3.INT_16(p1[0:len_para])
    return (r == ((e + x) % N))

 # 签名函数
def sign(e, da, K,len_para,Hexstr = 0):
    if Hexstr:
        e = SM3.INT_16(e)
    else:
        e = e.encode('utf-8')
        e = e.hex()
        e = SM3.INT_16(e)

    d = SM3.INT_16(da)
    k = SM3.INT_16(K)

    p1 = kp(k, G,len_para)

    x = SM3.INT_16(p1[0:len_para])
    R = ((e + x) % N)
    if R == 0 or R + k == N:
        return None
    d_1 = pow(d+1, N - 2, N)
    s = (d_1*(k + R) - R) % N
    if s == 0:
        return None
    else:
        return '%064x%064x' % (R,s)
# 加密函数
def encrypt(M,pa,len_para,Hexstr = 0):
    if Hexstr:
        msg = M
    else:
        msg = M.encode('utf-8')
        msg = msg.hex()
    k = SM3.getstr(len_para)
    C1 = kp(SM3.INT_16(k),G,len_para)
    xy = kp(SM3.INT_16(k),pa,len_para)
    x2 = xy[0:len_para]
    y2 = xy[len_para:2*len_para]
    ml = len(msg)
    t = kdf(xy,ml/2)
    if SM3.INT_16(t)==0:
        return None
    else:
        form = '%%0%dx' % ml
        C2 = form % (SM3.INT_16(msg) ^ SM3.INT_16(t))
        C3 = SM3.Hash_sm3('%s%s%s'% (x2,msg,y2),1)
        return '%s%s%s' % (C1,C3,C2)
# 解密函数
def decrypt(C,da,len_para):
    len_2 = 2 * len_para
    len_3 = len_2 + 64
    C1 = C[0:len_2]
    C3 = C[len_2:len_3]
    C2 = C[len_3:]
    xy = kp(SM3.INT_16(da),C1,len_para)
    x2 = xy[0:len_para]
    y2 = xy[len_para:len_2]
    cl = len(C2)
    t = kdf(xy, cl/2)
    if SM3.INT_16(t) == 0:
        return None
    else:
        form = '%%0%dx' % cl
        M = form % (SM3.INT_16(C2) ^ SM3.INT_16(t))
        u = SM3.Hash_sm3('%s%s%s'% (x2,M,y2),1)
        if  (u == C3):
            return M
        else:
            return None



#测试用例
LEN=64
e = SM3.getstr(LEN)
d = SM3.getstr(LEN)
k = SM3.getstr(LEN)

#验证加密算法
pa = kp(SM3.INT_16(d), G,LEN)
sig = sign(e,d,k,LEN,1)
print(verify(sig,e,pa,LEN))
print(sig)

#验证加解密算法
s = input('请随机输入一个字符串')
print('明文 = %s' % s)
C = encrypt(s,pa,LEN,0)
print('密文 = %s' % C)
m = decrypt(C,d,LEN)
M = bytes.fromhex(m)
print('decrypt outcome',end=" ")
print(M.decode())
