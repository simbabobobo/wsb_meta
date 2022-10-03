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