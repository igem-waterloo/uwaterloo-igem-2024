import data
import multiple_regression
import random_forest

X_train, X_test, y_train, y_test = data.process_data()

print("---------- MULTIPLE LINEAR REGRESSION ----------")
multiple_regression.multiple_regression(X_train, X_test, y_train, y_test)

print()
print()

print("---------- RANDOM FOREST REGRESSION ----------")
random_forest.random_forest(X_train, X_test, y_train, y_test)


