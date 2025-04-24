import copy
import math
import random
import numpy as np

import cal_U
import creatData


# initialization
def init(userd):
    global userbid_, budget, vm, r, userd_temp, userselpoi
    poiss_ = creatData.getPOI()
    userbid_ = creatData.getuserbid()
    vm = poiss_[0]
    r = poiss_[1]
    budget = sum([vm[i] * r[i] for i in range(len(vm))])
    userd_temp = userd
    userselpoi = [[] for i in range(len(userbid_))]


# value function
def V_s(S: list, j=-1):
    if len(S) == 0 and j == -1:
        return 0, []
    copyusers = copy.deepcopy(S)
    if j != -1:
        copyusers.append(j)
    values = 0
    userbids = []
    const_r = copy.deepcopy(r)
    for i in copyusers:
        value_temp = [[] for j in range(len(vm))]
        bidtemp = []
        for m in range(len(vm)):
            value_temp[m] = [vm[m], m]
        flg = [0 for s in range(len(vm))]
        for d in range(userd_temp):
            for p in range(len(vm)):
                if const_r[value_temp[p][1]] > 0 and flg[value_temp[p][1]] == 0:
                    values += value_temp[p][0]
                    const_r[value_temp[p][1]] -= 1
                    bidtemp.append(value_temp[p][1])
                    flg[value_temp[p][1]] = -1
                    break
        if i == j:
            userbids = bidtemp
    return values, userbids


def mar_vs(set_s: list, index):
    val1, userindex = V_s(set_s, index)
    val2 = V_s(set_s)[0]
    return val1 - val2, userindex


# OMZ
def OMZ(BudgetB, DeadlineT, userlist):
    epsilon = 1
    t = 1
    timeset_ = (DeadlineT / (2 ** int((math.log(DeadlineT, 2)))))
    stagebudget = (BudgetB / (2 ** int((math.log(DeadlineT, 2)))))
    sampleuser_ = []
    rou_ = epsilon
    selectuser = []
    p = [0 for i in range(len(userbid_))]
    idn = 0
    while t <= DeadlineT:
        usercome = np.random.poisson(5)
        for i in range(int(usercome)):
            if idn >= len(userlist):
                break
            user = userlist[idn]
            val, allpoi = mar_vs(selectuser, user)
            user_bid = 0
            for poi in allpoi:
                user_bid += userbid_[user][poi]
            ssb = (stagebudget - sum([p[m] for m in selectuser]))
            xs = val / rou_
            if user_bid <= (val / rou_) <= ssb:
                p[user] = val / rou_
                if p[user] != 0:
                    selectuser.append(user)
            sampleuser_.append(user)
            idn += 1

            if t == int(timeset_):
                rou_tmp = GetDensityThreshold(stagebudget, sampleuser_)
                if rou_tmp != 0:
                    rou_ = rou_tmp
                timeset_ = 2 * timeset_
                stagebudget = 2 * stagebudget
        if idn >= len(userlist):
            break
        t = t + 1
    return p, selectuser


def GetDensityThreshold(stage_B, userlist: list):
    copy_S = copy.deepcopy(userlist)
    delta = 1.5
    list_j = []
    max_tmp = 0
    max_i = -1
    max_ibid = 0

    for tmp_j in copy_S:
        val, index = mar_vs(list_j, tmp_j)
        sumb = 0
        for m in index:
            sumb += userbid_[tmp_j][m]

        if max_tmp < val / sumb:
            max_tmp = val / sumb
            max_i = tmp_j
            max_ibid = sumb

    while max_ibid <= ((mar_vs(list_j, max_i)[0] * stage_B) / V_s(list_j, max_i)[0]):
        list_j.append(max_i)
        max_tmp = 0
        for tmp_j in copy_S:
            if tmp_j not in list_j:
                val, index = mar_vs(list_j, tmp_j)
                if not index:
                    continue
                sumbs = 0
                for m in index:
                    sumbs += userbid_[tmp_j][m]
                if max_tmp < val / sumbs:
                    max_tmp = val / sumbs
                    max_i = tmp_j

    rou = V_s(list_j)[0] / stage_B
    return rou / delta


def getOMZ(users, userd):
    init(userd)
    user_uti = 0
    sever_uti = 0
    sever_paid = 0
    totalut = 0
    T = 50
    payment, selusers = OMZ(budget, T, users)
    if not selusers:
        return sever_uti, user_uti, sever_paid, totalut, 0, 0
    copyr = copy.deepcopy(r)
    selpoitemp = [[] for j in range(len(selusers))]
    sumbid = [0 for j in range(len(selusers))]
    sumvm = [0 for j in range(len(selusers))]
    winners = 0
    value_temp = [[] for j in range(len(vm))]
    for m in range(len(vm)):
        value_temp[m] = [vm[m], m]
    for i in range(len(selusers)):
        vmsum = 0
        flg = [0 for s in range(len(vm))]
        for d in range(userd):
            for p in range(len(vm)):
                if copyr[value_temp[p][1]] > 0 and flg[value_temp[p][1]] == 0:
                    copyr[value_temp[p][1]] -= 1
                    selpoitemp[i].append(value_temp[p][1])
                    sumbid[i] += userbid_[selusers[i]][value_temp[p][1]]
                    vmsum += vm[value_temp[p][1]]
                    flg[value_temp[p][1]] = -1
                    break
        sumvm[i] = vmsum

    usercr = 0
    for user in range(len(selusers)):
        if sumbid[user] <= payment[selusers[user]] <= sumvm[user]:
            user_uti += (payment[selusers[user]] - sumbid[user])
            sever_uti += sumvm[user] - payment[selusers[user]]
            sever_paid += payment[selusers[user]]
            winners += 1
            usercr += len(selpoitemp[user])

    coverrate = usercr / sum(r)
    print("^^^^^^^^^^^^^^^^")
    print("the sever utility is", sever_uti)
    print("the users utility is", user_uti)
    print("the sever payment is", sever_paid)
    print("the total utility is", user_uti + sever_uti)
    print("winners is", selusers)
    print("winners number is", winners)
    print("cover rate is", coverrate)

    return sever_uti, user_uti, sever_paid, sever_uti + user_uti, winners, coverrate


# user = creatData.creatuserlist(250, 250)
# getOMZ(user, 2)
