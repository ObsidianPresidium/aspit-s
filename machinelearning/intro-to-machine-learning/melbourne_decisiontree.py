import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

melbourne_file_path = "../../external/input/melbourne-housing-snapshot/melb_data.csv"

def get_mae(max_leaf_nodes, train_X, val_X, train_y, val_y):
    model = DecisionTreeRegressor(max_leaf_nodes=max_leaf_nodes, random_state=0)
    model.fit(train_X, train_y)
    preds_val = model.predict(val_X)
    mae = mean_absolute_error(val_y, preds_val)
    return mae

melbourne_data = pd.read_csv(melbourne_file_path)
print(melbourne_data.describe())

melbourne_data = melbourne_data.dropna(axis=0)

y = melbourne_data.Price
melbourne_features = ["Rooms", "Bathroom", "Landsize", "Lattitude", "Longtitude"]
X = melbourne_data[melbourne_features]
print(X.describe())
print(X.head())

melbourne_model = DecisionTreeRegressor(random_state=1)
melbourne_model.fit(X, y)

print("Making predictions for the following 5 houses:")
print(X.head())
print("The predictions are")
print(melbourne_model.predict(X.head()))
predicted_home_prices = melbourne_model.predict(X)
print("Mean Absolute Error:")
print(mean_absolute_error(y, predicted_home_prices))

train_X, val_X, train_y, val_y = train_test_split(X, y, random_state=0)
melbourne_model_validated = DecisionTreeRegressor(random_state=0)
melbourne_model_validated.fit(train_X, train_y)
val_predictions = melbourne_model_validated.predict(val_X)
print("Mean Absolute Error for Validated Model")
print(mean_absolute_error(val_y, val_predictions))

for max_leaf_nodes in [5, 50, 500, 5000]:
    my_mae = get_mae(max_leaf_nodes, train_X, val_X, train_y, val_y)
    print(f"Max leaf nodes: {max_leaf_nodes}\t\tMean Absolute Error: {my_mae}")