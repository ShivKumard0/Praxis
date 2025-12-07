from flask import Blueprint, jsonify, request
from ..utils.db import query_db

kpis_bp = Blueprint('kpis', __name__)

@kpis_bp.route('/kpis', methods=['GET'])
def get_kpis():
    # Get filters from query params
    start_date = request.args.get('start_date', '2023-01-01')
    end_date = request.args.get('end_date', '2025-12-31')
    region = request.args.get('region')
    
    query = """
        SELECT 
            SUM(Sales) as total_sales,
            SUM(Profit) as total_profit,
            SUM(Quantity) as total_volume,
            AVG(Discount) as avg_discount,
            COUNT(DISTINCT Order_Date) as days_active
        FROM orders
        WHERE Order_Date BETWEEN ? AND ?
    """
    params = [start_date, end_date]
    
    if region and region != 'All':
        query += " AND Region = ?"
        params.append(region)
        
    result = query_db(query, params, one=True)
    
    # Calculate derived metrics
    margin = (result['total_profit'] / result['total_sales'] * 100) if result['total_sales'] else 0
    
    return jsonify({
        'revenue': round(result['total_sales'] or 0, 2),
        'profit': round(result['total_profit'] or 0, 2),
        'margin': round(margin, 1),
        'volume': result['total_volume'] or 0
    })
