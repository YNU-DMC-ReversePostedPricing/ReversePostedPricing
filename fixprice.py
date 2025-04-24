import math

import creatData

# Fix price
def getprice(yu):
    pois = creatData.getPOI()
    vm = pois[0]
    price = []
    for vs in vm:
        price.append(vs * yu)
    return price

