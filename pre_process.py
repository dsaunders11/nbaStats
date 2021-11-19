import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 

def compiler(stats_set):
    for i, stats in enumerate(stats_set):
        if stats['min'] == '': # not counting games that they did not play! 
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

    return df

def onehot_encode(df):
    other_teams = [get_team_name(op) for op in range(30)] # more efficient? 
    othert = other_teams

    for j in df['opponent'].values:
        for i in other_teams:
            if i == j:
                othert.remove(i)     

    for team in othert: # getting the other teams in! 
        df[f'{team}'] = np.zeros(len(df.index))

    oh = pd.get_dummies(df['opponent'])

    learned_opponents = df['opponent'].values

    df = df.drop('opponent', axis = 1)
    df = pd.concat([df, oh], axis=1)

    return df 

def add_temporality(df):
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

def future_compiler(upcoming, team_id):
    if upcoming['home_team']['id'] == team_id:
        home = 0 
        opponent = upcoming['visitor_team']['id']
    else:
        home = 1
        opponent = upcoming['home_team']['id']
    g_info2 = {'date':upcoming['date'][:10],'home':home,
            'opponent':get_team_name(opponent)}
    return g_info2
