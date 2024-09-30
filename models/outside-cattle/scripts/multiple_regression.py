from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

def multiple_regression(X_train, X_test, y_train, y_test):
    regr = linear_model.LinearRegression()
    regr.fit(X_train, y_train)
    
    y_pred = regr.predict(X_test)

    # Calculate Mean Squared Error (MSE)
    mse = mean_squared_error(y_test, y_pred)
    print("Mean Squared Error:", mse)

    # Calculate Mean Absolute Error (MAE)
    mae = mean_absolute_error(y_test, y_pred)
    print("Mean Absolute Error:", mae)

    # Calculate R-squared score
    r2 = r2_score(y_test, y_pred)
    print("R-squared score:", r2)

    return y_pred
