import requests
import json 
import numpy as np 
import pandas as pd

from pre_process import future_compiler 

def upcoming_final(df2):
    df_ = df2
    pts = df['pts'].values
    reb = df['reb'].values
    ast = df['ast'].values
    
    pts_ = pts[-1:-6:-1]
    reb_ = reb[-1:-6:-1]
    ast_ = ast[-1:-6:-1]
    
    df_['pts-1'] = pts_[0]
    df_['pts-2'] = pts_[1]
    df_['pts-3'] = pts_[2]
    df_['pts-4'] = pts_[3]
    df_['pts-5'] = pts_[4]
    
    df_['reb-1'] = reb_[0]
    df_['reb-2'] = reb_[1]
    df_['reb-3'] = reb_[2]
    df_['reb-4'] = reb_[3]
    df_['reb-5'] = reb_[4]
    
    df_['ast-1'] = ast_[0]
    df_['ast-2'] = ast_[1]
    df_['ast-3'] = ast_[2]
    df_['ast-4'] = ast_[3]
    df_['ast-5'] = ast_[4]
    
    return df_

date = '2021-11-18'

upcoming = get_future_game(date)

g_info = future_compiler(upcoming, team_id)

df2 = pd.DataFrame([g_info2])

other_teams = ['Atlanta Hawks',
       'Charlotte Hornets', 'Denver Nuggets', 'Golden State Warriors',
       'Houston Rockets', 'LA Clippers', 'Los Angeles Lakers',
       'Memphis Grizzlies', 'Miami Heat', 'Milwaukee Bucks',
       'Minnesota Timberwolves', 'New Orleans Pelicans',
       'Oklahoma City Thunder', 'Phoenix Suns', 'Sacramento Kings',
       'San Antonio Spurs', 'Toronto Raptors', 'Utah Jazz', 'Boston Celtics',
       'Brooklyn Nets', 'Chicago Bulls', 'Cleveland Cavaliers',
       'Dallas Mavericks', 'Detroit Pistons', 'Indiana Pacers',
       'New York Knicks', 'Orlando Magic', 'Philadelphia 76ers',
       'Portland Trail Blazers', 'Washington Wizards']

def encode_future(df2):
    for team in other_teams: # getting the other teams in and targeting the opponent (the order has to be the same as the training set) 
        if team == df2['opponent'].values:
            df2[f'{team}'] = np.ones(1)
        else:
            df2[f'{team}'] = np.zeros(1)
    return df2

df2 = df2.drop('opponent', axis = 1)
df2 = df2.dropna()

df2 = upcoming_final(df2)
df2 = df2.drop('date', axis = 1)
