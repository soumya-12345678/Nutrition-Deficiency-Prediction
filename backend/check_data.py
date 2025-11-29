import os
import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.abspath(os.path.join(current_dir, ".."))
data_path = os.path.join(project_dir, "data", "nutrition_data.csv")

df = pd.read_csv(data_path)
print(df["deficiency_label"].value_counts().sort_index())
