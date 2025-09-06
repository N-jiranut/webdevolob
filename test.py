import pandas as pd

main=[]
for n in range(10):

    for i in range(21):
        for type in ["lx","ly"]:
            main.append(str(n)+type+str(i))
    for i in range(21):
        for type in ["rx","ry"]:
            main.append(str(n)+type+str(i))
    for i in [0,11,12,13,14]:
        for type in ["bx","by"]:
            main.append(str(n)+type+str(i))
# test = [1 for _ in range(84)]

df = pd.DataFrame(columns=main)
# df = pd.DataFrame([test])
df.to_csv("data/main.csv", mode="w", index=False, header=True)
