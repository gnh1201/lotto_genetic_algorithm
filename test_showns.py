# Lotto prediction with Genetic Algorithm and Mersenne Twister (MT19937)
# Go Namhyeon <gnh1201@gmail.com>
# first created: 2021-04-04
# last updated: 2022-09-02
# download excel data: https://dhlottery.co.kr/gameResult.do?method=byWin

import math
import random
import pandas as pd
import numpy as np

cols = [13, 14, 15, 16, 17, 18, 19]  # included bonus number
df = pd.read_excel('excel.xlsx', skiprows=2, usecols=cols, names=[0, 1, 2, 3, 4, 5, 6])
rows = df.values[:100]

def step1():
    data = []

    i = 0
    while i < len(rows):
        cur = rows[i]

        _rows = list(rows)[i+1:i+11]

        showns = []
        for row in _rows:
            showns = sorted(list(set(showns) | set(row)))
        notShowns = sorted(list(set(range(1, 46)) - set(showns)))
        data.append({
            'showns': showns,
            'notShowns': notShowns
        })

        i = i + 1

    return data

data = step1()

def get_numbers(lastData):
    num = random.sample(range(1, 46), 7)
    notShowns = lastData['notShowns']
    return random.sample(list(set(num) | set(notShowns)), 6)

def evaluate(nums):
    _rows = list(rows)

    score = 0
    for row in _rows:
        result = len(list(set(nums) & set(row)))
        if result > 5:
            score += 100
        elif result > 4:
            score += 75
        elif result > 3:
            score += 50
        elif result > 2:
            score += 25

    return str(round((score / len(rows)) * 50, 2)) + '%'

k = 0
while k < 10:
    nums = get_numbers(data[0])
    k = k  + 1
    print (evaluate(nums), nums)
