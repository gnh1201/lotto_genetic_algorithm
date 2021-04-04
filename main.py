# Lotto prediction with Genetic Algorithm and Mersenne Twister (MT19937)
# Go Namhyeon <gnh1201@gmail.com>
# 2021-04-04
# download excel data: https://dhlottery.co.kr/gameResult.do?method=byWin

import pandas as pd
import numpy as np
from geneticalgorithm2 import geneticalgorithm2 as ga

cols = [1, 13, 14, 15, 16, 17, 18, 19]  # including bonus number
df = pd.read_excel('excel.xlsx', skiprows=2, usecols=cols, names=[0, 1, 2, 3, 4, 5, 6, 7])
rows = df.values[:10]

def make_num(x, n, a, b, c, min, max):
    seed = int(x*a + n*b + c)
    rs = np.random.RandomState(np.random.MT19937())
    rs.seed(seed)
    return min + round((max - min) * rs.random())

def f(X):
    score = 0

    for row in rows:
        x  = row[0]
        N = row[1:]
        _N = [make_num(x, n, X[0], X[1], X[2], 1, 45) for n in range(1, 8)]  # including bonus number
        result = len(list(set(N) & set(_N)))
        if result > 5:
            score += 100
        elif result > 4:
            score += 75
        elif result > 3:
            score += 50
        elif result > 2:
            score += 25

    return -score

varbound = np.array([[0, 10000]]*3)

model = ga(function=f, dimension=3, variable_type='int', variable_boundaries=varbound)
model.run()

solution = model.output_dict
variable = model.output_dict['variable']

_x = max([row[0] for row in rows]) + 1  # get highest number

print ('Recommended numbers (' + str(_x) + 'th):')
nums = sorted([make_num(_x, n, variable[0], variable[1], variable[2], 1, 45) for n in range(1, 7)])
print(', '.join(str(x) for x in nums))
