from gmssl import sm3, func
import random


'''
代码运行需安装gmssl库
'''


#成功找到了40位的碰撞,数据对如下：
#b'2aed0f8289',b'e7ab762d2f'
x_0 = str(random.randint(0, 2**41-1))#l+1
n=10
x_0 = bytes(x_0, encoding='utf-8')
x_1 = sm3.sm3_hash(func.bytes_to_list(x_0))
x_2 = bytes(x_1[0:n], encoding='utf-8')
x_2 = sm3.sm3_hash(func.bytes_to_list(x_2))
i=0

while x_1[0:n] != x_2[0:n]:#寻找32位的碰撞
        x_1 = bytes(x_1[0:n], encoding='utf-8')
        x_2 = bytes(x_2[0:n], encoding='utf-8')
        x_1 = sm3.sm3_hash(func.bytes_to_list(x_1))
        x_2 = sm3.sm3_hash(func.bytes_to_list(x_2))
        x_2 = bytes(x_2[0:n], encoding='utf-8')
        x_2 = sm3.sm3_hash(func.bytes_to_list(x_2))
        i+=1

print(i)

x_2=x_1
x_1 = x_0
x_2 = bytes(x_2[0:n], encoding='utf-8')

for j in range(i):
    if sm3.sm3_hash(func.bytes_to_list(x_1))[0:n] == sm3.sm3_hash(func.bytes_to_list(x_2))[0:n]:
        print(x_1,x_2,sm3.sm3_hash(func.bytes_to_list(x_2))[:n])
        break
    else:
        x_1 = sm3.sm3_hash(func.bytes_to_list(x_1))
        x_1 = bytes(x_1[0:n], encoding='utf-8')
        x_2 = sm3.sm3_hash(func.bytes_to_list(x_2))
        x_2 = bytes(x_2[0:n], encoding='utf-8')
