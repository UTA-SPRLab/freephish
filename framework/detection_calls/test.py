import pandas as pd
from joblib import load

def predict_parser():
    try:
        xgb_model = load('model.pkl')
        
        # Load the features from the CSV file
        df = pd.read_csv('parsed_metadata/features.csv')
        
        # Track IDs for which predictions have been made
        predicted_ids = []
        
        for index, row in df.iterrows():
            # Skip rows with IDs that have already been predicted
            if row['id'] in predicted_ids:
                continue
            
            if row['label'] not in ['true', 'false']:
                x_test = df.loc[[index]].drop(columns=['url', 'id', 'label', 'another_unwanted_column'])
                
                y_pred = xgb_model.predict(x_test)
                
                # Update the 'label' column with the prediction
                df.at[index, 'label'] = 'true' if y_pred[0] == 1 else 'false'
                
                # Add the ID to the list of predicted IDs
                predicted_ids.append(row['id'])
                
        df.to_csv('parsed_metadata/features.csv', index=False)
        
        print("Predictions updated.")
        return True  # Return True if everything is successful
    except Exception as e:
        print(f"An error occurred: {e}")
        return False  # Return False if an exception is raised

