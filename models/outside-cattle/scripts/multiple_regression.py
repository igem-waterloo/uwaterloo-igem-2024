from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import data

def multiple_regression(X_train, X_test, y_train, y_test):
    regr = linear_model.LinearRegression()
    regr.fit(X_train, y_train/100)
    
    # y_pred = regr.predict(X_test)
    # scaling it back
    y_pred = regr.predict(X_test) * 100

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


# run this file for the MSE, MAE, R2, and plot for multiple linear regression
X_train, X_test, y_train, y_test = data.process_data()

print("---------- MULTIPLE LINEAR REGRESSION ----------")
mlr_pred = multiple_regression(X_train, X_test, y_train, y_test)
# plot predicted vs. actual
data.plot(y_test, mlr_pred, "Multiple Linear Regression")
