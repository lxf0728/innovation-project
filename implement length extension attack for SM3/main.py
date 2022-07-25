#对SM3进行长度扩展攻击
import SM3
'''
main文件可以直接运行
'''
#代码对SM3进行了长度扩展攻击，并对攻击的正确性进行了验证

#扩展函数
def expand(m_list,n):
    B = m_list
    W = ['0' for i in range(68)]
    W_0 = ['0' for i in range(64)]
    for i in range(int(len(B[n])/8)):
        w = B[n][i*8:(i+1)*8]
        W[i] = w
    for j in range(16,68):
        a = SM3.or_16(W[j-16],W[j-9])

        W_j_3 = SM3.Cyc_shift(W[j-3],15)

        a = SM3.or_16(a,W_j_3)

        a = SM3.Replace_P1(a)
        W_j_13=SM3.Cyc_shift(W[j-13],7)
        a = SM3.or_16(a,W_j_13)
        a = SM3.or_16(a,W[j-6])
        W[j]=a
    for j in range(64):
        W_0[j]=SM3.or_16(W[j],W[j+4])
    return W,W_0

#编写生日攻击函数（默认只知道散列值等相关的信息）
def add_attack(h,ADD,LEN):
    #利用已知的LEN创造出正确的m_list
    m_list = SM3.fenzu(ADD)
    l = hex(len(ADD)*4 + LEN)[2:]
    l_len=len(l)
    m_list[-1]=m_list[-1][0:128-l_len]+l
    m_len = len(m_list)
    print(m_list)
    V = ['0' for i in range(m_len + 1)]
    V[0] = h
    for k in range(m_len):
        w = expand(m_list, k)
        W = w[0]
        W_0 = w[1]
        A = V[k][0:8]
        B = V[k][8:16]
        C = V[k][16:24]
        D = V[k][24:32]
        E = V[k][32:40]
        F = V[k][40:48]
        G = V[k][48:56]
        H = V[k][56:64]
        all = ''
        for j in range(64):
            b = a = SM3.Cyc_shift(A, 12)
            T = SM3.T_j(j)
            T = SM3.Cyc_shift(T, j)
            a = SM3.add(a, E)
            a = SM3.add(a, T)
            SS1 = SM3.Cyc_shift(a, 7)
            SS2 = SM3.or_16(SS1, b)
            b = SM3.FF_j(A, B, C, j)
            b = SM3.add(b, D)
            b = SM3.add(b, SS2)
            TT1 = SM3.add(b, W_0[j])  #
            b = SM3.GG_j(E, F, G, j)
            b = SM3.add(b, H)
            b = SM3.add(b, SS1)
            TT2 = SM3.add(b, W[j])  #
            D = C
            C = SM3.Cyc_shift(B, 9)
            B = A
            A = TT1  #
            H = G
            G = SM3.Cyc_shift(F, 19)
            F = E
            E = SM3.Replace_P0(TT2)  #
            all = A + B + C + D + E + F + G + H
        V[k + 1] = SM3.or_16(V[k], all)
    # print(V[-1])
    return V[-1]
#以上帝视角先生成m+padding+ADD的hash,与add_attack对比判断结果是否一样,即可判断出攻击是否成功.

def known(m,ADD):
    after_fill = SM3.filling(m)+ADD
    outcome_know = SM3.hash(after_fill)
    return outcome_know

# 首先初始化原始的消息字
m = '12312'
# 默认设置消息字延长位
ADD = '12345'

#打印结果
#print(add_attack(SM3.hash(m),ADD,512*len(SM3.fenzu(m))))
#print(known(m,ADD))
if known(m,ADD) == add_attack(SM3.hash(m),ADD,512*len(SM3.fenzu(m))) :
   print('Successful implementation of length expansion attack')
else:
   print('Unsuccessful implementation of length expansion attack')
