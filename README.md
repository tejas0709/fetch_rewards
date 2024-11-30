
# Points Management System

This is a Points Management System implemented using **Flask** (Python) for the backend. The system allows users to manage points transactions, spend points, and check their balance.

## Features

- **Add Points**: Add points for a specific payer.
- **Spend Points**: Spend points from the available balance in the order of the oldest transactions.
- **Get Balance**: Retrieve the current point balance for each payer.
- **Clear Data**: Reset all data (transactions and balances) to start fresh.

## Requirements

- Python 3.x
- Flask (Python web framework)

## Optional(If you don't want to test it using frontend)
- Axios (for making HTTP requests in the frontend)
- Bootstrap 5 (for styling)

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/tejas0708/fetch_rewards.git
   cd fetch_rewards
   ```

2. **Install dependencies:**
   Install Flask and any necessary packages using pip.
   ```bash
   pip install flask
   ```

3. **Run the Flask app:**
   Start the Flask development server.
   ```bash
   python app.py
   ```

   The server will run on `http://127.0.0.1:8000`.

## Usage

1. **Navigate to the app in your browser:**
   Open your browser and visit `http://127.0.0.1:8000` to access the Points Management System.

2. **Add Points:**
   - Enter a JSON object in the "Add Points" text area to add points for a specific payer.
   - Example JSON:
     ```json
     {
       "payer": "DANNON",
       "points": 300,
       "timestamp": "2022-10-31T10:00:00Z"
     }
     ```

3. **Spend Points:**
   - Enter the number of points you wish to spend in the "Spend Points" text area.
   - Example JSON:
     ```json
     {
       "points": 5000
     }
     ```

4. **Get Current Balance:**
   - Click the "Get Current Balance" button to retrieve the current point balance by payer.

5. **Clear Data:**
   - Click the "Clear Data" button in the top-left corner to reset all transactions and balances to start fresh.

## API Endpoints

1. **`POST /add`**:
   - Adds points to a payer's balance.
   - **Request body** (JSON):
     ```json
     {
       "payer": "DANNON",
       "points": 300,
       "timestamp": "2022-10-31T10:00:00Z"
     }
     ```
   - **Response**: `200 OK` on success, `400` if the transaction is invalid (e.g., points can't be negative).

2. **`POST /spend`**:
   - Spend points based on the oldest transactions.
   - **Request body** (JSON):
     ```json
     {
       "points": 5000
     }
     ```
   - **Response**: List of payers and the points subtracted.
     Example:
     ```json
     [
       {"payer": "DANNON", "points": -100},
       {"payer": "UNILEVER", "points": -200},
       {"payer": "MILLER COORS", "points": -4700}
     ]
     ```

3. **`GET /balance`**:
   - Get the current points balance by payer.
   - **Response** (JSON):
     ```json
     {
       "DANNON": 1000,
       "UNILEVER": 0,
       "MILLER COORS": 5300
     }
     ```

4. **`POST /reset`**:
   - Clears all stored data (transactions and balances).
   - **Response**: `200 OK` on success.

## Testing

You can test the system by adding sample data through the "Add Points" and "Spend Points" sections. Use the "Clear Data" button to reset the system at any time. You can also test the API endpoints by using **Postman** or **curl**.

Example of a `curl` request to add points:
```bash
curl -X POST http://127.0.0.1:8000/add -H "Content-Type: application/json" -d '{"payer": "DANNON", "points": 5000, "timestamp": "2022-11-02T14:00:00Z"}'
```