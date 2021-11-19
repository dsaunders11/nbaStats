import pandas as pd 
import numpy as np 
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression

# https://youtu.be/1Gx1y2boe_M

ln = LinearRegression()

def inpout(final):
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

    X, y = inpout(final)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state=100)

    ln.fit(X_train, y_train)

    prediction = ln.predict(X_test)

    return prediction 

def predict(next_game, player, date):
    result = ln.predict(next_game)

    results = {'player': player.name, 'date': date, 'team': player.team, 'pts': [result[0][0]], 'reb': [result[0][1]], 'ast':[result[0][2]]}

    df_final = pd.DataFrame(results)

    return df_final

