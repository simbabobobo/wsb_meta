"""

@author: hxw

description：

 基于TSP，使用禁忌搜索算法及gurobi进行求解，

 比较两者的结果并输出

"""

from basic_class import Instance
from tsp_gurobi import gurobi_solve
import random
import copy
import time
import cPickle as pickle
import csv

def multy():
  node_count_list = [10, 20, 50, 100, 200] #定义测试集
  result = dict()
  for node_count in node_count_list:
    seed_value = random.randint(1, 100000) #产生随机种子数
    inst = Instance(node_count, seed_value) #生成算例
    random.seed(inst.seed_value)
    start_time = time.clock()
    gurobi_result = gurobi_solve(inst) #调用gurobi求解
    end_time = time.clock()
    gurobi_time = end_time - start_time
    gurobi_result['time'] = gurobi_time
    start_time = time.clock()
    tabu_result = tabu_solve(inst, start_time, gurobi_time,gurobi_result['cost']) #调用tabuSearch求解
    end_time = time.clock()
    tabu_time = end_time - start_time
    tabu_result['time'] = tabu_time
    result['gurobi,' + str(node_count)] = gurobi_result
    result['tabu_search,' + str(node_count)] = tabu_result
  #将结果用pickle及csv存储
  f= file('result/experiment_3.pkl', 'wb')
  pickle.dump(result, f, True)
  f.close()
  table = [['node_count'], ['gurobi_obj'], ['gurobi_time'], ['ts_obj'],['ts_time'], ['avg_obj_gap']]
  for node_count in node_count_list:
    table[0].append(node_count)
    gurobi_result = result['gurobi,' + str(node_count)]
    tabu_result = result['tabu_search,' + str(node_count)]
    table[1].append(gurobi_result['cost'])
    table[2].append(gurobi_result['time'])
    table[3].append(tabu_result['cost'])
    table[4].append(tabu_result['time'])
    obj_gap = (tabu_result['cost'] -gurobi_result['cost']) / gurobi_result['cost']
    table[5].append(round(obj_gap, 3))
  print(table)
  f= open('result/experiment_3.csv', 'wb')
  writer = csv.writer(f)
  for line in table:
    writer.writerow(line)
  f.close()

