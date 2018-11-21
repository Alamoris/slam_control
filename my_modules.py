import math


# инвертированный range
def reversedRange(x):
    while x > 0:
        yield x
        x -= 1

# Рассчет длинны гипотенузы
def gip_len(first_x, first_y, fin_x, fin_y):
    gip = math.sqrt((first_x - fin_x) ** 2 + (first_y - fin_y) ** 2)
    return gip
