from flask import Flask, request, jsonify, render_template
from datetime import datetime
import heapq

app = Flask(__name__)

# In-memory storage for transactions and balances
transactions = []
balances = {}

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_points():
    """Add points for a specific payer."""
    data = request.json
    payer = data['payer']
    points = data['points']
    
    # Check if adding points goes below zero for the payer
    new_balance = balances.get(payer, 0) + points
    if new_balance < 0:
        return jsonify({"error": "Insufficient balance after transaction"}), 400
    
    # Convert timestamp to datetime
    timestamp = datetime.fromisoformat(data['timestamp'].replace('Z', '+00:00'))
    
    # Add to transactions heap
    heapq.heappush(transactions, (timestamp, payer, points))
    
    # Update payer balance
    balances[payer] = new_balance
    
    return '', 200

@app.route('/spend', methods=['POST'])
def spend_points():
    """Spend points according to the oldest transactions."""
    global transactions, balances

    points_to_spend = request.json['points']

    # Check total points available
    total_points = sum(balances.values())
    if points_to_spend > total_points:
        return "Not enough points", 400

    spent = {}
    updated_transactions = []

    while points_to_spend > 0:
        # Get the oldest transaction
        if not transactions:
            break
        timestamp, payer, points = heapq.heappop(transactions)

        # Skip if no balance for the payer
        if balances[payer] <= 0:
            continue

        # Determine points to deduct
        points_to_deduct = min(points, points_to_spend)

        # Update balances and remaining points
        balances[payer] -= points_to_deduct
        points_to_spend -= points_to_deduct

        # Aggregate spending for each payer
        if payer in spent:
            spent[payer] -= points_to_deduct
        else:
            spent[payer] = -points_to_deduct

        # If transaction has leftover points, re-add it
        if points > points_to_deduct:
            updated_transactions.append((timestamp, payer, points - points_to_deduct))

    # Add unspent transactions back into the heap
    for transaction in updated_transactions:
        heapq.heappush(transactions, transaction)

    # Convert aggregated spending to a list
    result = [{"payer": payer, "points": points} for payer, points in spent.items()]

    return jsonify(result), 200


@app.route('/balance', methods=['GET'])
def get_balance():
    """Retrieve current point balances."""
    return jsonify(balances), 200

@app.route('/reset', methods=['POST'])
def reset_data():
    """Clear all transactions and balances to start fresh."""
    global transactions, balances
    transactions = []  # Reset transactions
    balances = {}      # Reset balances
    return '', 200  # Return a success response

if __name__ == '__main__':
    app.run(debug=True, port=8000)