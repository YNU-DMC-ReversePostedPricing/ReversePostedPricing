from docplex.mp.model import Model
import creatData
import numpy as np


def OPTpm(userd, userlist):
    pois = creatData.getPOI()
    userbid = creatData.getuserbid()
    price = creatData.getPrice()
    vm = pois[0]
    km = pois[1]
    d = float(userd)
    user_N = len(userlist)
    POI_M = len(vm)
    user_bid = [[] for i in range(user_N)]
    for i in range(user_N):
        user_bid[i] = userbid[userlist[i]]

    model = Model(name='OPTpm')

    x = [[model.binary_var(name=f'x_{i}_{j}') for j in range(POI_M)] for i in range(user_N)]

    model.maximize(model.sum((vm[j] - user_bid[i][j]) * x[i][j] for i in range(user_N) for j in range(POI_M)))

    for j in range(POI_M):
        model.add_constraint(model.sum(x[i][j] for i in range(user_N)) <= km[j], f'poi_limit_{j}')

    for i in range(user_N):
        model.add_constraint(model.sum(x[i][j] for j in range(POI_M)) <= d, f'user_limit_{i}')

    for i in range(user_N):
        model.add_constraint(model.sum(x[i][j]*user_bid[i][j] for j in range(POI_M))-model.sum(x[i][j]*price[j] for j in range(POI_M)) <=0, f'price_limit_{i}')

    solution = model.solve(log_output=False)
    cval=solution.objective_value

    sever_ut = 0
    user_ut = 0
    sever_paid = 0
    winner = 0
    km_tmp = [0 for i in range(POI_M)]
    for i in range(len(userlist)):
        win_ = False
        for j in range(POI_M):
            if x[i][j].solution_value == 1:
                sever_ut += round(vm[j] - price[j], 2)
                user_ut += round(price[j] - userbid[userlist[i]][j], 2)
                sever_paid += round(price[j], 2)
                win_ = True
                km_tmp[j] += 1
        if win_:
            winner += 1
    coverrate = sum(km_tmp) / sum(km)
    return cval, sever_ut, user_ut, sever_paid, winner, coverrate


