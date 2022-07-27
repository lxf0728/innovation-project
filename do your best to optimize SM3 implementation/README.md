<h1 align="center">the Rho method of reduced SM3</h1>

# 项目原理
<div align=center><img width="620" alt="image" src="https://user-images.githubusercontent.com/109843978/181232230-a58123f7-8703-484d-ad31-ad9a3d652105.png"></div>

# 代码说明与运行截图
为了使代码的执行速度更快，代码没有引用库函数，通过自行编写一个函数进制转化函数等来提高运行速度,并融合减少一些重复的步骤，并且融合了消息填充和消息扩展以加快散列值的运算.
## 代码说明

<div align=center>
<table>
<tr>
<th>相关辅助函数</th>
<td>
<pre>
<code>
def out_hex(list1):
    for i in list1:
        print("%08x" % i)
    print("\n")

#左移
def rotate_left(a, k):
    k = k % 32
    return ((a << k) & 0xFFFFFFFF) | ((a & 0xFFFFFFFF) >> (32 - k))

#初始化
T_j = []
for i in range(0, 16):
    T_j.append(0)
    T_j[i] = 0x79cc4519
for i in range(16, 64):
    T_j.append(0)
    T_j[i] = 0x7a879d8a

#布尔函数
def FF_j(X, Y, Z, j):
    if 0 <= j and j < 16:
        ret = X ^ Y ^ Z
    elif 16 <= j and j < 64:
        ret = (X & Y) | (X & Z) | (Y & Z)
    return ret

#布尔函数
def GG_j(X, Y, Z, j):
    if 0 <= j and j < 16:
        ret = X ^ Y ^ Z
    elif 16 <= j and j < 64:
        ret = (X & Y) | ((~ X) & Z)
    return ret

def P_0(X):
    return X ^ (rotate_left(X, 9)) ^ (rotate_left(X, 17))

def P_1(X):
    return X ^ (rotate_left(X, 15)) ^ (rotate_left(X, 23))

</code>
</pre>
</td>
</tr>
</table>
</div>


## 运行截图
<div align=center><img width="415" alt="image" src="https://user-images.githubusercontent.com/109843978/181228518-fe9e6956-b8f6-4df2-8396-9ff5b2f3608c.png"></div>


# 运行指导












