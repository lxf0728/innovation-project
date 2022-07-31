<h1 align="center">Implement a PGP scheme with SM2</h1>

# 项目原理
<div align=center><img width="478" alt="image" src="https://user-images.githubusercontent.com/109843978/182007692-11704fc7-1824-4dd2-8162-31e7f6d266e2.png"></div>




# 代码说明与运行截图

## 代码说明
在该项目的实现中，主要包括以下几个环节：
1、生成公私钥对 
2、生成会话密钥
3、用sm2公钥加密DES密钥
4、加密消息(DES算法)
5、用sm2私钥解密DES密钥
6、解密消息(DES算法)
<div align=center>
<table>
<tr>
<th>DES算法</th>
<td>
<pre>
<code>
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
</code>
</pre>
</td>
</tr>
</table>
</div>

<div align=center>
<table>
<tr>
<th>PGP加密端</th>
<td>
<pre>
<code>
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
</code>
</pre>
</td>
</tr>
</table>
</div>

<div align=center>
<table>
<tr>
<th>PGP解密端</th>
<td>
<pre>
<code>
def PGP_decrypt(enc_m_des,enc_K_sm2):
    sm2_crypt = sm2.CryptSM2(public_key=pub_key_sm2, private_key=pri_key_sm2)
    #解密出密钥
    K = sm2_crypt.decrypt(enc_K_sm2)
    #解密加密的消息
    m = des_descrypt(enc_m_des)
    print('解密出的密钥',K)
    print('解密出的消息', m)
</code>
</pre>
</td>
</tr>
</table>
</div>

## 运行截图

测试代码：<div align=center><img width="386" alt="image" src="https://user-images.githubusercontent.com/109843978/182007817-8b83fad9-e116-462d-b682-8cd7afba1ec8.png"></div>
运行结果：<div align=center><img width="813" alt="image" src="https://user-images.githubusercontent.com/109843978/182007825-934f7c12-8791-4cc4-9d8a-08f296eb3899.png"></div>



# 运行指导

安装gmssl库，且main.py与pyDes.py同源下,代码可直接运行.
