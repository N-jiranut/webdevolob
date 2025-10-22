import pandas as pd

test = pd.read_csv("data/main.csv", encoding="TIS-620")
print(test["label"].value_counts())