import math
from hashlib import sha256
import random
import base64
from gmssl import sm3,func
from gmssl import sm2
from pyDes import des, CBC, PAD_PKCS5
import binascii

pub_key_sm2 = 'B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'
pri_key_sm2 = '00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5'
KEY = 'mHAxsLYz'

def des_encrypt(s):
    secret_key = KEY
    iv = secret_key
    k = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
    en = k.encrypt(s, padmode=PAD_PKCS5)
    return binascii.b2a_hex(en)


def des_descrypt(s):
    secret_key = KEY
    iv = secret_key
    k = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
    de = k.decrypt(binascii.a2b_hex(s), padmode=PAD_PKCS5)
    return de

#hash
def hash(string):
    return int(sha256(string.encode()).hexdigest(), 16)

#取模逆
def inverse(value, p):
    for i in range(1, p):
        if (i * value) % p == 1:
            return i
    return -1

# 计算椭圆曲线下两点相加
def G_(x1, y1, x2, y2, a, p):
    flag = 1  # 控制符号位
    if x1 == x2 and y1 == y2:
        num_under = 3 * (x1 ** 2) + a  # 计算分子
        num = 2 * y1  # 计算分母
    else:
        num_under = y2 - y1
        num = x2 - x1
        if num_under * num < 0:
            flag = 0
            num_under = abs(num_under)
            num = abs(num)
    gcd_value = math.gcd(num_under, num)
    num_under = num_under // gcd_value
    num = num // gcd_value
    inverse_value = inverse(num, p)
    k = (num_under * inverse_value)
    if flag == 0:
        k = -k
    k = k % p
    # 计算x3,y3
    x3 = (k ** 2 - x1 - x2) % p
    y3 = (k * (x1 - x3) - y1) % p
    return [x3, y3]

#计算倍元
def nG(x0, y0, n, a, p):
    x1 = x0
    y1 = y0
    for i in range(n-1):
        outcome = G_(x1,y1, x0, y0, a, p)
        x1 = outcome[0]
        y1 = outcome[1]
    return outcome

#pgp的加密端
def PGP_encrypt(m,K):
    #使用DES算法对消息进行加密
    enc_m_des = des_encrypt(m)
    #使用sm2对密钥进行加密
    sm2_crypt = sm2.CryptSM2(public_key=pub_key_sm2, private_key=pri_key_sm2)
    K = str.encode(K)
    enc_K_sm2 = sm2_crypt.encrypt(K)
    print('enc_m',enc_m_des)
    print('enc_K',enc_K_sm2)
    return (enc_m_des,enc_K_sm2)

#PGP解密函数
def PGP_decrypt(enc_m_des,enc_K_sm2):
    sm2_crypt = sm2.CryptSM2(public_key=pub_key_sm2, private_key=pri_key_sm2)
    #解密出密钥
    K = sm2_crypt.decrypt(enc_K_sm2)
    #解密加密的消息
    m = des_descrypt(enc_m_des)
    print('解密出的密钥',K)
    print('解密出的消息', m)

'''测试代码'''
# DES默认秘钥

#m=input('请输入一个消息字符串（注意不要输入汉字）')
m='project_sdu'#默认消息字

a,b=PGP_encrypt(m,KEY)[0],PGP_encrypt(m,KEY)[1]

PGP_decrypt(a,b)