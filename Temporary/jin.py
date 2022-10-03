import math
import random
import numpy as np
import sys
import copy


#城市数量
n = 4
distance = [[0,1,0.5,1],[1,0,1,1],[1.5,5,0,1],[1,1,1,0]]

#禁忌表
tabu_list = []
tabu_time = []
#当前禁忌对象数量
current_tabu_num = 0
#禁忌长度，即禁忌期限
tabu_limit = 2

#最佳路径以及最佳距离
best_route = []
best_distance = sys.maxsize
current_route = []
current_distance = 0.0

def init():
    sum=0.0
    visited = []
    id = 0
    frontid=0
    visited.append(0)
    i=1
    while i<n:
        id=random.randint(1,n-1)
        if(id not in visited):
            visited.append(id)
            sum+=distance[frontid][id]
            i+=1
        frontid=id
    sum+=distance[id][0]
    print("初始解：",visited,"f(s)=",sum)
    return visited

def factorial(n):
    sum=0
    for i in range(1,n-1):
        sum+=i
    return sum

#构建初始参考距离矩阵
def getdistance():
    for i in range(n):
        for j in range(n):
            if distance[i][j] == 0:
                distance[i][j] = sys.maxsize
                
#计算总距离
def cacl_best(rou):
    sumdis = 0.0
    for i in range(n-1):
        sumdis += distance[rou[i]][rou[i+1]]
    sumdis += distance[rou[n-1]][rou[0]]     
    return sumdis

#初始设置
def setup():
    global best_route
    global best_distance
    global tabu_time
    global current_tabu_num
    global current_distance
    global current_route
    global tabu_list
    #得到初始解以及初始距离
    #current_route = random.sample(range(0, n), n) 
    current_route = init()
    #current_route = [0,1,2,3]
    best_route = copy.copy(current_route)
    #函数内部修改全局变量的值
    current_distance = cacl_best(current_route)
    best_distance = current_distance
    
    #置禁忌表为空
    tabu_list.clear()
    tabu_time.clear()
    current_tabu_num = 0

#交换数组两个元素
def exchange(index1, index2, arr):
    current_list = copy.copy(arr)
    current = current_list[index1]
    current_list[index1] = current_list[index2]
    current_list[index2] = current

    return current_list

#存储两个交换的位置
exchange_position= []
def getcan(start,n,a):
    if n==1:
        return
    for i in range(1,n):
        current=[]
        current.append(a[start])
        current.append(a[start+i])
        exchange_position.append(current)
    return getcan(start+1,n-1,a)

#得到邻域 候选解
def get_candidate():
    global best_route
    global best_distance
    global current_tabu_num
    global current_distance
    global current_route
    global tabu_list
    global c
    #候选集
    candidate=[]
    candidate_distance = []
    temp = 0
    exchange_position.clear()
    getcan(1,n-1,current_route)

    for current in exchange_position:
        if current not in tabu_list and current[::-1] not in tabu_list:
            candidate.append(exchange(current_route.index(current[0]), current_route.index(current[1]), current_route))
            candidate_distance.append(cacl_best(candidate[temp]))
            temp += 1
        else:
            exchange_position.remove(current)

  
            

    #得到候选解中的最优解
    if candidate_distance:
        candidate_best = min(candidate_distance)
    else:
        candidate_best =candidate_best
    best_index = candidate_distance.index(candidate_best)
    
    current_distance = candidate_best
    current_route = copy.copy(candidate[best_index])
    print("candidate：",candidate)
    print("current_distance：",current_distance,"       current_route：",current_route)

    
    #与当前最优解进行比较 
    
    if current_distance < best_distance:
        best_distance = current_distance
        best_route = copy.copy(current_route)
        
    
    #加入禁忌表
    tabu_list.append(exchange_position[best_index])
    tabu_time.append(tabu_limit)
    current_tabu_num += 1


    candidate.clear()
    candidate_distance.clear()
    
#更新禁忌表以及禁忌期限
def update_tabu():
    global current_tabu_num
    global tabu_time
    global tabu_list
    del_num = 0
    temp = []
    
    #如果达到期限，释放
    for i in range(current_tabu_num):
        if tabu_time[i] == 0:
            del_num += 1
            temp = tabu_list[i]
           
    current_tabu_num -= del_num        
    while 0 in tabu_time:
        tabu_time.remove(0)
    
    while temp in tabu_list:
        tabu_list.remove(temp)

    
    #更新步长
    tabu_time = [x-1 for x in tabu_time]
    

                
def solve():
    getdistance()
    runtime = int(input("迭代次数："))
    setup()
    for rt in range(runtime):
        print("次数：",rt)
        get_candidate()
        update_tabu()
        print("tabu_list：",tabu_list,"\n\n\n")
    print("最优距离：")    
    print(best_route)
    print(best_distance)
    
if __name__=="__main__":
    solve()
    
