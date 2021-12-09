import pandas as pd 
import numpy as np 
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# https://youtu.be/1Gx1y2boe_M

ln = LinearRegression()

def inpout(final):
    """
    Splits the categories of data into the inputs (X) and ouputs (y) for ML. 

    Parameters 
    ----------
    final: pandas dataframe 
        The training dataset 

    Returns 
    ----------
    X: list 
        the input variables 
    y: list 
        the desired output variables 
    
    """
    X = final[['home', 'Atlanta Hawks',
        'Charlotte Hornets', 'Denver Nuggets', 'Golden State Warriors',
        'Houston Rockets', 'LA Clippers', 'Los Angeles Lakers',
        'Memphis Grizzlies', 'Miami Heat', 'Milwaukee Bucks',
        'Minnesota Timberwolves', 'New Orleans Pelicans',
        'Oklahoma City Thunder', 'Phoenix Suns', 'Sacramento Kings',
        'San Antonio Spurs', 'Toronto Raptors', 'Utah Jazz', 'Boston Celtics',
        'Brooklyn Nets', 'Chicago Bulls', 'Cleveland Cavaliers',
        'Dallas Mavericks', 'Detroit Pistons', 'Indiana Pacers',
        'New York Knicks', 'Orlando Magic', 'Philadelphia 76ers',
        'Portland Trail Blazers', 'Washington Wizards', 'pts-1', 'pts-2',
        'pts-3', 'pts-4', 'pts-5', 'reb-1', 'reb-2', 'reb-3', 'reb-4', 'reb-5',
        'ast-1', 'ast-2', 'ast-3', 'ast-4', 'ast-5']]
    y = final[['pts', 'reb', 'ast']]

    return X, y

def train_model(final):
    """
    Trains a linear regression model to the player's statistics using sklearn 

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

    ln.fit(X_train, y_train)

    prediction = ln.predict(X_test)

    return prediction, np.array(y_test) 

def predict(next_game, player, date, pred_model, pred_inputs):
    """
    Applies the linear regression model to the next game and gets an output, also evaluating the error and the model's efficacy. 

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
        the results of the linear regression ML analysis and the error estimations. 
    
    """
    result = ln.predict(next_game)

    chi2, r2 = mean_squared_error(pred_inputs, pred_model), r2_score(pred_inputs, pred_model) # error calculations (https://scikit-learn.org/stable/auto_examples/linear_model/plot_ols.html)
    #https://scikit-learn.org/stable/modules/generated/sklearn.metrics.r2_score.html

    results = {'Player': player.name, 'Date': date, 'Team': player.team, 'Pts': [result[0][0]], 'Reb': [result[0][1]], 'Ast':[result[0][2]],
        'Error': chi2, 'Regression Score': r2
    }

    df_final = pd.DataFrame(results)
    return df_final
