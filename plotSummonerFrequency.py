from MatchHistory import load_full_history
from matplotlib import pyplot as plot

summoners = {}
for m in load_full_history():
    for s in m.get_all_summoner():
        if s in summoners:
            summoners[s] += 1
        else:
            summoners[s] = 1

duplicates = {}

for s in summoners:
    if summoners[s] > 1:
        duplicates[s] = summoners[s]

duplicates = dict(sorted(duplicates.items(), reverse=True, key=lambda item: item[1]))

plot.bar(duplicates.keys(), duplicates.values())
plot.xticks(rotation=90)
plot.show()

print(duplicates)
