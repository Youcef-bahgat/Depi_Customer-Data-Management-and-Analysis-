import streamlit as st
import pickle
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from pandas.tseries.offsets import DateOffset

# Load the saved ARIMA model
with open('C:/Users/FreeComp\Downloads/arima_model.pkl', 'rb') as pkl_file:
    model_fit = pickle.load(pkl_file)

# Streamlit App
st.title("Sales Forecasting App")

# Input from the user: choose a future month for prediction
selected_date = st.date_input("Select a future date to forecast sales for the month:")

# Ensure the selected date is valid
if selected_date:
    # Convert to the first day of the selected month
    selected_month_start = pd.Timestamp(selected_date.year, selected_date.month, 1)
    
    # Predict for the next 12 months from the last observed month in the data
    forecast_steps = 12
    forecasted_values = model_fit.forecast(steps=forecast_steps)
    
    # Create a date range for the forecasted 12 months
    forecast_dates = pd.date_range(start=model_fit.data.dates[-1], periods=forecast_steps + 1, freq='M')[1:]
    
    # Combine the forecast dates and values into a DataFrame
    forecast_df = pd.DataFrame({'Date': forecast_dates, 'Forecasted Sales': forecasted_values})
    
    # Find the prediction for the selected month
    predicted_value = forecast_df[forecast_df['Date'].dt.to_period('M') == selected_month_start.to_period('M')]
    
    if not predicted_value.empty:
        # Display the forecasted value for the selected month
        st.write(f"## Forecasted Sales for {selected_month_start.strftime('%B %Y')}:")
        st.write(f"${predicted_value['Forecasted Sales'].values[0]:,.2f}")
        
        # Plot the forecast with the selected month highlighted
        plt.figure(figsize=(10, 6))
        plt.plot(forecast_df['Date'], forecast_df['Forecasted Sales'], label='Forecasted Sales', linestyle='--')
        plt.axvline(selected_month_start, color='red', linestyle='--', label=f'Selected Month: {selected_month_start.strftime("%B %Y")}')
        plt.title('Sales Forecast for the Next 12 Months')
        plt.xlabel('Date')
        plt.ylabel('Total Sales')
        plt.legend()
        plt.grid(True)
        st.pyplot(plt)
    else:
        st.write(f"## No forecast available for {selected_month_start.strftime('%B %Y')}")
else:
    st.write("## Please select a date.")
