#零知识证明————验证六级成绩通过
#证明用到了Schnorr协议,使用该协议的前提是假设六级通过以后会第三方发送给成绩拥有者一个特殊令牌表示成绩
#下面就使用零知识证明的方法，假设A为成绩拥有者,使A在使B不知道令牌的情况下,向B证明自己拥有令牌
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

#这里定义两个函数A和B，来表示非交互式的证明过程
def A(G,x):
    #r = random.randint(1,50)
    r=11
    R = nG(G[0],G[1],r,4,29)
    X = nG(G[0],G[1],x,4,29)
    e = hash(str(R[0])+str(R[1]))%10
    s = r+e*x
    return (s,X,R)

def B(s,X,R,G):
    e = hash(str(R[0])+str(R[1]))%10
    sG = nG(G[0],G[1],s,4,29)
    eX = nG(X[0],X[1],e,4,29)
    R_eX = G_(eX[0],eX[1],R[0],R[1],4,29)
    print('sG',sG)
    print('R_eX',R_eX)
    if sG==R_eX:
        print('成功验证')
        return True
    else:
        return False

#设定G点
G=(2,6)
#x即为前提设定假定拥有的证明字
x=7
#A计算需要发送给B的值
s,X,R=A(G,x)[0],A(G,x)[1],A(G,x)[2]
#打印是否完成验证
print(B(s,X,R,G))
