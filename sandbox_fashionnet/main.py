import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load datasets
product_data = pd.read_csv("../archive/product_data.csv")
attribute_data = pd.read_csv("../archive/attribute_data.csv")

# Merge datasets
data = pd.merge(product_data, attribute_data, on="cod_modelo_color", how="left")

# Handle missing attributes by setting them to "INVALID"
data['des_value'] = data['des_value'].fillna("INVALID")

# Remove classes with fewer than 2 instances
class_counts = data['des_value'].value_counts()
valid_classes = class_counts[class_counts >= 2].index
data = data[data['des_value'].isin(valid_classes)]

# Split dataset into features and target
X = data.drop(columns=['des_value'])
y = data['des_value']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# Frequency encode categorical columns
for col in X_train.select_dtypes(include='object').columns:
    freq = X_train[col].value_counts(normalize=True)
    X_train[col] = X_train[col].map(freq)
    X_test[col] = X_test[col].map(freq).fillna(0)

# Train a Random Forest classifier
clf = RandomForestClassifier(random_state=42)
clf.fit(X_train, y_train)

# Evaluate the model
y_pred = clf.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
