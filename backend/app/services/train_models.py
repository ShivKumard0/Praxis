import pandas as pd
import numpy as np
import sqlite3
import pickle
import os
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Config
DB_PATH = 'backend/data/superstore_enhanced.db'
MODEL_DIR = 'backend/static/models'
os.makedirs(MODEL_DIR, exist_ok=True)

def load_data():
    conn = sqlite3.connect(DB_PATH)
    query = """
        SELECT 
            Order_Date, Region, Category, Sub_Category, Sales, Quantity, Discount, Profit,
            Weather_Index, Is_Promo, Holiday_Flag
        FROM orders
    """
    # Note: Holiday_Flag might not exist in my ETL, let's check. 
    # Actually I didn't add Holiday_Flag in ETL. I added Weather_Index, Is_Promo.
    # Let's adjust query.
    query = """
        SELECT 
            Order_Date, Region, Category, Sub_Category, Sales, Quantity, Discount, Profit,
            Weather_Index, Is_Promo
        FROM orders
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def train_demand_model():
    print("Training Demand Forecast Model (XGBoost)...")
    df = load_data()
    
    # Feature Engineering
    df['Order_Date'] = pd.to_datetime(df['Order_Date'])
    df['Month'] = df['Order_Date'].dt.month
    df['DayOfWeek'] = df['Order_Date'].dt.dayofweek
    df['Year'] = df['Order_Date'].dt.year
    
    # Encode Categoricals
    le_region = LabelEncoder()
    df['Region_Encoded'] = le_region.fit_transform(df['Region'])
    
    le_category = LabelEncoder()
    df['Category_Encoded'] = le_category.fit_transform(df['Category'])
    
    le_subcategory = LabelEncoder()
    df['Sub_Category_Encoded'] = le_subcategory.fit_transform(df['Sub_Category'])
    
    # Features & Target
    X = df[['Month', 'DayOfWeek', 'Year', 'Region_Encoded', 'Category_Encoded', 'Sub_Category_Encoded', 'Discount', 'Weather_Index', 'Is_Promo']]
    y = df['Quantity'] # Forecasting Demand (Quantity)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=5)
    model.fit(X_train, y_train)
    
    score = model.score(X_test, y_test)
    print(f"Model R2 Score: {score:.4f}")
    
    # Save Model & Encoders
    with open(f'{MODEL_DIR}/demand_model.pkl', 'wb') as f:
        pickle.dump(model, f)
        
    with open(f'{MODEL_DIR}/encoders.pkl', 'wb') as f:
        pickle.dump({
            'region': le_region,
            'category': le_category,
            'subcategory': le_subcategory
        }, f)
        
    print("Model saved.")

if __name__ == "__main__":
    train_demand_model()
