from fastapi import APIRouter
import numpy as np # Multi-dimensional array manipulation
import pandas as pd # DataFrame Manipulation
import matplotlib.pyplot as plt # Data Visualization
import seaborn as sns # Data Visualization
from sklearn import metrics
from database import db_cursor, db_connection
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle
from sklearn.metrics import r2_score
from models.tictactoe import TictactoePredictBase  # Assuming you have a Tictactoe model

router = APIRouter()

@router.get("/tictactoe_model/train")
async def train():
    tictactoe_df = pd.read_sql("SELECT * FROM tictactoe", con=db_connection)
    
    X = tictactoe_df.drop(["class_"], axis="columns")  # Assuming "Class" is the target column
    y = tictactoe_df["class_"]


    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

    model_rf = RandomForestClassifier()
    model_rf.fit(X_train, y_train)

    with open('model_rf_tictactoe', 'wb') as files:
        pickle.dump(model_rf, files)

    # make predictions on the test data
    yRF_predict = model_rf.predict(X_test)

    r2 = round(r2_score(y_test, yRF_predict), 3)

    return {"message": "model_rf_tictactoe", "R2": str(r2)}

@router.post("/tictactoe_models/predict")
async def predict(item: TictactoePredictBase):
    # Define a mapping from Tic Tac Toe symbols to numeric values (e.g., 'x' to 1, 'o' to 0)
    symbol_mapping = {'x': 1, 'o': 0}
    
    # Create a dictionary to hold the input data with numeric values
    input_data = {
        "top_left_square": [symbol_mapping[item.top_left_square]],
        "top_middle_square": [symbol_mapping[item.top_middle_square]],
        "top_right_square": [symbol_mapping[item.top_right_square]],
        "middle_left_square": [symbol_mapping[item.middle_left_square]],
        "middle_middle_square": [symbol_mapping[item.middle_middle_square]],
        "middle_right_square": [symbol_mapping[item.middle_right_square]],
        "bottom_left_square": [symbol_mapping[item.bottom_left_square]],
        "bottom_middle_square": [symbol_mapping[item.bottom_middle_square]],
        "bottom_right_square": [symbol_mapping[item.bottom_right_square]]
    }

    # Load the trained model
    with open('model_rf_tictactoe', 'rb') as model_file:
        model_rf = pickle.load(model_file)

    # Create a DataFrame from the input data
    tictactoe_df = pd.DataFrame(input_data)
    
    # Make predictions using the loaded model
    deploy_Y = model_rf.predict(tictactoe_df)
    
    # Convert the prediction to a Python native integer
    prediction = int(deploy_Y[0])

    return {"class_": prediction}
