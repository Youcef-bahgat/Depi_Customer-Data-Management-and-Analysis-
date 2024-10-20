
from flask import Flask, request, jsonify
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import datetime

# Initialize the Flask application
app = Flask(__name__)

# Load your monthly sales data
monthly_sales = pd.read_csv('monthly_sales.csv')

# Ensure that the 'transaction_date' column is parsed as a datetime
monthly_sales['transaction_date'] = pd.to_datetime(monthly_sales['transaction_date'])

# Set 'transaction_date' as the DataFrame index
monthly_sales.set_index('transaction_date', inplace=True)

# Ensure that 'total_sales' is numeric (remove non-numeric values if necessary)
monthly_sales['total_sales'] = pd.to_numeric(monthly_sales['total_sales'], errors='coerce')

# Drop any rows with missing data
monthly_sales.dropna(inplace=True)

# Train the ARIMA model on the 'total_sales' column
model = ARIMA(monthly_sales['total_sales'], order=(5, 1, 0))
model_fit = model.fit()

# Route to forecast sales for a specific date
@app.route('/forecast', methods=['GET'])
def forecast_sales():
    try:
        # Get the date from query params (e.g., "date=2024-06-30")
        forecast_date = request.args.get('date')
        forecast_date = pd.to_datetime(forecast_date).date()  # Parse the date

        # Get the last date in the historical data
        last_historical_date = monthly_sales.index[-1].date()

        # Ensure the forecast date is in the future
        if forecast_date <= last_historical_date:
            return jsonify({"error": "The date must be in the future. Provide a future date."}), 400

        # Calculate how many months into the future the requested date is
        months_ahead = (forecast_date.year - last_historical_date.year) * 12 + (forecast_date.month - last_historical_date.month)

        if months_ahead <= 0:
            return jsonify({"error": "Invalid date range. Date must be after the last historical date."}), 400

        # Forecast future values up to the requested date
        forecast = model_fit.forecast(steps=months_ahead)

        # Create a date range for the forecasted values
        forecast_dates = pd.date_range(start=last_historical_date + pd.DateOffset(1), periods=months_ahead, freq='M')

        # Find the forecasted value for the requested date
        forecast_dict = {str(date.date()): float(value) for date, value in zip(forecast_dates, forecast)}

        # Return the forecasted value for the requested date
        if str(forecast_date) in forecast_dict:
            return jsonify({"date": str(forecast_date), "forecasted_sales": forecast_dict[str(forecast_date)]})
        else:
            return jsonify({"error": "No forecast available for the provided date."}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=False)

