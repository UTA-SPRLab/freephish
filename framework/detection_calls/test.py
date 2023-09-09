import pandas as pd
from joblib import load

def predict_parser():
    try:
        # Load the trained model
        xgb_model = load('model.pkl')
        
        # Load the features from the CSV file
        df = pd.read_csv('parsed_metadata/features.csv')
        
        # Initialize an empty list to keep track of IDs for which predictions have been made
        predicted_ids = []
        
        # Loop through each row and make a prediction if 'label' is neither 'true' nor 'false'
        for index, row in df.iterrows():
            # Skip rows with IDs that have already been predicted
            if row['id'] in predicted_ids:
                continue
            
            if row['label'] not in ['true', 'false']:
                # Drop the columns that are not features, use 'loc' to get a single row DataFrame
                x_test = df.loc[[index]].drop(columns=['url', 'id', 'label', 'another_unwanted_column'])
                
                # Make a prediction for that row
                y_pred = xgb_model.predict(x_test)
                
                # Update the 'label' column with the prediction
                df.at[index, 'label'] = 'true' if y_pred[0] == 1 else 'false'
                
                # Add the ID to the list of predicted IDs
                predicted_ids.append(row['id'])
                
        # Save the updated DataFrame back to the CSV file
        df.to_csv('parsed_metadata/features.csv', index=False)
        
        print("Predictions updated.")
        return True  # Return True if everything is successful
    except Exception as e:
        print(f"An error occurred: {e}")
        return False  # Return False if an exception is raised

# Example usage
if predict_parser():
    print("Prediction successful.")
else:
    print("Prediction failed.")
