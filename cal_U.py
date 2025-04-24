import copy

import creatData


# Used for calculating utility
def calu(user, price, userd):
    pois = creatData.getPOI()
    userbid = creatData.getuserbid()
    vm = pois[0]
    km = pois[1]
    POI_M = len(vm)
    user_uti = 0
    sever_uti = 0
    sever_paid = 0
    kmtmp = copy.deepcopy(km)
    winuser = 0
    for u in user:
        userut = [[] for i in range(POI_M)]
        for m in range(POI_M):
            if price[m] >= userbid[u][m]:
                userut[m] = [round(price[m] - userbid[u][m], 2), m]
            else:
                userut[m] = ([-1, -1])
        userut.sort(reverse=True)
        usersele = False
        user_temp = copy.deepcopy(userut)
        i=0
        for j in range(len(user_temp)):
            indx = user_temp[j][1]
            if kmtmp[indx] > 0 and indx != -1:
                user_uti += round(user_temp[j][0], 2)
                sever_uti += round(vm[indx] - price[indx], 2)
                sever_paid += round(price[indx], 2)
                kmtmp[indx] -= 1
                user_temp[j][1] = -1
                usersele = True
                i=i+1
            if i>=userd:
                break
        if usersele:
            winuser += 1
    coverrate = (sum(km) - sum(kmtmp)) / sum(km)
    print("the sever utility is", sever_uti)
    print("the users utility is", user_uti)
    print("the sever payment is", sever_paid)
    print("the total utility is", user_uti + sever_uti)
    print("the POI coverage rate is", coverrate)

    return sever_uti, user_uti, sever_paid, user_uti + sever_uti, winuser, coverrate
