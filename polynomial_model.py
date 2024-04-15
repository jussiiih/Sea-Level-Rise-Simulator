import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.metrics import median_absolute_error
from sklearn.metrics import max_error

CURR_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
data_dir = CURR_DIR_PATH + "/data/"

def error_metrics(test, prediction):
    '''Calculates different error metrics for the prediction'''
    error = r2_score(test, prediction)
    print('R2 score: {:.2f}'.format(error))
    error2 = mean_squared_error(test, prediction)
    print('Mean squared error: {:.2f}'.format(error2))
    error3 = mean_absolute_error(test, prediction)
    print('Mean absolute error: {:.2f}'.format(error3))
    error4 = mean_absolute_percentage_error(test, prediction)
    print('Mean absolute percentage error: {:.2f}'.format(error4))
    error5 = median_absolute_error(test, prediction)
    print('Median absolute error: {:.2f}'.format(error5))
    error6 = max_error(test, prediction)
    print('Max error: {:.2f}'.format(error6))

def plot(df, future_years, future_predictions):
    '''Plots a figure of the predictions with Matplotlib'''
    plt.figure(figsize=(10, 6))
    plt.scatter(df['Year'], df['Sea level [mm]'], color='blue', alpha=0.2, label='Historical Data')
    plt.plot(future_years, future_predictions, color='red', linestyle='-', label='Predictions')
    plt.xlabel('Year')
    plt.ylabel('Sea Level [mm]')
    plt.title('Sea Level Predictions')
    plt.legend()
    plt.grid(True)
    plt.show()

def global_model(filename='Global-sea-level.csv'):
    '''Creates a polynomial model for predicting sea level. Takes the name of the csv-file as argument.
    Returns the polynomial prediction. '''
    # Read the file to a dataframe
    filepath = data_dir + filename
    df = pd.read_csv(filepath)
    # Define X and y
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    X = df[['Year']]
    y = df['Sea level [mm]']

    # Create the model and train data
    degree = 2
    polyreg = make_pipeline(PolynomialFeatures(degree), LinearRegression())
    polyreg.fit(X, y)
    # Make prediction
    y_pred = polyreg.predict(X)
    # Predict the future
    future_years = np.array(range(df['Year'].min(), df['Year'].max() + 301)).reshape(-1, 1)
    future_pred = polyreg.predict(future_years)

    # Call error and plotting functions
    plot(df, future_years, future_pred)

    # Change the values so that year 2024 is 0
    value24 = 64.6993582637333
    future_df = pd.DataFrame({'Year': future_years.flatten(), 'Sea level [mm]': future_pred })
    future_df['Sea level [mm]'] -= value24
    # Change values to meters
    future_df['Sea level [mm]'] /= 1000
    future_df.rename(columns={'Sea level [mm]': 'Sea level [m]'}, inplace=True)
    future_df.to_csv('data/sea_level_predictions.csv', index=False)

    return future_pred

# Call the function
global_model('Global-sea-level.csv')