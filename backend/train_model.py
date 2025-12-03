import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import pickle
import os

def load_and_process_data():
    print("Loading NHANES datasets...")
    
    # Define paths (assuming files are in the 'data' folder next to 'backend')
    base_path = os.path.join(os.path.dirname(__file__), '..', 'data')
    
    # Load the CSVs
    # Using 'SEQN' as the index since it's the unique ID for participants
    demo_df = pd.read_csv(os.path.join(base_path, 'demographic.csv')).set_index('SEQN')
    exam_df = pd.read_csv(os.path.join(base_path, 'examination.csv')).set_index('SEQN')
    labs_df = pd.read_csv(os.path.join(base_path, 'labs.csv')).set_index('SEQN')
    
    # We merge them into one big table
    print("Merging datasets...")
    df = demo_df.join([exam_df, labs_df], how='inner')
    
    # --- Feature Engineering ---
    
    # 1. Rename columns to be human-readable
    # RIAGENDR: 1=Male, 2=Female
    # RIDAGEYR: Age in years
    # BMXWT: Weight (kg)
    # BMXHT: Height (cm)
    # LBXHGB: Hemoglobin (g/dL) - Main indicator for Anemia/Iron Deficiency
    # LBXSCH: Total Cholesterol (mg/dL) - Indicator for poor diet/heart risk
    
    keep_cols = ['RIAGENDR', 'RIDAGEYR', 'BMXWT', 'BMXHT', 'LBXHGB', 'LBXSCH']
    df = df[keep_cols].copy()
    
    # 2. Drop rows with missing values in these critical columns
    df.dropna(inplace=True)
    
    # 3. Process Inputs (X)
    # Convert Gender to 0=Male, 1=Female (Original: 1=Male, 2=Female)
    df['gender'] = df['RIAGENDR'].apply(lambda x: 0 if x == 1 else 1)
    
    # Calculate BMI: Weight(kg) / (Height(m)^2)
    # Height is in cm, so divide by 100
    df['bmi'] = df['BMXWT'] / ((df['BMXHT'] / 100) ** 2)
    
    # 4. Define Targets (Y) - The "Deficiency" Label
    # We will categorize patients based on real medical thresholds
    # Label 0: Healthy
    # Label 1: Anemia (Iron Deficiency)
    # Label 2: High Cholesterol (Risk)
    
    def classify_patient(row):
        # Anemia Thresholds (WHO): Men < 13.0, Women < 12.0
        is_female = row['gender'] == 1
        hb = row['LBXHGB']
        
        if (is_female and hb < 12.0) or (not is_female and hb < 13.0):
            return 1 # Anemia / Iron Deficiency
            
        # High Cholesterol > 240 mg/dL
        if row['LBXSCH'] > 240:
            return 2 # High Cholesterol / Diet Risk
            
        return 0 # Healthy / Low Risk

    df['deficiency_label'] = df.apply(classify_patient, axis=1)
    
    # Final Selection
    X = df[['RIDAGEYR', 'gender', 'bmi']] # Features: Age, Gender, BMI
    y = df['deficiency_label']            # Target: Calculated Label
    
    print(f"Processed data: {len(df)} samples.")
    print("Class distribution:\n", y.value_counts())
    
    return X, y

def train():
    X, y = load_and_process_data()
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale features (Age and BMI have vastly different ranges)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train Model (RandomForest is robust for tabular medical data)
    print("Training Random Forest Classifier...")
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train_scaled, y_train)
    
    # Evaluate
    accuracy = clf.score(X_test_scaled, y_test)
    print(f"Model Accuracy: {accuracy * 100:.2f}%")
    
    # Save Model and Scaler
    # We need to save the scaler too, to scale user input later!
    with open('model.pkl', 'wb') as f:
        pickle.dump({'model': clf, 'scaler': scaler}, f)
    
    print("Model and scaler saved to model.pkl")

if __name__ == "__main__":
    train()