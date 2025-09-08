import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from tensorflow.keras.models import load_model
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder
from matplotlib import rcParams
rcParams['font.family'] = 'TH Sarabun New'
name = "M9-3-2025-Uan"
model = load_model(f"ML-model/{name}/model.h5")
with open(f"ML-model/{name}/text.txt", "r", encoding="utf-8") as f:
    class_names = f.read().splitlines()
# โหลดข้อมูล
df = pd.read_csv("data/main.csv", encoding="utf-8")

# แยก features และ label
X = df.drop("label", axis=1)
y = df.iloc[:, -1].values  
test=[]
# ทำนาย
y_pred = model.predict(X)
predicted_index = np.argmax(y_pred, axis=1)
for id in predicted_index:
    test.append(class_names[id])

# ทำ confusion matrix
cm = confusion_matrix(y, test)
print(cm)
# วาด confusion matrix
plt.figure(figsize=(8,6))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=class_names, yticklabels=class_names)
plt.xlabel("Predicted")
plt.ylabel("True")
plt.title("Confusion Matrix")
plt.show()
