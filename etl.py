import pandas as pd
import numpy as np
import sqlite3
import os
from datetime import datetime, timedelta
import random

# Configuration
DB_PATH = 'backend/data/superstore_enhanced.db'
NUM_ROWS = 50000
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2025, 12, 31)

def generate_data():
    print("Generating synthetic data...")
    
    # Dimensions
    regions = ['North', 'South', 'East', 'West', 'Central']
    categories = ['Furniture', 'Office Supplies', 'Technology']
    sub_categories = {
        'Furniture': ['Bookcases', 'Chairs', 'Tables', 'Furnishings'],
        'Office Supplies': ['Labels', 'Storage', 'Art', 'Binders', 'Appliances', 'Paper', 'Fasteners', 'Envelopes', 'Supplies'],
        'Technology': ['Phones', 'Accessories', 'Machines', 'Copiers']
    }
    segments = ['Consumer', 'Corporate', 'Home Office']
    ship_modes = ['Standard Class', 'Second Class', 'First Class', 'Same Day']
    
    # Generate Dates
    date_range = (END_DATE - START_DATE).days
    dates = [START_DATE + timedelta(days=random.randint(0, date_range)) for _ in range(NUM_ROWS)]
    
    # Generate Core Data
    data = {
        'Order_Date': dates,
        'Region': np.random.choice(regions, NUM_ROWS),
        'Segment': np.random.choice(segments, NUM_ROWS),
        'Ship_Mode': np.random.choice(ship_modes, NUM_ROWS),
        'Category': np.random.choice(categories, NUM_ROWS),
    }
    
    df = pd.DataFrame(data)
    
    # Dependent Columns
    df['Sub_Category'] = df['Category'].apply(lambda x: np.random.choice(sub_categories[x]))
    df['Sales'] = np.random.lognormal(mean=4.5, sigma=1.2, size=NUM_ROWS).round(2)
    df['Quantity'] = np.random.randint(1, 15, size=NUM_ROWS)
    df['Discount'] = np.random.choice([0, 0.1, 0.2, 0.3, 0.4, 0.5], size=NUM_ROWS, p=[0.5, 0.2, 0.15, 0.1, 0.03, 0.02])
    df['Profit'] = (df['Sales'] * np.random.uniform(-0.2, 0.4, size=NUM_ROWS)).round(2)
    
    # Enhanced Columns
    df['Weather_Index'] = np.random.uniform(0, 100, size=NUM_ROWS).round(1) # 0=Bad, 100=Good
    df['Supplier_Reliability'] = np.random.uniform(70, 100, size=NUM_ROWS).round(1)
    df['Lead_Time_Days'] = np.random.randint(1, 14, size=NUM_ROWS)
    df['Is_Promo'] = np.random.choice([0, 1], size=NUM_ROWS, p=[0.8, 0.2])
    df['Customer_ID'] = np.random.randint(1000, 5000, size=NUM_ROWS)
    df['Store_ID'] = np.random.randint(1, 50, size=NUM_ROWS)
    
    # Adjust Sales/Profit based on factors
    # Promo increases sales but decreases margin
    df.loc[df['Is_Promo'] == 1, 'Sales'] *= 1.2
    df.loc[df['Is_Promo'] == 1, 'Profit'] *= 0.8
    
    # Bad weather decreases sales for some categories
    mask_weather = (df['Weather_Index'] < 30) & (df['Category'].isin(['Furniture']))
    df.loc[mask_weather, 'Sales'] *= 0.7
    
    print(f"Generated {len(df)} rows.")
    return df

def load_to_db(df):
    print(f"Loading data to {DB_PATH}...")
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    
    # Main Table
    df.to_sql('orders', conn, if_exists='replace', index=False)
    
    # Create Indices
    conn.execute('CREATE INDEX IF NOT EXISTS idx_order_date ON orders(Order_Date)')
    conn.execute('CREATE INDEX IF NOT EXISTS idx_region ON orders(Region)')
    conn.execute('CREATE INDEX IF NOT EXISTS idx_category ON orders(Category)')
    
    # Create Summary Tables for Performance
    print("Creating summary tables...")
    
    # Monthly Sales
    conn.execute('''
        CREATE TABLE IF NOT EXISTS monthly_sales AS
        SELECT strftime('%Y-%m', Order_Date) as Month, Sum(Sales) as Total_Sales, Sum(Profit) as Total_Profit
        FROM orders
        GROUP BY 1
    ''')
    
    conn.close()
    print("Database populated successfully.")

if __name__ == "__main__":
    df = generate_data()
    load_to_db(df)
