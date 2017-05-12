a = ['1','2','1','1','2','2','2','2','3','6','6', '6','6', '3','4','6','6']
a.sort()
from itertools import groupby
data = {key : len(list(group)) for key, group in groupby(a)}
print sorted(data, key=data.get, reverse=True)