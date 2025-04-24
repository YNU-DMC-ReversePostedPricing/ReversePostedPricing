import random
import numpy as np
import torch
import os
import OMZ
import OPT_M
import OPT_pm
import cal_U
import creatData
import fixprice
import SoRP

def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    os.environ['CUBLAS_WORKSPACE_CONFIG'] = ':4096:8'
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

set_seed(42)

"""1.creat data"""
needcreat = 1
usernum =250
userd =2
if needcreat:
    creatData.creatData(usernum)
    creatData.creatuserd(usernum, userd)
"""2.suffer user list"""
listnum =250
users = creatData.creatuserlist(usernum, listnum)
"""3.run opt"""
optm = OPT_M.opt_m(userd, users)
print(optm)
"""4.run GD for Reward Price"""
"""read xij"""
with open("./xij.txt", 'r') as f_xij:
    xij_ = f_xij.readlines()
data_xij = []
for u in xij_:
    datas = []
    u = u.strip("\n")
    u = u.rstrip()
    data_split = u.split(" ")
    temp = list(data_split)
    for i in temp:
        p = int(i)
        datas.append(p)
    data_xij.append(datas)
SoRP.autoPrice(data_xij)
price = creatData.getPrice()
"""5.run opt_pm"""
opt_pm, ser_ut_opt, user_ut_opt, ser_pay_opt, winnum, coverrate_opt = OPT_pm.OPTpm(userd, users)
print("opt_pm", opt_pm)
print("optm", optm)
# start test
sever_uti_GDRP, user_uti_GDRP, sever_payment_GDRP, totalut_GDRP, winuser_GDRP, coverrate_GDRP = 0, 0, 0, 0, 0, 0
sever_uti_OMZ, user_uti_OMZ, sever_payment_OMZ, totalut_OMZ, winuser_OMZ, coverrate_OMZ = 0, 0, 0, 0, 0, 0
sever_uti_FIXPRICE, user_uti_FIXPRICE, sever_payment_FIXPRICE, totalut_FIXPRICE, winuser_FIXPRICE, coverrate_FIXPRICE = 0, 0, 0, 0, 0, 0
sever_uti_FIXPRICE1, user_uti_FIXPRICE1, sever_payment_FIXPRICE1, totalut_FIXPRICE1, winuser_FIXPRICE1, coverrate_FIXPRICE1 = 0, 0, 0, 0, 0, 0
rond = 500
for i in range(rond):
    print("round %d #####################################" % i)
    # suffer
    random.shuffle(users)
    print("users: ", users)
    # 1.GD for Reward Price test
    print("GDRP start.........................")
    print(price)
    sever_uti_GDRP0, user_uti_GDRP0, sever_payment_GDRP0, totalut_GDRP0, winuser_GDRP0, coverrate_GDRP0 = cal_U.calu(
        users, price, userd)
    sever_uti_GDRP += sever_uti_GDRP0
    user_uti_GDRP += user_uti_GDRP0
    sever_payment_GDRP += sever_payment_GDRP0
    totalut_GDRP += totalut_GDRP0
    winuser_GDRP += winuser_GDRP0
    coverrate_GDRP += coverrate_GDRP0
    print("GDRP end.........................")
    # 2.OMZ test
    print("OMZ start.........................")
    sever_uti_OMZ0, user_uti_OMZ0, sever_payment_OMZ0, totalut_OMZ0, winuser_OMZ0, coverrate_OMZ0 = OMZ.getOMZ(users,
                                                                                                               userd)
    sever_uti_OMZ += sever_uti_OMZ0
    user_uti_OMZ += user_uti_OMZ0
    sever_payment_OMZ += sever_payment_OMZ0
    totalut_OMZ += totalut_OMZ0
    winuser_OMZ += winuser_OMZ0
    coverrate_OMZ += coverrate_OMZ0
    print("OMZ end.........................")
    # 3.fix price test
    print("FIXPRICE start.........................")
    price_fix = fixprice.getprice(0.4)
    sever_uti_FIXPRICE0, user_uti_FIXPRICE0, sever_payment_FIXPRICE0, totalut_FIXPRICE0, winuser_FIXPRICE0, coverrate_FIXPRICE0 = cal_U.calu(
        users, price_fix, userd)
    sever_uti_FIXPRICE += sever_uti_FIXPRICE0
    user_uti_FIXPRICE += user_uti_FIXPRICE0
    sever_payment_FIXPRICE += sever_payment_FIXPRICE0
    totalut_FIXPRICE += totalut_FIXPRICE0
    winuser_FIXPRICE += winuser_FIXPRICE0
    coverrate_FIXPRICE += coverrate_FIXPRICE0
    print("FIXPRICE end.........................")

print("test end%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
print("optm:", optm)
print("optpm:", opt_pm)
print("total utility:   OPT_pm:", round(opt_pm, 2), "    GDRP:", round(totalut_GDRP / rond, 2), "    OMZ:",
      round(totalut_OMZ / rond, 2), "   FIXPRICE0.4:", round(totalut_FIXPRICE / rond, 2))
print("sever utility:   OPT_pm:", round(ser_ut_opt, 2), "   GDRP:", round(sever_uti_GDRP / rond, 2), "    OMZ:",
      round(sever_uti_OMZ / rond, 2), "    FIXPRICE0.4:", round(sever_uti_FIXPRICE / rond, 2))
print("user utility:    OPT_pm:", round(user_ut_opt, 2), "    GDRP:", round(user_uti_GDRP / rond, 2), "   OMZ:",
      round(user_uti_OMZ / rond, 2), "  FIXPRICE0.4:", round(user_uti_FIXPRICE / rond, 2))
print("sever payment:   OPT_pm:", round(ser_pay_opt, 2), "    GDRP:", round(sever_payment_GDRP / rond, 2), "  OMZ:",
      round(sever_payment_OMZ / rond, 2), " FIXPRICE0.4:", round(sever_payment_FIXPRICE / rond, 2))
print("count of winners:    OPT_pm:", winnum, "   GDRP:", winuser_GDRP / rond, "  OMZ:", winuser_OMZ / rond,
      "    FIXPRICE0.4:", winuser_FIXPRICE / rond)
print("POI coverage rate:    OPT_pm:", coverrate_opt, "   GDRP:", coverrate_GDRP / rond, "  OMZ:", coverrate_OMZ / rond,
      "    FIXPRICE0.4:", coverrate_FIXPRICE / rond)
