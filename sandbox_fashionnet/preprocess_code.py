import pandas as pd
from sklearn.model_selection import train_test_split

# Load datasets
product_data = pd.read_csv("../archive/product_data.csv")
attribute_data = pd.read_csv("../archive/attribute_data.csv")

# Merge datasets
data = pd.merge(product_data, attribute_data, on="cod_modelo_color", how="left")

# Handle missing attributes by setting them to "INVALID"
data['des_value'] = data['des_value'].fillna("INVALID")

# Identify and remove classes with fewer than 2 instances
class_counts = data['des_value'].value_counts()
valid_classes = class_counts[class_counts >= 2].index  # Only keep classes with at least 2 instances
data = data[data['des_value'].isin(valid_classes)]

# Verify the remaining class distribution
print("Class distribution after removing single-instance classes:")
print(data['des_value'].value_counts())

# Perform stratified train-test split
train_df, valid_df = train_test_split(data, test_size=0.2, stratify=data['des_value'], random_state=42)

# Verify split sizes
print(f"Training set size: {len(train_df)}")
print(f"Validation set size: {len(valid_df)}")
