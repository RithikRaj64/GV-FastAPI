import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm

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
df['days_since_start'] = (df['date'] - start_date).dt.days

# what will be value in days_since_start column on the christmas of 2025 but dataset has only until 2024
# print((pd.to_datetime('2025-12-25') - start_date).days)

# Prepare future dates and features
future_dates = pd.date_range(start='2025-01-01', end='2026-01-01', freq='D')  # Adjust based on your desired prediction period
future_days_since_start = (future_dates - start_date).days
future_features = pd.DataFrame({'days_since_start': future_days_since_start})

# Fit SARIMA model with exogenous variables
sarima_model = sm.tsa.statespace.SARIMAX(
    df['amount'],
    exog=df[['days_since_start']],
    order=(1, 0, 1),  # Adjust based on your SARIMA order
    seasonal_order=(1, 0, 1, 12),  # Adjust based on your SARIMA seasonal order
)
sarima_results = sarima_model.fit()

# Predict future values with SARIMA model
future_predictions_sarima = sarima_results.get_forecast(steps=len(future_dates), exog=future_features)

# Extract predicted values and confidence intervals
future_predictions_mean = future_predictions_sarima.predicted_mean
future_predictions_ci = future_predictions_sarima.conf_int()

# Add the predicted values to the original DataFrame
df_future_sarima = df.copy()
df_future_sarima['predicted_amount_sarima'] = future_predictions_mean

print(df_future_sarima)

# Plot the future predicted data
plt.figure(figsize=(10, 6))

# Plot SARIMA predicted amount in green dashed line
plt.plot(df_future_sarima['predicted_amount_sarima'], label='SARIMA Predicted Amount', color='green', linestyle='--')

# Set plot title and labels
plt.title('Predicted Amounts Over Time')
plt.xlabel('Date')
plt.ylabel('Amount')

# Show legend to differentiate series
plt.legend()

# Show the plot
plt.show()

# # Plot the future predicted data
# plt.figure(figsize=(10, 6))

# # Plot actual amount in blue solid line
# plt.plot(df['amount'], label='Actual Amount', color='blue', linestyle='-')

# # Plot SARIMA predicted amount in green dashed line
# plt.plot(df_future_sarima['predicted_amount_sarima'], label='SARIMA Predicted Amount', color='green', linestyle='--')

# # Set plot title and labels
# plt.title('Comparison of Predicted Amounts Over Time')
# plt.xlabel('Date')
# plt.ylabel('Amount')

# # Show legend to differentiate series
# plt.legend()

# # Show the plot
# plt.show()
# # Prepare X and y for XGBoost
# X = df[['days_since_start']]
# y = df['amount']

# # Split the data into training and testing sets
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Create and fit the XGBoost model
# model = XGBRegressor()
# model.fit(X_train, y_train)

# # Make predictions on the test set
# y_pred = model.predict(X_test)

# # Calculate and print the Root Mean Squared Error
# rmse = np.sqrt(mean_squared_error(y_test, y_pred))
# print(f'Root Mean Squared Error: {rmse}')

# # Plot the predictions
# plt.figure(figsize=(12, 6))
# plt.plot(df['days_since_start'], df['amount'], label='Actual', color='blue')
# # plt.scatter(X_test, y_test, label='Test Data', color='green')
# plt.scatter(X_test, y_pred, label='Predicted', color='red')
# plt.title('XGBoost Predictions vs Actual Values')
# plt.xlabel('Days Since Start')
# plt.ylabel('Amount')
# plt.legend()
# plt.show()

# # Retrain the model on the full dataset
# X_train_full = df[['days_since_start']]  # Adjust based on your features
# y_train_full = df['amount']  # Adjust based on your target variable
# model = XGBRegressor()
# model.fit(X_train_full, y_train_full)

# # Prepare future dates and features
# future_dates = pd.date_range(start='2025-01-01', end='2026-01-01', freq='D')  # Adjust based on your desired prediction period
# future_days_since_start = (future_dates - start_date).days
# future_features = pd.DataFrame({'days_since_start': future_days_since_start})

# # Predict future values
# future_predictions = model.predict(future_features)

# # Create a DataFrame with future dates and predicted values
# future_df = pd.DataFrame({'date': future_dates, 'predicted_amount': future_predictions})

# print(future_df)

# # Plot the future predicted data
# plt.figure(figsize=(10, 6))
# plt.plot(future_df['date'], future_df['predicted_amount'], label='Predicted Amount', color='red')
# plt.title('Predicted Future Amount Over Time')
# plt.xlabel('Date')
# plt.ylabel('Predicted Amount')
# plt.legend()
# plt.show()