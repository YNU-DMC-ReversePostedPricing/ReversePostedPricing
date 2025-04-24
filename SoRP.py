import torch
import numpy as np

import cal_U
import creatData

# gradient descent
def autograd(p_values, xij, userbid, vm, km, userlist):
    poi_m = len(userbid[0])
    userutility = [0 for i in range(len(userlist))]
    bid_sum=0
    for i in range(len(userlist)):
        for m_ in range(len(xij[0])):
            if p_values[m_] - userbid[userlist[i]][m_] > 0:
                userutility[i] += (p_values[m_] - userbid[userlist[i]][m_]) * xij[i][m_]
                bid_sum += (p_values[m_] - userbid[userlist[i]][m_])* xij[i][m_]
            else:
                userutility[i] += 0

    poiutility = [0 for j in range(poi_m)]
    for j in range(poi_m):
        for i in range(len(userlist)):
            poiutility[j] += userutility[i] * xij[i][j]


    y_values = sum([(km[j] * (vm[j] - p_values[j]) - poiutility[j]) ** 2 for j in range(poi_m)])
    targets = y_values
    targets = torch.sum(targets)
    targets.backward()
    return [float(p_values[i].grad) for i in range(len(p_values))], targets


def autoPrice(data_xij):
    pois = creatData.getPOI()
    userbid = creatData.getuserbid()
    userlist = creatData.getuserlist()
    vm = pois[0]
    km = pois[1]
    POI_M = len(vm)
    # autograd
    loss = float('inf')

    x = [0.0 for i in range(POI_M)]
    while loss >0.01:
        alph = 0.000001
        x_, tar = autograd([torch.tensor(x[i] * 1.0, requires_grad=True) for i in range(POI_M)], data_xij, userbid, vm,
                           km, userlist)
        loss = float(tar)
        print("loss = ", loss)
        for i in range(POI_M):
            d = x[i] - alph * float(x_[i])
            x[i] = d
        print([x[i] for i in range(POI_M)])
    np.savetxt("price.txt", x, fmt="%f")
    return x

