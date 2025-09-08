import pandas as pd

main=[]
for n in range(10):
    for type in ["l","r"]:
        for i in range(21):
            main.append(f"{n}_{type}{i}")
# test = [1 for _ in range(84)]

df = pd.DataFrame(columns=main)
# df = pd.DataFrame([test])
df.to_csv("data/main.csv", mode="w", index=False, header=True)
