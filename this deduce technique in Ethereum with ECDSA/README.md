<h1 align="center">implement pk_attack with ECDSA</h1>

# 项目原理
<div align=center><img width="358" alt="image" src="https://user-images.githubusercontent.com/109843978/181866134-cdb47362-32cd-43eb-b456-bb5538040dd1.png"></div>


# 代码说明与运行截图

## 代码说明
<div align=center>
<table>
<tr>
<th>hash函数</th>
<td>
<pre>
<code>
def hash(string):
    return int(sha256(string.encode()).hexdigest(), 16)
</code>
</pre>
</td>
</tr>
</table>
</div>

<div align=center>
<table>
<tr>
<th>取模逆</th>
<td>
<pre>
<code>
def inverse(value, p):
    for i in range(1, p):
        if (i * value) % p == 1:
            return i
    return -1
</code>
</pre>
</td>
</tr>
</table>
</div>

<div align=center>
<table>
<tr>
<th>点加函数</th>
<td>
<pre>
<code>
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
def nG(x0, y0, n, a, p):
    x1 = x0
    y1 = y0
    for i in range(n-1):
        outcome = G_(x1,y1, x0, y0, a, p)
        x1 = outcome[0]
        y1 = outcome[1]
    return outcome
</code>
</pre>
</td>
</tr>
</table>
</div>

<div align=center>
<table>
<tr>
<th>ecdsa签名</th>
<td>
<pre>
<code>
def sign(a,b,p,G,n,h,da,k):
    R = nG(G[0],G[1],11,a,p)
    r = R[0] % n
    s = (inverse(11,n)*(h+da*r))%n
    return (r,s)
</code>
</pre>
</td>
</tr>
</table>
</div>

<div align=center>
<table>
<tr>
<th>attack函数</th>
<td>
<pre>
<code>
def pk_attack(G,x,y,a,p,n,h):
    r_1 = inverse(r, n)
    x_2 = nG(G[0], G[1], (-(h * r_1)) % n, a, p)
    x_1 = nG(x, y, (s * r_1) % n, a, p)
    return G_(x_1[0],x_1[1],x_2[0],x_2[1],a,p)
</code>
</pre>
</td>
</tr>
</table>
</div>



## 运行截图
测试代码:
<div align=center><img width="446" alt="image" src="https://user-images.githubusercontent.com/109843978/181866380-60a069b9-bf50-41cd-9157-9501982ecfd1.png"></div>

运行结果:
<div align=center><img width="527" alt="image" src="https://user-images.githubusercontent.com/109843978/181866235-e913f703-183a-4147-b58b-6d79ac22e993.png">
</div>
由打印的内容可知，可以完成攻击.

# 运行指导

代码可直接运行.