def tabu_solve(inst, start_time, gurobi_time,best_obj):
  #函数功能：随机生成一个输出路径（初始解）
  def initial_route():
    route = []
    unvisited = range(n)
    count = n
    while(count != 0):
      index = random.randint(0, count - 1)
      current = unvisited[index]
      route.append(current)
      unvisited.remove(current)
      count -= 1
    return route
  #函数功能：输出路径的目标值
  def cal_distance(route):
    distance = 0.0
    for i in range(n - 1):
      distance += get_edge(i, i+1, route)
    distance += get_edge(0, n-1, route)
    return distance
  #函数功能：获取两点之间的边距
  def get_edge(index_i, index_j, route):
    if(index_i == n):
      index_i = 0
    if(index_j == n):
      index_j = 0
    return edge[route[index_i]][route[index_j]]
  #函数功能：计算邻域（按Swap算子）
  def cal_neighbor(nid_i, nid_j, route):
    \#i, j means the node id, and the index_i and index_j means the node'sindex in route
    index_i = route.index(nid_i)
    index_j = route.index(nid_j)
    delta = 0
    if(index_i == index_j - 1 or index_i == index_j + n - 1):
      delta += get_edge(index_i, index_j + 1, route) + get_edge(index_i - 1,index_j, route)
      delta -= get_edge(index_i - 1, index_i, route) + get_edge(index_j,index_j + 1, route)
    elif(index_i == index_j + 1 or index_j == index_i + n -1):
      delta += get_edge(index_j, index_i + 1, route) + get_edge(index_j - 1,index_i, route)
      delta -= get_edge(index_j - 1, index_j, route) + get_edge(index_i,index_i + 1, route)
    else:
      delta += get_edge(index_j, index_i - 1, route) + get_edge(index_j,index_i + 1, route)
      delta += get_edge(index_i, index_j - 1, route) + get_edge(index_i,index_j + 1, route)
      delta -= get_edge(index_i, index_i - 1, route) + get_edge(index_i,index_i + 1, route)
      delta -= get_edge(index_j, index_j - 1, route) + get_edge(index_j,index_j + 1, route)
    return delta

  def output_route(info, route, distance):
    print(info, ', tour:', route, ', distance:', distance)
  eplison = 0.000001
  iteration = 10000 #最大迭代次数
  n= inst.n
    tabu_length= int(n * 0.2) #禁忌长度——这里设置为节点数的20%
  points = inst.points
  dist = inst.dist
  edge = [([0] * n) for i in range(n)]
  for j in range(n):
    for i in range(n):
      if(i > j):
        edge[i][j] = dist.get((i,j))
      elif(i < j):
        edge[i][j] = edge[j][i]
  tabu_list = [([0] * n) for i in range(n)] #定于禁忌表
    #best用于存储搜索最优目标值，local用于存储搜索当前目标值
  best = float('inf')
  best_route = list()
  local = 0.0
  ini_route = initial_route()
  local = cal_distance(ini_route)
  best = min(best, local)
  route = copy.copy(ini_route)
  best_route = copy.copy(ini_route)
    #计算初始邻域
  neighbors = dict()
  for i in range(n):
    for j in range(i + 1, n):
      neighbors[str(i) + ',' + str(j)] = cal_neighbor(i, j, route)
  #print(neighbors)
    #搜索开始
  for k in range(iteration):
    sorted_neighbors = sorted(neighbors.items(), key = lambda item :item[1])
    #print('sort_neighbors', sorted_neighbors)
    nid_i = nid_j = 0
    flag = 0
    for neighbor in sorted_neighbors:
      nids = neighbor[0].split(',')
      nid_i = int(nids[0])
      nid_j = int(nids[1])
      delta = neighbor[1]
      temp_local = local + delta
      # 破禁准则
      if(temp_local < best):
        local = temp_local
        best = local
        flag = 1
      else:
              #禁忌表数值非零时，跳过当前邻域
        if(tabu_list[nid_i][nid_j] !=0):
          continue
        else:
          local = temp_local
      break
    # 根据上述邻域选择的结果，更新路径（按swap交换两个节点）
    index_i = route.index(nid_i)
    index_j = route.index(nid_j)
    route.pop(index_i)
    route.insert(index_i, nid_j)
    route.pop(index_j)
    route.insert(index_j, nid_i)
    if(flag == 1):
      best_route = copy.copy(route)
    # 更新禁忌表
    for i in range(n):
      for j in range(n - i):
        if(tabu_list[i][j] != 0):
          tabu_list[i][j] -= 1
    tabu_list[nid_i][nid_j] = tabu_length
    # 更新邻域
    for i in range(n):
      for j in range(i + 1, n):
        neighbors[str(i) + ',' +str(j)] = cal_neighbor(i, j, route)
    end_time = time.clock()
    if(end_time - start_time > gurobi_time + eplison or abs(best_obj -best) < eplison):
      break
    #将TS结果按字典形式返回
  result = dict()
  result['tour'] = str(best_route)
  result['cost'] = best
  return result



def main():
  multy()
if(__name__ == '__main__'):
  main()
  print('finished')
#%%
import math
import random
#Instance类的定义方式
class Instance:
  def __init__(self, n, seed_value):
    self.n = n # the count of nodes
    self.seed_value = seed_value
    random.seed(self.seed_value)
    self.points = [(random.randint(0, 100), random.randint(0, 100)) \
        for i in range(n)] # coordinates of nodes
    self.dist = {(i, j) : math.sqrt(sum((self.points[i][k] -self.points[j][k])**2 \
        for k in range(2))) for i inrange(n) for j in range(i)} # edges between nodes
  def __str__(self):
    pass