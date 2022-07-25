import math,string,random
import hashlib

'''
代码可直接运行
'''

#第一步随机生成数据
def data(l):
    List = [''.join(random.sample(string.digits+string.ascii_letters, 5)) for _ in range(0, l)]
    return List

#第二步生成一个Merkel树
def create(data,LEN):
    depth = math.ceil(math.log(LEN, 2)+1)
    #创建一个二维数组
    merkletree = [[]]
    #二维数组倒置
    merkletree[0] = [(hashlib.sha256(i.encode())).hexdigest() for i in data]

    for i in range(1, depth):
        LEN = int(len(merkletree[i-1])/2)
        node=[(hashlib.sha256(merkletree[i-1][2*j].encode() + merkletree[i-1][2*j+1].encode())).hexdigest() for j in range(0, LEN)]
        merkletree.append(node)
        if len(merkletree[i-1])%2 == 1:
            merkletree[i].append(merkletree[i-1][-1])
    return merkletree

#第三步 验证
def verification(m,tree):
    depth = len(tree)
    hash = (hashlib.sha256(m.encode())).hexdigest()
    if hash in tree[0]:
        node = tree[0].index(hash)
    else:
        return "There is no such node in the tree"
    #记录查验路线
    path = []
    for d in range(0,depth):
        if node%2==0:
            if node != len(tree[d]) - 1:
                path.append([tree[d][node], tree[d][node + 1]])
        else:
            path.append([tree[d][node-1], tree[d][node]])
        node = int(node/2)
    path.append([tree[-1][0]])
    if hash != path[0][0] and hash != path[0][1] and path[-1][0] != tree[-1][0]:
        return False
    depth = len(path)
    for i in range(0, depth - 1):
        node = (hashlib.sha256(path[i][0].encode() + path[i][1].encode())).hexdigest()
        if node != path[i + 1][0] and node != path[i + 1][1]:
            return False
    if (hashlib.sha256(path[-2][0].encode() + path[-2][1].encode())).hexdigest() != path[-1][0]:
        return False
    return True


#以下是测试结果：
LEN=100000
#生成数据集合
d=data(LEN)
#生成树
tree=create(d,LEN)
#打印树（结构倒置）
#print(tree)
print(verification(d[random.randint(0,99999)],tree))#测试数据集中的数据
print(verification('1234',tree))#测试不可能存在于数据集中的数据
