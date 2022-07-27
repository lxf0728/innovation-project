<h1 align="center">birthday attack of reduced SM3</h1>

# 项目原理

![image-20220727092720638](C:\Users\GL\AppData\Roaming\Typora\typora-user-images\image-20220727092720638.png)



# 代码说明与运行截图

## 代码说明

生成指定数量随机数的列表：![image-20220727092925530](C:\Users\GL\AppData\Roaming\Typora\typora-user-images\image-20220727092925530.png)

生成两个随机数列表，然后对第一个列表的元素进行sm3哈希，然后对第二个进行哈希时，判断散列值是否在第一个散列值列表中出现，如果有就找了碰撞:![image-20220727093246811](C:\Users\GL\AppData\Roaming\Typora\typora-user-images\image-20220727093246811.png)

## 运行截图

设置了**32位**碰撞以后，运行代码，找到了**32位**的碰撞，碰撞的输入对是如下图：

![image-20220727094505027](C:\Users\GL\AppData\Roaming\Typora\typora-user-images\image-20220727094505027.png)

## 测试结果：

以上图第一对作为测试对象：

![image-20220727094814273](C:\Users\GL\AppData\Roaming\Typora\typora-user-images\image-20220727094814273.png)

测试结果(输出结果为16进制)：![image-20220727094827464](C:\Users\GL\AppData\Roaming\Typora\typora-user-images\image-20220727094827464.png)

可以看到前32位是一样的



# 运行指导

下载gmssl库，代码可直接运行.

![image-20220727095224670](C:\Users\GL\AppData\Roaming\Typora\typora-user-images\image-20220727095224670.png)





