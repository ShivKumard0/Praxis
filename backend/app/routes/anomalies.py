from flask import Blueprint, jsonify
from sklearn.ensemble import IsolationForest
from ..utils.db import query_db
import pandas as pd
import numpy as np

anomalies_bp = Blueprint('anomalies', __name__)

@anomalies_bp.route('/anomaly-alerts', methods=['GET'])
def get_anomalies():
    # Detect anomalies in Daily Sales
    
    data = query_db("""
        SELECT Order_Date, SUM(Sales) as Sales
        FROM orders
        GROUP BY 1
        ORDER BY 1
    """)
    
    df = pd.DataFrame(data, columns=['Order_Date', 'Sales'])
    
    model = IsolationForest(contamination=0.05, random_state=42)
    df['Anomaly'] = model.fit_predict(df[['Sales']])
    
    # -1 is anomaly, 1 is normal
    anomalies = df[df['Anomaly'] == -1].copy()
    
    results = []
    for _, row in anomalies.iterrows():
        results.append({
            'date': row['Order_Date'],
            'value': row['Sales'],
            'type': 'Sales Spike/Drop',
            'severity': 'High'
        })
        
    return jsonify(results)
