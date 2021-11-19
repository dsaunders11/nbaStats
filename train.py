import pandas as pd 
import numpy as np 
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression

# https://youtu.be/1Gx1y2boe_M

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

def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state=100)

    ln = LinearRegression()
    ln.fit(X_train, y_train)

    prediction = ln.predict(X_test)

    return prediction 

