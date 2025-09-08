import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams
rcParams['font.family'] = 'TH Sarabun New'
name = "M9-3-2025-Uan"
with open(f"ML-model/{name}/text.txt", "r", encoding="utf-8") as f:
    class_names = f.read().splitlines()

cm = [[  0,  8,  0,  2,  0],
 [   0,  0, 10,  0,  0],
 [  11,  0,  1,  0,  8],
 [   0,  2,  0,  8,  0],
 [   0,  0,  0,  0,  0],
 ]
plt.figure(figsize=(8,6))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=class_names, yticklabels=class_names)
plt.xlabel("Predicted")
plt.ylabel("True")
plt.title("Confusion Matrix")
plt.show()
