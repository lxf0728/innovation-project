#Project: forge a signature to pretend that you are Satoshi
import math
from hashlib import sha256
import random

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

#ecdsa签名过程
def sign(a,b,p,G,n,h,da,k):
    R = nG(G[0],G[1],11,a,p)
    r = R[0] % n
    s = (inverse(11,n)*(h+da*r))%n
    return (r,s)

#ecdsa验证函数(不验证message,因此有安全缺陷)
def verify(a,p,r,s,n,h,K,G):
    s_1 = inverse(s,n)
    u1 = (s_1*h)%n
    u2 = (s_1*r)%n
    n1 = nG(G[0],G[1],u1,a,p)
    n2 = nG(K[0],K[1],u2,a,p)
    n1_n2 = G_(n1[0],n1[1],n2[0],n2[1],a,p)
    if  n1_n2[0]%n==r:
        #'验证成功'
        return True
    else:
        #'验证失败'
        return False

#伪造攻击
def forge_attack(n,K,G,a,p):
    #这里是去伪造一个签名
    u = random.randint(1,n-1)
    v = random.randint(1,n-1)
    r_ = G_(nG(G[0],G[1],u,a,p)[0],nG(G[0],G[1],u,a,p)[1],nG(K[0],K[1],v,a,p)[0],nG(K[0],K[1],v,a,p)[1],a,p)[0]
    e = (r_*u*inverse(v,n))%n
    s = (r_*inverse(v,n))%n
    if verify(a,p,r_%n,s,n,e,K,G) == True:
        print('Successfully forged')
        print('伪造的签名和明文为',(r_,s),e)
    else:
        print('Unsuccessfully forged')

'''测试代码'''
#string = input('请输入一个字符串作为要加密的明文')
#h = hash(string)
h = hash("山东大学sdu")
#print('hash:', h)
# 设置初始参数
G = (2, 6)
a, b, p = 4, 20, 29
n = 37
#d = input('请输入一个数字作为私钥(可以以5、7、8作为例子)')
d=7
# 随机生成k
k = random.randint(1, n - 1)
r, s = sign(a, b, p, G, n, 88, 7, k)[0], sign(a, b, p, G, n, 88, 7, k)[1]
K=nG(G[0],G[1],7,a,p)
#根据测试数据，测试不验证message的验证函数是否正确运行
#print(verify(a,p,r,s,n,88,K,G))
#运行伪造攻击函数
forge_attack(n,K,G,a,p)
