# import pandas as pd
# from statsmodels.tsa.arima.model import ARIMA
# from pymongo.mongo_client import MongoClient
# from decouple import config
# import matplotlib.pyplot as plt

# # Get the MongoDB Atlas connection URI
# uri = config("MONGO_URI")

# # Create a new client and connect to the server
# client = MongoClient(uri)

# db = client["Database"]
# collection = db["TS"]

# def predict_and_plot():
#     # Fetch data from MongoDB
#     cursor = collection.find({})
#     data_list = list(cursor)

#     # Convert data to Pandas DataFrame
#     df = pd.DataFrame(data_list)

#     # Convert date column to datetime format
#     df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")

#     # Set date as index
#     df.set_index("date", inplace=True)

#     # Sort DataFrame by date
#     df.sort_index(inplace=True)

#     # Check for and handle NaN values
#     if df['amount'].isnull().any():
#         df = df.dropna()

#     # Stationarize the time series (if needed)
#     df['amount_diff'] = df['amount'].diff().dropna()

#     # Fit an ARIMA model
#     order = (1, 1, 1)  # Example order, adjust based on ACF and PACF analysis
#     model = ARIMA(df['amount'], order=order)
#     results = model.fit()

#     # Forecast future values for one year
#     forecast_steps = 365  # Forecast for the next one year
#     forecast = results.get_forecast(steps=forecast_steps)

#     # Create a DataFrame with forecasted values
#     forecast_df = pd.DataFrame({
#         'Forecast': forecast.predicted_mean,
#         'Lower Confidence Interval': forecast.conf_int().iloc[:, 0],
#         'Upper Confidence Interval': forecast.conf_int().iloc[:, 1]
#     }, index=pd.date_range(df.index[-1] + pd.Timedelta(days=1), periods=forecast_steps))

#     # Plot the actual data and the forecast
#     plt.figure(figsize=(10, 6))
#     plt.plot(df['amount'], label='Actual Amount', color='blue')
#     plt.plot(forecast_df['Forecast'], label='Forecasted Amount', color='red')
#     plt.fill_between(forecast_df.index, forecast_df['Lower Confidence Interval'], forecast_df['Upper Confidence Interval'], color='pink', alpha=0.3, label='Confidence Interval')
#     plt.title('Actual and Forecasted Amount Over Time')
#     plt.xlabel('Date')
#     plt.ylabel('Amount')
#     plt.legend()
#     plt.show()

#     # Print the forecast DataFrame
#     print(forecast_df)

# predict_and_plot()

import pandas as pd
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt

# # Get the MongoDB Atlas connection URI
uri = config("MONGO_URI")

# # Create a new client and connect to the server
client = MongoClient(uri)

db = client["Database"]
collection = db["TS"]

cursor = collection.find({})
data_list = list(cursor)

# Convert data to Pandas DataFrame
df = pd.DataFrame(data_list)

# Assuming df is your time series DataFrame with 'date' and 'amount' columns
# Make sure 'date' is in datetime format
df['date'] = pd.to_datetime(df['date'], format="%Y-%m-%d")
df.set_index('date', inplace=True)

# Create lag features
for i in range(1, 6):  # Create lag features for the last 5 days
    df[f'amount_lag_{i}'] = df['amount'].shift(i)

# Drop rows with NaN values created by lag features
df.dropna(inplace=True)

# Train-test split
train_size = int(0.8 * len(df))
train, test = df[:train_size], df[train_size:]

# Separate features and target
X_train, y_train = train.drop('amount', axis=1), train['amount']
X_test, y_test = test.drop('amount', axis=1), test['amount']

# Train XGBoost model
model = XGBRegressor()
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model
mae = mean_absolute_error(y_test, y_pred)
print(f'Mean Absolute Error: {mae}')

# Plot the actual vs predicted values
plt.plot(test.index, y_test, label='Actual Amount', color='blue')
plt.plot(test.index, y_pred, label='Predicted Amount', color='red')
plt.title('Actual vs Predicted Amount Over Time')
plt.xlabel('Date')
plt.ylabel('Amount')
plt.legend()
plt.show()
