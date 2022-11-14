
def fitness(X, ori, eq, ueq):
    value = ori(X)
    eq_value = []
    ueq_value = []
    for i in eq:
        eq_i = lambda x: eval(i)
        eq_value.append(eq_i(X))
    eq_value=np.array(eq_value)
    penalty_eq = np.array([np.sum((np.abs(eq_value))**2)])
    for i in ueq:
        ueq_i = lambda x: eval(i)
        ueq_value.append(max(0, ueq_i(X)))
    ueq_value = np.array(ueq_value)
    penalty_ueq = np.array([np.sum(ueq_value)])
    value = value + 1e5 * penalty_eq + 1e5 * penalty_ueq

    return value

def read_mps(model):
    base_path = os.path.dirname(os.path.dirname(__file__))
    in_path = os.path.join(base_path, 'model_file_mps', model)
    # os.path.join 将目录和文件名合成一个路径
    print(in_path)
    return in_path

