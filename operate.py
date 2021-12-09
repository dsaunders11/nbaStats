import streamlit as st
import pandas as pd 
import json

from pull import Player 
from pre_process import compiler, season_stats
from train import train_model, predict
from prediction_set import nextgame
from neural_net import predict_nn
from forest import training_forest, predict_forest

def corr(result, result2, result3):
    avpts = (result['Pts'] + result2['Pts'] + result3['Pts']) / 3
    diffs_pts = (avpts - result['Pts'])**2 + (avpts - result2['Pts'])**2 + (avpts - result3['Pts'])**2

    avast = (result['Ast'] + result2['Ast'] + result3['Ast']) / 3
    diffs_ast = (avast - result['Ast'])**2 + (avast - result2['Ast'])**2 + (avast - result3['Ast'])**2

    avreb = (result['Reb'] + result2['Reb'] + result3['Reb']) / 3
    diffs_reb = (avreb - result['Reb'])**2 + (avreb - result2['Reb'])**2 + (avreb - result3['Reb'])**2

    correlation = (diffs_reb + diffs_ast + diffs_pts) / 3

    return correlation

if 'score' not in st.session_state:
    st.session_state.score = 10000

st.title('nbaStats: Player Stat Predictor')

st.text('Made by David Saunders')

st.info("Enter the player's name with normal capitalization (i.e 'Kevin Durant') as listed on [link](https://www.nba.com/players)")

st.warning("Making too many requests in a short period of time will overload the API with requests. Please wait a short amount of time between each request.")

player = st.text_input("Player:")

st.text('Progress:')

elapsed = st.progress(0) # times estimated based on the running time of each segment (as performed in a notebook)

if len(player) > 0:

    try:
        pl = Player(player)
        elapsed.progress(5)
        training_data = compiler(pl.stats)
        elapsed.progress(40)
    except (KeyError, IndexError):
        st.error("Please write out the player's full name as listed on [link](https://www.nba.com/players)")
    except json.decoder.JSONDecodeError:
        st.error("Overloaded API, please wait a few minutes and try again.")

    plstats = training_data[['date', 'pts', 'reb', 'ast']]

    pred_model, pred_inputs = train_model(training_data)
    pred_modelfr, pred_inputsfr = training_forest(training_data)
    elapsed.progress(50)

    next_game, gamedate, opponent = nextgame(pl, training_data) 
    elapsed.progress(80)

    result = predict(next_game, pl, gamedate, pred_model, pred_inputs)
    result2 = predict_nn(training_data, next_game, pl, gamedate)
    result3 = predict_forest(next_game, pl, gamedate, pred_modelfr, pred_inputsfr)
    elapsed.progress(100)

    correlation = corr(result, result2, result3)

    st.header('__*Next Game:*__ ' + result['Date'][0])

    st.subheader(result['Team'][0] + ' _vs_ ' + opponent[0])

    st.header('Player Score: ' + str(round(correlation[0],0)))
    st.info('A higher value means a lower correlation between the three ML regression methods.')

    if st.session_state.score != 0:
        if st.session_state.score > correlation[0]:
            st.success('This is a better player to bet on!')
        elif st.session_state.score < correlation[0]:
            st.error('This player has a lower correlation; you might want to try again.')
        else:
            st.warning('This player has the same correlation as the previous one.')

    st.session_state.score = correlation[0]

    st.header('__*Predictions:*__')

    st.subheader('_Random Forest Regression Calculation_')

    forest = pd.DataFrame({'':'Predictions:', 'PTS':[round(result3['Pts'],1)[0]], 'REB':[round(result3['Reb'],1)[0]], 'AST': [round(result3['Ast'],1)[0]]})
    forest.set_index('', inplace=True)

    st.write(forest)
    st.write("Error: " + str(round(result3['Error'][0],1)))
    st.write('Regression Score: ' + str(round(result3['Regression Score'][0],1)))

    st.subheader('_Linear Regression Calculation_')

    linear = pd.DataFrame({'':'Predictions:', 'PTS':[round(result['Pts'],1)[0]], 'REB':[round(result['Reb'],1)[0]], 'AST': [round(result['Ast'],1)[0]]})
    linear.set_index('', inplace=True)

    st.write(linear)
    st.write("Error: " + str(round(result['Error'][0],1)))
    st.write('Regression Score: ' + str(round(result['Regression Score'][0],1)))

    st.subheader('_Neural Network Calculation_')

    neural = pd.DataFrame({'':'Predictions:', 'PTS':[round(result2['Pts'],1)[0]], 'REB':[round(result2['Reb'],1)[0]], 'AST': [round(result2['Ast'],1)[0]]})
    neural.set_index('', inplace=True)

    st.write(neural)
    st.write("Error (pts): " + str(round(result2['Error in Pts'][0],1)))
    st.write("Error (reb): " + str(round(result2['Error in Reb'][0],1)))
    st.write("Error (ast): " + str(round(result2['Error in Ast'][0],1)))

    st.header('__*Previous 5-Game Statistics*__')

    final_stats = plstats[-5:]
    final_stats[''] = [5,4,3,2,1]
    final_stats.set_index('', inplace=True)

    st.table(final_stats)

    st.balloons()

