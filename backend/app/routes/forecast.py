from flask import Blueprint, jsonify, request
import pickle
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

forecast_bp = Blueprint('forecast', __name__)

MODEL_PATH = 'backend/static/models/demand_model.pkl'
ENCODER_PATH = 'backend/static/models/encoders.pkl'

model = None
encoders = None

def load_model():
    global model, encoders
    if model is None and os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
    if encoders is None and os.path.exists(ENCODER_PATH):
        with open(ENCODER_PATH, 'rb') as f:
            encoders = pickle.load(f)

@forecast_bp.route('/demand-forecast', methods=['GET'])
def get_forecast():
    load_model()
    if not model:
        return jsonify({'error': 'Model not trained'}), 503
        
    # Parameters
    region = request.args.get('region', 'North')
    category = request.args.get('category', 'Furniture')
    sub_category = request.args.get('sub_category', 'Chairs')
    days = int(request.args.get('days', 30))
    
    # Generate future dates
    start_date = datetime.now()
    dates = [start_date + timedelta(days=i) for i in range(days)]
    
    # Prepare input dataframe
    future_df = pd.DataFrame({
        'Order_Date': dates,
        'Region': [region] * days,
        'Category': [category] * days,
        'Sub_Category': [sub_category] * days,
        'Discount': [0.1] * days, # Assumption
        'Weather_Index': [80] * days, # Assumption
        'Is_Promo': [0] * days # Assumption
    })
    
    # Feature Engineering
    future_df['Month'] = future_df['Order_Date'].dt.month
    future_df['DayOfWeek'] = future_df['Order_Date'].dt.dayofweek
    future_df['Year'] = future_df['Order_Date'].dt.year
    
    # Encode
    try:
        future_df['Region_Encoded'] = encoders['region'].transform(future_df['Region'])
        future_df['Category_Encoded'] = encoders['category'].transform(future_df['Category'])
        future_df['Sub_Category_Encoded'] = encoders['subcategory'].transform(future_df['Sub_Category'])
    except ValueError:
        return jsonify({'error': 'Invalid category or region'}), 400
        
    X = future_df[['Month', 'DayOfWeek', 'Year', 'Region_Encoded', 'Category_Encoded', 'Sub_Category_Encoded', 'Discount', 'Weather_Index', 'Is_Promo']]
    
    # Predict
    predictions = model.predict(X)
    
    # Format response
    result = []
    for date, pred in zip(dates, predictions):
        result.append({
            'date': date.strftime('%Y-%m-%d'),
            'forecast': max(0, round(float(pred), 1)), # No negative demand
            'lower_ci': max(0, round(float(pred) * 0.8, 1)),
            'upper_ci': round(float(pred) * 1.2, 1)
        })
        
    return jsonify(result)
