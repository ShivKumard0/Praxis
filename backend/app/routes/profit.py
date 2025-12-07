from flask import Blueprint, jsonify, request
from ..utils.db import query_db

profit_bp = Blueprint('profit', __name__)

@profit_bp.route('/profit-diagnostic', methods=['GET'])
def get_profit_diagnostic():
    start_date = request.args.get('start_date', '2023-01-01')
    end_date = request.args.get('end_date', '2025-12-31')
    
    # Waterfall Chart Data (Simplified)
    # Revenue -> COGS -> Discounts -> Promo Cost -> Net Profit
    
    totals = query_db("""
        SELECT 
            SUM(Sales) as Revenue,
            SUM(Sales) * 0.6 as COGS, -- Approx 60% COGS
            SUM(Sales * Discount) as Discounts,
            SUM(CASE WHEN Is_Promo = 1 THEN Sales * 0.1 ELSE 0 END) as Promo_Cost,
            SUM(Profit) as Net_Profit
        FROM orders
        WHERE Order_Date BETWEEN ? AND ?
    """, [start_date, end_date], one=True)
    
    waterfall = [
        {'label': 'Gross Revenue', 'value': totals['Revenue'], 'type': 'positive'},
        {'label': 'COGS', 'value': -totals['COGS'], 'type': 'negative'},
        {'label': 'Discounts', 'value': -totals['Discounts'], 'type': 'negative'},
        {'label': 'Promo Impact', 'value': -totals['Promo_Cost'], 'type': 'negative'},
        {'label': 'Net Profit', 'value': totals['Net_Profit'], 'type': 'total'}
    ]
    
    # Pareto Analysis (80/20 Rule) by Sub-Category
    pareto_data = query_db("""
        SELECT 
            Sub_Category,
            SUM(Profit) as Profit
        FROM orders
        WHERE Order_Date BETWEEN ? AND ?
        GROUP BY 1
        ORDER BY Profit DESC
    """, [start_date, end_date])
    
    pareto = []
    cumulative_profit = 0
    total_profit = totals['Net_Profit'] or 1
    
    for row in pareto_data:
        cumulative_profit += row['Profit']
        pareto.append({
            'category': row['Sub_Category'],
            'profit': row['Profit'],
            'cumulative_percentage': round((cumulative_profit / total_profit) * 100, 1)
        })
        
    return jsonify({
        'waterfall': waterfall,
        'pareto': pareto
    })
