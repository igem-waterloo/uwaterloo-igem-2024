import pandas as pd 
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error

# var to control if we want to log data
LOG = False

def random_forest(X_train, X_test, y_train, y_test): # returns predictions
    if LOG: 
        print(f'X_train: {X_train.shape}')
        print(f'y_train: {y_train.shape}')
        print(f'X_test: {X_test.shape}')
        print(f'y_test: {y_test.shape}')

        print(X_train)


    param_grid = {
        'n_estimators': [100, 200, 500],
        'max_depth': [None, 10, 20, 30],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4],
        'max_features': ['auto', 'sqrt', 'log2']
    }

    """
    trying to find best parameters but it didn't really work
    """
    # from sklearn.model_selection import GridSearchCV
    # rf = RandomForestRegressor()
    # grid_search = GridSearchCV(rf, param_grid, cv=5, scoring='neg_mean_squared_error')
    # grid_search.fit(X_train, y_train)

    # best_rf = grid_search.best_estimator_
    # best_rf.fit(X_train, y_train)

    # build random forest model
    rf_model = RandomForestRegressor(n_estimators=100, max_depth=15, max_features="sqrt", random_state=42)
    rf_model.fit(X_train, y_train)

    # make predictions
    y_pred = rf_model.predict(X_test)
    # y_pred = best_rf.predict(X_test)
    # print(best_rf.get_params())

    # evaluate model performance
    mse = mean_squared_error(y_test, y_pred)
    print(f'Mean Squared Error : {mse}')

    # Calculate Mean Absolute Error (MAE)
    mae = mean_absolute_error(y_test, y_pred)
    print("Mean Absolute Error:", mae)

    return y_pred
