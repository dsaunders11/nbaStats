import numpy as np 
import pandas as pd
from datetime import datetime

from nbastats.pull import get_team_name

def future_compiler(upcoming, team_id): 
    """
    Sets up the necessary categorical variables for a future game. 

    Parameters 
    ----------
    upcoming: list 
        the basic information about the upcoming game 
    team_id: int 
        the player's team's ID 

    Returns 
    ----------
    g_info2: dict 
        the basic categorical information about the upcoming game 
    
    """
    if upcoming['home_team']['id'] == team_id:
        home = 0 
        opponent = upcoming['visitor_team']['id']
    else:
        home = 1
        opponent = upcoming['home_team']['id']
    g_info2 = {'date':upcoming['date'][:10],'home':home,
            'opponent':get_team_name(opponent)}
    return g_info2

def upcoming_final(df2, final):
    """
    Adds previous five-game statistics to each sample as numerical data. 

    Parameters 
    ----------
    df2: pandas dataframe
        upcoming game with categorical variables 
    final: pandas dataframe 
        Containing basic stats from past games (pts, reb, ast, date, etc)

    Returns 
    ----------
    df_: pandas dataframe 
        The updated df, previous stats included. 
    
    """
    df_ = df2
    pts = final['pts'].values
    reb = final['reb'].values
    ast = final['ast'].values
    
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
    """
    One-hot encodes the NBA teams for the next game using pandas (to ensure the prediction dataset has the same format as the training/testing one)

    Parameters 
    ----------
    df2: pandas dataframe
        upcoming game with simple parameters 

    Returns 
    ----------
    df2: pandas dataframe 
        The updated df, with the given opponent one-hot encoded with the other NBA teams. 
    
    """
    for team in other_teams:
        if team == df2['opponent'].values:
            df2[f'{team}'] = np.ones(1)
        else:
            df2[f'{team}'] = np.zeros(1)
    return df2

def nextgame(player, final):
    """
    Compiles the necessary information for the next game to enter into the ML algorithms. 

    Parameters 
    ----------
    player: class obj 
        the given player 
    final: pandas dataframe 
        The training dataset 

    Returns 
    ----------
    df: pandas dataframe 
        The data to pe processed by the ML algorithms for a prediction.
    gamedate: str 
        the date of the game to be predicted  
    
    """

    date = datetime.today().strftime('%Y-%m-%d')

    upcoming = player.get_future_game(date)

    g_info = future_compiler(upcoming, player.team_id)

    df = pd.DataFrame([g_info])

    df = encode_future(df)

    opponent = df['opponent']
    df = df.drop('opponent', axis = 1)
    df = df.dropna()

    df = upcoming_final(df, final)
    gamedate = g_info['date']
    df = df.drop('date', axis = 1)

    return df, gamedate, opponent

def corr(result, result2, result3):
    """
    Computes the correlation between the three regression methods by taking squared differences from averages in each category and then averaging those results. 
    Interpret this as a smaller # meaning a better score / agreement. 

    Parameters 
    ----------
    result: pandas dataframe 
        linear regression results 
    result2: pandas dataframe
        the neural network results 
    result3: pandas dataframe 
        the random forest regression results 

    Returns 
    ----------
    correlation: pandas.core.series.Series
        the correlation value for the given player 
    
    """
    avpts = (result['Pts'] + result2['Pts'] + result3['Pts']) / 3
    diffs_pts = (avpts - result['Pts'])**2 + (avpts - result2['Pts'])**2 + (avpts - result3['Pts'])**2

    avast = (result['Ast'] + result2['Ast'] + result3['Ast']) / 3
    diffs_ast = (avast - result['Ast'])**2 + (avast - result2['Ast'])**2 + (avast - result3['Ast'])**2

    avreb = (result['Reb'] + result2['Reb'] + result3['Reb']) / 3
    diffs_reb = (avreb - result['Reb'])**2 + (avreb - result2['Reb'])**2 + (avreb - result3['Reb'])**2

    correlation = (diffs_reb + diffs_ast + diffs_pts) / 3

    return correlation
