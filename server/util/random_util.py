import random
import bisect

# coding=utf-8
class random_util:
    def __init__(self, items):
        weights = [w for _, w in items]
        self.goods = [x for x, _ in items]
        self.total = sum(weights)
        self.acc = list(self.accumulate(weights))

    def accumulate(self, weights):  # 累和.如accumulate([10,40,50])->[10,50,100]
        cur = 0
        for w in weights:
            cur = cur + w
            yield cur

    def __call__(self):
        return self.goods[bisect.bisect_right(self.acc, random.uniform(0, self.total))]

#
# wr = random_util([('a1', 10), ('a2', 20), ('a3', 30), ('a4', 40)])
# print(wr())
