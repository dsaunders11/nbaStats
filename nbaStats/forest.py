from numpy.random import random_sample
import pandas as pd 
import numpy as np 
from sklearn.model_selection import train_test_split 
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor

from nbaStats.train import inpout

#Citations: https://www.geeksforgeeks.org/random-forest-regression-in-python/

cl = RandomForestRegressor(n_estimators=100, random_state=0)

def training_forest(final):
    """
    Trains a random forest regression model to the player's statistics using sklearn 

    Parameters 
    ----------
    final: pandas dataframe 
        The training dataset 

    Returns 
    ----------
    prediction: list 
        the predicted statlines from the test dataset 
    np.array(y_test): array-like 
        the actual statlines from the test dataset 
    
    """
    X, y = inpout(final)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state=100)

    cl.fit(X_train, y_train)

    prediction = cl.predict(X_test)

    return prediction, np.array(y_test)

def predict_forest(next_game, player, date, pred_model, pred_inputs):
    """
    Applies the random forest regression model to the next game and gets an output, also evaluating the error and the model's efficacy. 

    Parameters 
    ----------
    next_game: pandas dataframe 
        the organized information about the next game 
    player: class obj 
        the player's information 
    date: str 
        the game date 
    pred_model: list
        the model's statline predictions on test data 
    pred_inputs: array-like 
        the actual statlines from the test data 

    Returns 
    ----------
    df_final: pandas dataframe 
        the results of the random forest regression ML analysis and the error estimations. 
    
    """

    result = cl.predict(next_game)

    chi2, r2 = mean_squared_error(pred_inputs, pred_model), r2_score(pred_inputs, pred_model) # error calculations (https://scikit-learn.org/stable/auto_examples/linear_model/plot_ols.html)
    #https://scikit-learn.org/stable/modules/generated/sklearn.metrics.r2_score.html

    results = {'Player': player.name, 'Date': date, 'Team': player.team, 'Pts': [result[0][0]], 'Reb': [result[0][1]], 'Ast':[result[0][2]],
        'Error': chi2, 'Regression Score': r2
    }

    df_final = pd.DataFrame(results)
    return df_final