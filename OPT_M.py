from docplex.mp.model import Model
import creatData
import numpy as np


def opt_m(userd, userlist):
    pois = creatData.getPOI()
    userbid = creatData.getuserbid()
    vm = pois[0]
    km = pois[1]
    d = float(userd)
    user_N = len(userlist)
    POI_M = len(vm)

    model = Model(name='OPTm')

    x = [[model.binary_var(name=f'x_{i}_{j}') for j in range(POI_M)] for i in range(user_N)]

    model.maximize(model.sum((vm[j] - userbid[userlist[i]][j]) * x[i][j] for i in range(user_N) for j in range(POI_M)))

    for j in range(POI_M):
        model.add_constraint(model.sum(x[i][j] for i in range(user_N)) <= km[j], f'poi_limit_{j}')

    for i in range(user_N):
        model.add_constraint(model.sum(x[i][j] for j in range(POI_M)) <= d, f'user_limit_{i}')

    solution = model.solve(log_output=False)
    cval = solution.objective_value

    x_ij=[]

    for i in range(user_N):
        temp = 0
        for j in range(POI_M):
            x_ij.append(x[i][j].solution_value)
            temp += x[i][j].solution_value
        if temp<d:
            print(temp,userbid[userlist[i]])
    for j in range(POI_M):
        temp = 0
        for i in range(user_N):
            temp += x[i][j].solution_value
        print(temp)
    xij = np.array(x_ij)
    xij = xij.reshape(user_N, POI_M)
    np.savetxt("xij.txt", xij, fmt="%d")
    return cval


