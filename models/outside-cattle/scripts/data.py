import pandas as pd 
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler, StandardScaler

# var to control if we want to log data
LOG = False

def process_data(): # returns a tuple of datasets (X_train, X_test, y_train, y_test)
    # load data
    methane_data = pd.read_csv("models/outside-cattle/data/methane.csv")
    metadata = pd.read_csv("models/outside-cattle/data/metadata.csv")
    lactation_data = pd.read_csv("models/outside-cattle/data/lactation_stage.csv")
    data = pd.merge(methane_data, metadata, on='sample_id')
    data = pd.merge(data, lactation_data, on='sample_id').drop(['sample_id'], axis=1)

    if LOG: print(data)

    # get target data
    y = data['methane emission (g/d)']
    X = data.drop(['methane emission (g/d)'], axis=1)
    if LOG: print(f'x: {X.shape}')

    # divide data into traning and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 101)
    
    # preprocess data
    scaler = MinMaxScaler(feature_range=(-2, 2))

    # Fit the scaler on the training data and transform it
    X_train_scaled = scaler.fit_transform(X_train)

    # Transform the test data using the same scaler
    X_test_scaled = scaler.transform(X_test)


    return (X_train_scaled, X_test_scaled, y_train, y_test)