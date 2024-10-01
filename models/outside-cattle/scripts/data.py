import pandas as pd 
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import matplotlib.pyplot as plt
import numpy as np


def process_data(): # returns a tuple of datasets (X_train, X_test, y_train, y_test)
    # load data
    methane_data = pd.read_csv("models/outside-cattle/data/methane.csv")
    metadata = pd.read_csv("models/outside-cattle/data/metadata.csv")
    lactation_data = pd.read_csv("models/outside-cattle/data/lactation_stage.csv")
    data = pd.merge(methane_data, metadata, on='sample_id')
    data = pd.merge(data, lactation_data, on='sample_id')
    # dropping outliers
    data = data[data['methane emission (g/d)'] <= 600].reset_index().drop(['sample_id'], axis=1)

    # get target data
    y = data['methane emission (g/d)']
    X = data.drop(['methane emission (g/d)'], axis=1)

    # divide data into traning and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 101)
    
    # preprocess data
    scaler = StandardScaler()

    # Fit the scaler on the training data and transform it
    X_train_scaled = scaler.fit_transform(X_train)

    # Transform the test data using the same scaler
    X_test_scaled = scaler.transform(X_test)

    return (X_train_scaled, X_test_scaled, y_train, y_test)


def plot(test, pred, model_name):
    # Scatter plot of actual vs. predicted
    plt.scatter(test, pred, color='blue', label='Predicted vs. Actual')

    # Plot a 45-degree line for reference (ideal case: predicted = actual)
    line = np.linspace(min(test), max(test), 100)
    plt.plot(line, line, color='red', linestyle='--', label='Ideal Fit (y=x)')

    # Labels and title
    plt.xlabel('Actual values (test)')
    plt.ylabel('Predicted values (pred)')
    plt.title(f'{model_name}: Actual vs Predicted (methane emissions, grams/cow/day)')

    # Add a legend
    plt.legend()

    # Display the plot
    plt.show()
    return

