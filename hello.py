import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Generate dates for three years (365 days * 3 years)
start_date = pd.to_datetime('2022-01-01')
end_date = start_date + pd.DateOffset(days=365 * 3 - 1)
date_range = pd.date_range(start=start_date, end=end_date, freq='D')

# Generate random amounts for each day with more deviation
amounts = np.random.normal(loc=500, scale=100, size=len(date_range))  # Adjusted mean and standard deviation

# Introduce higher amounts during festive seasons
festive_dates = pd.to_datetime(['2022-12-25', '2023-01-01',  # Christmas and New Year
                                '2023-01-14', '2023-09-06',  # Pongal and Onam
                                '2023-11-04', '2023-10-08',  # Diwali and Navaratri
                                '2024-03-22', '2024-04-02',  # Ramadan and Bakrid
                                '2024-12-25', '2025-01-01',  # Christmas and New Year
                                '2023-02-09', '2023-05-05',  # Valentine's Day and Cinco de Mayo
                                '2023-07-04', '2024-02-14',  # Independence Day and Valentine's Day
                                '2024-05-05', '2024-07-04'])  # Cinco de Mayo and Independence Day

# Ensure festive dates align with the actual dates in the dataset
festive_dates = festive_dates[festive_dates.isin(date_range)]

# Introduce higher amounts during festive days
amounts[date_range.isin(festive_dates)] += np.random.normal(loc=800, scale=100, size=len(festive_dates))  # Adjusted mean and standard deviation

# Clip values to ensure normal values fall in the range of 300 to 700
# and festive values fall in the range of 700 to 1500
amounts = np.clip(amounts, 300, 1500)

# Create the DataFrame
df = pd.DataFrame({'date': date_range, 'amount': amounts})

# Convert datetime to numerical representation (number of days since start_date)
# df['days_since_start'] = (df['date'] - start_date).dt.days
# df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")

 # Set date as index
df.set_index("date", inplace=True)

# Sort DataFrame by date
df.sort_index(inplace=True)

# Check for and handle NaN values
if df['amount'].isnull().any():
    df = df.dropna()

# Stationarize the time series (if needed)
df['amount_diff'] = df['amount'].diff().dropna()

# Fit an ARIMA model
order = (1, 1, 1)  # Example order, adjust based on ACF and PACF analysis
model = ARIMA(df['amount'], order=order)
results = model.fit()

# Forecast future values for one year
forecast_steps = 12  # Forecast for the next one year
forecast_df = pd.DataFrame(columns=['Forecast', 'Lower Confidence Interval', 'Upper Confidence Interval'])

for _ in range(forecast_steps):
    # Forecast one step ahead
    forecast = results.get_forecast(steps=1)
    
    # Append the forecasted values to the DataFrame
    next_date = forecast_df.index[-1] + pd.Timedelta(days=1) if not forecast_df.empty else df.index[-1] + pd.Timedelta(days=1)
    forecast_df.loc[next_date] = {
        'Forecast': forecast.predicted_mean.iloc[0],
        'Lower Confidence Interval': forecast.conf_int().iloc[0, 0],
        'Upper Confidence Interval': forecast.conf_int().iloc[0, 1]
    }
    
    # Update the model with the observed value (use the actual value if available)
    observed_value = df['amount'].iloc[-1] if not df.empty else forecast.predicted_mean.iloc[0]
    results.update(observed_value)
    
    # Append the observed value to the DataFrame
    df.loc[df.index[-1] + pd.DateOffset(days=1)] = {'amount': observed_value}

# Create a DataFrame with forecasted values
forecast_df.index = pd.date_range(df.index[-1] + pd.Timedelta(days=1), periods=forecast_steps)

# Plot the actual data and the forecast
plt.figure(figsize=(10, 6))
plt.plot(df['amount'], label='Actual Amount', color='blue')
plt.plot(forecast_df['Forecast'], label='Forecasted Amount', color='red')
plt.fill_between(forecast_df['Lower Confidence Interval'], forecast_df['Upper Confidence Interval'], color='pink', alpha=0.3, label='Confidence Interval')
plt.title('Actual and Forecasted Amount Over Time')
plt.xlabel('Date')
plt.ylabel('Amount')
plt.legend()
plt.show()

# Print the forecast DataFrame
print(forecast_df)

