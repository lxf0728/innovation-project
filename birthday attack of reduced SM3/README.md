<h1 align="center">birthday attack of reduced SM3</h1>

# 项目原理
<div align=center><img width="574" alt="image" src="https://user-images.githubusercontent.com/109843978/181145558-430857d8-3140-413e-b835-17f514dbf363.png"></div>




# 代码说明与运行截图

## 代码说明

生成指定数量随机数的列表：<div align=center><img width="599" alt="image" src="https://user-images.githubusercontent.com/109843978/181145647-540022ed-65a0-4352-b325-d31d1aa56e12.png"></div>


生成两个随机数列表，然后对第一个列表的元素进行sm3哈希，然后对第二个进行哈希时，判断散列值是否在第一个散列值列表中出现，如果有就找了碰撞:<div align=center><img width="429" alt="image" src="https://user-images.githubusercontent.com/109843978/181145729-f7ea3bcf-466e-42b6-8e14-4f46988b9b10.png"></div>


## 运行截图

设置了**32位**碰撞以后，运行代码，找到了**32位**的碰撞，碰撞的输入对是如下图：

<div align=center><img width="524" alt="image" src="https://user-images.githubusercontent.com/109843978/181146409-52c82ef5-a5f8-49e8-9c36-35288a9bec35.png"></div>

## 测试结果：

以上图第一对作为测试对象：

<div align=center><img width="515" alt="image" src="https://user-images.githubusercontent.com/109843978/181146488-eaa1afcc-0d45-46f5-bcc8-0abe65bde312.png">
</div>

测试结果(输出结果为16进制)：
<div align=center><img width="588" alt="image" src="https://user-images.githubusercontent.com/109843978/181146535-cf0d0a21-486a-4433-891a-85ef6da780ca.png">
</div>

可以看到前32位是一样的



# 运行指导

下载gmssl库，代码可直接运行，运行时间可能较慢需要等待一段时间.







