import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
from datetime import datetime

from pull import get_team_name

def onehot_encode(df):
    """
    One-hot encode a dataframe using pandas to identify the opposing team for a given game. 

    Parameters 
    ----------
    df: pandas dataframe
        Containing basic stats from past games (pts, reb, ast, date, etc)

    Returns 
    ----------
    df: pandas dataframe 
        The updated df, with one-hot encoding for each NBA team. 
    
    """

    other_teams = [get_team_name(op) for op in range(30)] # more efficient? 
    othert = other_teams

    for j in df['opponent'].values:
        for i in other_teams:
            if i == j:
                othert.remove(i)     

    for team in othert: # getting the other teams in! 
        df[f'{team}'] = np.zeros(len(df.index))

    oh = pd.get_dummies(df['opponent'])

    df = df.drop('opponent', axis = 1)
    df = pd.concat([df, oh], axis=1)

    return df 

def add_temporality(df):
    """
    Adds previous five-game statistics to each sample as numerical data. 

    Parameters 
    ----------
    df: pandas dataframe
        Containing basic stats from past games (pts, reb, ast, date, etc)

    Returns 
    ----------
    df: pandas dataframe 
        The updated df, previous stats included. 
    
    """
    df_ = df.drop([0,1,2,3,4])
    
    pts = df['pts'].values
    reb = df['reb'].values
    ast = df['ast'].values
    
    pts_ = []
    reb_ = []
    ast_ = []
    
    for i in range(1,6):
        pts_.append([pts[j-i] for j in range(5,len(pts))])
        reb_.append([reb[j-i] for j in range(5,len(reb))])
        ast_.append([ast[j-i] for j in range(5,len(ast))])
        
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

def compiler(stats_set):
    """
    Processes the API data into a clean dataframe for analysis and predictions. 

    Parameters 
    ----------
    stats_set: list
        Incoming data on all previous games from the balldontlie API request. 

    Returns 
    ----------
    final: pandas dataframe 
        The training dataset, cleaned and processed. 
    
    """
    df = pd.DataFrame([])
    for i, stats in enumerate(stats_set):
        if stats['min'] == '' or stats['min'] == '0:00': # not counting games that they did not play! 
            if i == 0:
                df = pd.DataFrame([])
            continue
        if stats['game']['home_team_id'] == stats['player']['team_id']:
            home = 0 
            opponent = stats['game']['visitor_team_id']
        else:
            home = 1
            opponent = stats['game']['home_team_id']
        g_info = {'date':stats['game']['date'][:10],'pts': stats['pts'], 'reb': stats['reb'], 'ast': stats['ast'], 'mins':stats['min'], 'home':home,
                'opponent':get_team_name(opponent)}
        if i == 0: 
            df = pd.DataFrame([g_info])
        else:
            df2 = pd.DataFrame([g_info])
            df = pd.concat([df,df2])
    
    df = df.sort_values(by=['date'])
    df = df.reset_index(drop=True)

    df = onehot_encode(df)

    final = add_temporality(df)

    # Remove the current game if it is underway 

    date = datetime.today().strftime('%Y-%m-%d')

    for i in final['date']:
        if i == date:
            final = final.iloc[:-1 , :] # https://thispointer.com/drop-last-row-of-pandas-dataframe-in-python-3-ways/

    return final

def season_stats(stats_set):
    """
    Processes the API data into a clean dataframe for the season statistics. 

    Parameters 
    ----------
    stats_set: list
        Incoming data on all previous games from the balldontlie API request. 

    Returns 
    ----------
    final: pandas dataframe 
        The season statistics. 
    
    """

    df = pd.DataFrame([])
    for i, stats in enumerate(stats_set):
        if stats['min'] == '' or stats['min'] == '0:00': # not counting games that they did not play! 
            if i == 0:
                df = pd.DataFrame([])
            continue
        if stats['game']['home_team_id'] == stats['player']['team_id']:
            home = 0 
            opponent = stats['game']['visitor_team_id']
        else:
            home = 1
            opponent = stats['game']['home_team_id']
        g_info = {'date':stats['game']['date'][:10],'pts': stats['pts'], 'reb': stats['reb'], 'ast': stats['ast'], 'mins':stats['min'], 'home':home,
                'opponent':get_team_name(opponent)}
        if i == 0: 
            df = pd.DataFrame([g_info])
        else:
            df2 = pd.DataFrame([g_info])
            df = pd.concat([df,df2])
    
    df = df.sort_values(by=['date'])
    df = df.reset_index(drop=True)

    # Remove the current game if it is underway 

    date = datetime.today().strftime('%Y-%m-%d')

    for i in final['date']:
        if i == date:
            final = final.iloc[:-1 , :] # https://thispointer.com/drop-last-row-of-pandas-dataframe-in-python-3-ways/

    return final

