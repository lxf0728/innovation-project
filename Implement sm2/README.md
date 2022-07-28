<h1 align="center">Implement sm2</h1>

# 代码说明与运行截图

## 代码说明
<div align=center>
<table>
<tr>
<th>点加函数</th>
<td>
<pre>
<code>
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
</code>
</pre>
</td>
</tr>
</table>
</div>
<div align=center>
<table>
<tr>
<th>倍点函数</th>
<td>
<pre>
<code>
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
</code>
</pre>
</td>
</tr>
</table>
</div>

<div align=center>
<table>
<tr>
<th>验签函数</th>
<td>
<pre>
<code>
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
</code>
</pre>
</td>
</tr>
</table>
</div>

<div align=center>
<table>
<tr>
<th>签名函数</th>
<td>
<pre>
<code>
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
</code>
</pre>
</td>
</tr>
</table>
</div>

<div align=center>
<table>
<tr>
<th>加密函数</th>
<td>
<pre>
<code>
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
</code>
</pre>
</td>
</tr>
</table>
</div>

<div align=center>
<table>
<tr>
<th>解密函数</th>
<td>
<pre>
<code>
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
</code>
</pre>
</td>
</tr>
</table>
</div>


## 测试代码与结果
测试代码的签名算法和加解密算法是否能正常运行，测试代码如下：
<div align=center><img width="213" alt="image" src="https://user-images.githubusercontent.com/109843978/181413051-d7c203ea-55b5-4287-8f52-59b8f94a1751.png"></div>
测试结果:
<div align=center><img width="900" alt="image" src="https://user-images.githubusercontent.com/109843978/181413135-65c84693-6ac7-48bb-bb51-f96fe691066b.png"></div>


# 运行指导

SM2.py与SM3.py在一个文件夹中，代码可直接运行.








