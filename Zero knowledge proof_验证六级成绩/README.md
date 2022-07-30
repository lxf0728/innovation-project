<h1 align="center">Zero knowledge proof_验证六级成绩</h1>

# 项目原理
Schnorr协议本质上是一种零知识的技术，即证明方(Prover)声称知道一个密钥x的值，通过使用Schnorr加密技术，可以在不揭露x的值情况下向验证方(Verifier)证明对x的知情权.
<div align=center><img width="591" alt="image" src="https://user-images.githubusercontent.com/109843978/181935635-a0c48d44-aa78-4922-a931-02a77ec94be1.png">
</div>

# 代码说明与运行截图

## 代码说明
代码根据Schnorr协议模拟了证明方A和验证发B的验证过程:

<div align=center>
<table>
<tr>
<th>A</th>
<td>
<pre>
<code>
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
</code>
</pre>
</td>
</tr>
</table>
</div>

<div align=center>
<table>
<tr>
<th>伪造攻击函数</th>
<td>
<pre>
<code>
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
</code>
</pre>
</td>
</tr>
</table>
</div>

## 运行截图

给定默认的原始信息和附加信息，检验攻击是否成功：
<div align=center><img width="456" alt="image" src="https://user-images.githubusercontent.com/109843978/181903198-ad0d5598-f544-4eba-94b6-44279cf061c9.png"></div>
运行结果:
<div align=center><img width="253" alt="image" src="https://user-images.githubusercontent.com/109843978/181903202-304731e5-cb7e-4f66-8c0c-18cb432284d6.png"></div>
由打印的内容可知，可以完成攻击.

# 运行指导
代码可直接运行.

