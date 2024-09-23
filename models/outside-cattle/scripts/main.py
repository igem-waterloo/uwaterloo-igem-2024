import data
import multiple_regression
import random_forest


X_train, X_test, y_train, y_test = data.process_data()

print("---------- MULTIPLE LINEAR REGRESSION ----------")
mlr_pred = multiple_regression.multiple_regression(X_train, X_test, y_train, y_test)
# plot predicted vs. actual
# data.plot(y_test, mlr_pred, "Multiple Linear Regression")

print()
print()

print("---------- RANDOM FOREST REGRESSION ----------")
rf_pred = random_forest.random_forest(X_train, X_test, y_train, y_test)
# plot predicted vs. actual
# data.plot(y_test, rf_pred, "Random Forest Regression")


