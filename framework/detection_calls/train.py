import xgboost as xgb
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import confusion_matrix, accuracy_score
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('parsed_metadata/features.csv')

# Separate features and label dataframes

y = df['label']  # 'label' column indicates whether the URL is phishing or benign
x = df.drop(columns=['url', 'id'])  # Columns not needed

# Split data into training and validation sets
x_train, x_val, y_train, y_val = train_test_split(x, y, test_size=0.2, random_state=42)

print(f"Training set length: {len(x_train)}")
print(f"Number of phishing instances in training set: {list(y_train).count('phishing')}")

# Initialize and fit the XGBoost model
xgb_model = xgb.XGBClassifier()
xgb_model.fit(x_train, y_train)

# Save the model
joblib.dump(xgb_model, 'model.pkl')

# Make predictions and evaluate the model
y_pred = xgb_model.predict(x_val)
print(confusion_matrix(y_val, y_pred))
print(accuracy_score(y_val, y_pred))

# Plot feature importance
#xgb.plot_importance(xgb_model)
#plt.show()

