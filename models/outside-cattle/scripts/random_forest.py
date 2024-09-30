import pandas as pd 
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


def random_forest(X_train, X_test, y_train, y_test): # returns predictions

    # build random forest model
    rf_model = RandomForestRegressor(n_estimators=100, max_depth=20, random_state=42)
    rf_model.fit(X_train, y_train)

    # make predictions
    y_pred = rf_model.predict(X_test)

    # evaluate model performance
    mse = mean_squared_error(y_test, y_pred)
    print(f'Mean Squared Error : {mse}')

    # Calculate Mean Absolute Error (MAE)
    mae = mean_absolute_error(y_test, y_pred)
    print("Mean Absolute Error:", mae)

    # Calculate R-squared score
    r2 = r2_score(y_test, y_pred)
    print("R-squared score:", r2)

    return y_pred
