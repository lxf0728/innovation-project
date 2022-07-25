from gmssl import sm3, func
import random

'''
代码运行需安装gmssl库
'''

#集合方式实现生成n个数
#成功找到了32位的碰撞，输入数据对如下：
#[b'cea63e735e9a'，b'3d8ef82cf0e4']

def getRandomList(n):
    numbers = []
    while len(numbers) < n:
        i = random.randint(0, 2**48)
        if i not in numbers:
            numbers.append(bytes(str(hex(i)[2:]),encoding='utf-8'))
    return numbers

num1 = getRandomList(100000)
num2 = getRandomList(100000)
OUT1=[]
OUT=[]
OUT_number_1=[]
OUT_number_2=[]
#采用两个循环的方式，对于随机产生的数据集合进行哈希
for i in num1:
    outcome = sm3.sm3_hash(func.bytes_to_list(i))[0:8]#设置了32位的碰撞
    OUT1.append(outcome)
for i in num2:
    outcome = sm3.sm3_hash(func.bytes_to_list(i))[0:8]
    if outcome in OUT1:#判断是否有32位的碰撞
        OUT.append(outcome)
        OUT_number_1.append(num1[OUT1.index(outcome)])
        OUT_number_2.append(i)
#打印出两个数据集合产生碰撞的结果
print(OUT_number_1)
print(OUT_number_2)
