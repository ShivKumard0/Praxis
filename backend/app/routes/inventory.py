from flask import Blueprint, jsonify, request
import pulp
from ..utils.db import query_db

inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('/inventory-optimize', methods=['GET'])
def optimize_inventory():
    # Simplified Multi-Echelon Inventory Optimization
    # Minimize Total Cost = Holding Cost + Ordering Cost + Shortage Cost
    # Subject to: Service Level > 95%
    
    # Mock Data for Optimization
    # In real app, fetch from DB
    warehouses = ['WH_North', 'WH_South', 'WH_East', 'WH_West']
    stores = [f'Store_{i}' for i in range(1, 11)]
    
    demand = {s: 100 for s in stores} # Avg daily demand
    holding_cost = 0.5 # per unit per day
    ordering_cost = 50 # per order
    capacity = {w: 5000 for w in warehouses}
    
    # Create Problem
    prob = pulp.LpProblem("Inventory_Optimization", pulp.LpMinimize)
    
    # Variables
    # x[w][s] = amount shipped from warehouse w to store s
    x = pulp.LpVariable.dicts("ship", (warehouses, stores), lowBound=0, cat='Integer')
    
    # Objective Function: Minimize Transport Cost (proxy for total cost here)
    # Cost matrix (mock)
    costs = {}
    for w in warehouses:
        costs[w] = {}
        for s in stores:
            costs[w][s] = 2 if w.split('_')[1] in s else 5 # Cheaper if same region (mock logic)
            
    prob += pulp.lpSum([x[w][s] * costs[w][s] for w in warehouses for s in stores])
    
    # Constraints
    # 1. Demand Satisfaction
    for s in stores:
        prob += pulp.lpSum([x[w][s] for w in warehouses]) >= demand[s]
        
    # 2. Warehouse Capacity
    for w in warehouses:
        prob += pulp.lpSum([x[w][s] for s in stores]) <= capacity[w]
        
    # Solve
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    
    # Format Result
    network_flow = []
    for w in warehouses:
        for s in stores:
            val = x[w][s].varValue
            if val > 0:
                network_flow.append({
                    'source': w,
                    'target': s,
                    'value': val
                })
                
    return jsonify({
        'status': pulp.LpStatus[prob.status],
        'total_cost': pulp.value(prob.objective),
        'network_flow': network_flow,
        'service_level': '98.5%' # Mocked derived metric
    })
