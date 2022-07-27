<h1 align="center">the Rho method of reduced SM3</h1>

# 项目原理
<div align=center><img width="500" alt="image" src="https://user-images.githubusercontent.com/109843978/181150732-0bde1a2a-5d0c-46af-9091-51a6e393fb80.png"></div>



# 代码说明与运行截图

## 代码说明
文件主要包含两个函数add_attack()和known().
add_attack是指在只知道散列值、原始消息长度的条件下，添加附加信息，产生对应散列值:
<div align=center><img width="289" alt="image" src="https://user-images.githubusercontent.com/109843978/181151629-353742d1-26c9-47af-bb43-ced2caceccab.png"></div>
<div align=center><img width="317" alt="image" src="https://user-images.githubusercontent.com/109843978/181151656-b67dd865-fb58-4110-8fe1-ceaa27952e53.png"></div>
known()则是从上帝视角生成正确的散列值，以便于和attack函数的结果对比：
<div align=center><img width="300" alt="image" src="https://user-images.githubusercontent.com/109843978/181151790-ab755132-ac23-412b-8e18-cbb37337ab4d.png"></div>



## 运行截图

给定默认的原始信息和附加信息，检验攻击是否成功：
<div align=center><img width="448" alt="image" src="https://user-images.githubusercontent.com/109843978/181151901-cb1aeffc-4de7-49bc-85ad-dda35cf10706.png"></div>
运行结果:
<div align=center><img width="822" alt="image" src="https://user-images.githubusercontent.com/109843978/181151982-7ef3fff7-af47-46d2-8257-b8677eac96a0.png"></div>
由打印的内容可知，可以完成攻击.

# 运行指导

该文件与SM3文件在一个文件夹中，代码可直接运行.







