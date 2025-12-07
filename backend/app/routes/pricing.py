from flask import Blueprint, jsonify, request
import numpy as np
from sklearn.linear_model import LinearRegression
from ..utils.db import query_db

pricing_bp = Blueprint('pricing', __name__)

@pricing_bp.route('/pricing-elasticity', methods=['GET'])
def get_pricing_elasticity():
    # Calculate Price Elasticity of Demand (PED)
    # PED = % Change in Quantity / % Change in Price
    
    # Fetch historical price/quantity data
    data = query_db("""
        SELECT Sales/Quantity as Price, Quantity
        FROM orders
        WHERE Quantity > 0 AND Sales > 0
        LIMIT 1000
    """)
    
    prices = np.array([row['Price'] for row in data]).reshape(-1, 1)
    quantities = np.array([row['Quantity'] for row in data])
    
    # Train simple Linear Regression on the fly (fast enough for 1000 rows)
    model = LinearRegression()
    model.fit(prices, quantities)
    
    slope = model.coef_[0]
    intercept = model.intercept_
    
    # Generate Demand Curve points
    price_range = np.linspace(min(prices), max(prices), 20)
    demand_curve = []
    
    for p in price_range:
        q = slope * p + intercept
        elasticity = slope * (p / q) if q != 0 else 0
        demand_curve.append({
            'price': round(float(p), 2),
            'predicted_quantity': max(0, round(float(q), 1)),
            'elasticity': round(float(elasticity), 2)
        })
        
    return jsonify({
        'slope': round(float(slope), 4),
        'intercept': round(float(intercept), 2),
        'demand_curve': demand_curve,
        'recommendation': 'Decrease price' if slope < -0.5 else 'Maintain price'
    })
