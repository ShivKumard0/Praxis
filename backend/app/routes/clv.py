from flask import Blueprint, jsonify
from sklearn.cluster import KMeans
from ..utils.db import query_db
import pandas as pd

clv_bp = Blueprint('clv', __name__)

@clv_bp.route('/clv-churn', methods=['GET'])
def get_clv_churn():
    # RFM Analysis (Recency, Frequency, Monetary)
    
    # Fetch customer data
    data = query_db("""
        SELECT 
            Customer_ID,
            MAX(Order_Date) as Last_Order,
            COUNT(DISTINCT Order_Date) as Frequency,
            SUM(Sales) as Monetary
        FROM orders
        GROUP BY 1
        LIMIT 2000
    """)
    
    if not data:
        return jsonify([])
        
    df = pd.DataFrame(data, columns=['Customer_ID', 'Last_Order', 'Frequency', 'Monetary'])
    df['Last_Order'] = pd.to_datetime(df['Last_Order'])
    now = df['Last_Order'].max()
    df['Recency'] = (now - df['Last_Order']).dt.days
    
    # Simple Segmentation using Quantiles (or KMeans if we had more time/data complexity)
    # For this demo, let's use simple logic for "Churn Risk"
    
    # High Risk: High Recency (haven't bought in a while)
    # High Value: High Monetary
    
    df['Churn_Risk'] = df['Recency'].apply(lambda x: 'High' if x > 365 else ('Medium' if x > 180 else 'Low'))
    df['Customer_Value'] = pd.qcut(df['Monetary'], 3, labels=['Low', 'Medium', 'High'])
    
    # Aggregate for Heatmap
    heatmap = df.groupby(['Churn_Risk', 'Customer_Value']).size().reset_index(name='count')
    
    # Format for frontend
    segments = []
    for _, row in heatmap.iterrows():
        segments.append({
            'churn_risk': row['Churn_Risk'],
            'value_segment': row['Customer_Value'],
            'count': int(row['count'])
        })
        
    return jsonify({
        'segments': segments,
        'total_customers': len(df),
        'avg_clv': round(df['Monetary'].mean(), 2)
    })
