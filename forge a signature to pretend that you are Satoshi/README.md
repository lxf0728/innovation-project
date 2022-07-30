<h1 align="center">forge a signature to pretend that you are Satoshi
</h1>

# 项目原理
<div align=center><img width="438" alt="image" src="https://user-images.githubusercontent.com/109843978/181902903-5a3595a4-6dd9-490f-a8f9-a153d172ebe0.png"></div>



# 代码说明与运行截图

## 代码说明
代码主要是利用了ecdsa验证算法中不对message进行验证的特点，根据课上所讲的过程，对ecdsa进行伪造攻击：

<div align=center>
<table>
<tr>
<th>ecdsa验证函数</th>
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
