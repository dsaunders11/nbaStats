import streamlit as st
import time
import pandas as pd 
import json

from pull import Player 
from pre_process import compiler, season_stats
from train import train_model, predict
from prediction_set import nextgame
from neural_net import predict_nn
from forest import training_forest, predict_forest

st.title('nbaStats: Player Stat Predictor')

st.text('Made by David Saunders')

st.info("Enter the player's name with normal capitalization (i.e 'Kevin Durant') as listed on [link](https://www.nba.com/players)")

st.warning("Making too many requests in a short period of time will overload the API with requests. Please wait a short amount of time between each request.")

player = st.text_input("Player:")

st.text('Progress:')

elapsed = st.progress(0) # times estimated based on the running time of each segment (as performed in a notebook)

if player == 'Dash Stevanovich':

    st.success('80 PTS, 69 REB, 202 BLK, 90 STL')

    quit()

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

    st.header('__*Next Game:*__ ' + result['Date'][0])

    st.subheader(result['Team'][0] + ' _vs_ ' + opponent[0])

    st.header('__*Predictions:*__')

    st.subheader('_Random Forest Regression Calculation_')

    forest = pd.DataFrame({'':'Predictions:', 'PTS':round(result3['Pts'],1), 'REB':round(result3['Reb'],1), 'AST': round(result3['Ast'],1)})
    forest.set_index('', inplace=True)

    st.write(forest)
    st.write("Error: " + str(round(result3['Error'][0],1)))
    st.write('Regression Score: ' + str(round(result3['Regression Score'][0],1)))

    st.subheader('_Linear Regression Calculation_')

    linear = pd.DataFrame({'':'Predictions:','PTS':round(result['Pts'],1),'REB':round(result['Reb'],1), 'AST': round(result['Ast'],1)})
    linear.set_index('', inplace=True)

    st.write(linear)
    st.write("Error: " + str(round(result['Error'][0],1)))
    st.write('Regression Score: ' + str(round(result['Regression Score'][0],1)))

    st.subheader('_Neural Network Calculation_')

    neural = pd.DataFrame({'':'Predictions:','PTS':round(result2['Pts'],1),'REB':round(result2['Reb'],1), 'AST': round(result2['Ast'],1)})
    neural.set_index('', inplace=True)

    st.write(neural)
    st.write("Error (pts): " + str(round(result2['Error in Pts'][0],1)))
    st.write("Error (reb): " + str(round(result2['Error in Reb'][0],1)))
    st.write("Error (ast): " + str(round(result2['Error in Ast'][0],1)))

    st.header('__*Previous 5-Game Statistics*__')

    final_stats = plstats[-5:]
    final_stats.reset_index()

    st.table(final_stats)

    st.balloons()

