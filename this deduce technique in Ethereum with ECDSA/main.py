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

def pk_attack(G,x,y,a,p,n,h):
    r_1 = inverse(r, n)
    x_2 = nG(G[0], G[1], (-(h * r_1)) % n, a, p)
    x_1 = nG(x, y, (s * r_1) % n, a, p)
    return G_(x_1[0],x_1[1],x_2[0],x_2[1],a,p)


'''测试代码'''
string = input('请输入一个字符串作为要加密的明文')
h=hash(string)
print('hash:',h)
#设置初始参数
G=(2,6)
a,b,p=4,20,29
n=37
d=input('请输入一个数字作为私钥(可以以5、7、8作为例子)')
#随机生成k
k = random.randint(1,n-1)
r,s = sign(a,b,p,G,n,h,int(d),k)[0],sign(a,b,p,G,n,h,int(d),k)[1]
#print(nG(G[0],G[1],int(d),a,p))
#print(pk_attack(G,16,2,a,p,n,h))
#判断攻击是否成功
if nG(G[0],G[1],int(d),a,p)==pk_attack(G,16,2,a,p,n,h):
    print('attack successfully')
    print('pk=',pk_attack(G,16,2,a,p,n,h))
else:
    print('attack unsuccessfully')