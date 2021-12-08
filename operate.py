import streamlit as st
import time
import pandas as pd 

from pull import Player 
from pre_process import compiler, season_stats
from train import train_model, predict
from prediction_set import nextgame
from neural_net import predict_nn
from forest import training_forest, predict_forest

st.title('nbaStats: Player Stat Predictor')

st.text('Made by David Saunders')

player = st.text_input("Player:")

st.text('Progress:')

elapsed = st.progress(0) # times estimated based on the running time of each segment (as performed in a notebook)

if len(player) > 0:

    try:
        pl = Player(player)
    except KeyError:
        st.error("Please write out the player's full name as listed on [link](https://www.nba.com/stats/players/)")
    elapsed.progress(5)

    training_data = compiler(pl.stats)
    elapsed.progress(40)
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

    st.table({'PTS':result3['Pts'], 'REB':result3['Reb'], 'AST': result3['Ast']})
    st.write("Error: " + str(result3['Error'][0]))
    st.write('Regression Score: ' + str(result3['Regression Score'][0]))

    st.subheader('_Linear Regression Calculation_')

    st.table({'PTS':result['Pts'], 'REB':result['Reb'], 'AST': result['Ast']})
    st.write("Error: " + str(result['Error'][0]))
    st.write('Regression Score: ' + str(result['Regression Score'][0]))

    st.subheader('_Neural Network Calculation_')

    st.table({'PTS':result2['Pts'], 'REB':result2['Reb'], 'AST': result2['Ast']})
    st.write("Error (pts): " + str(result2['Error in Pts'][0]))
    st.write("Error (reb): " + str(result2['Error in Reb'][0]))
    st.write("Error (ast): " + str(result2['Error in Ast'][0]))

    st.header('__*Previous 5-Game Statistics*__')

    final_stats = plstats[-5:]
    final_stats.reset_index()

    st.table(final_stats)

    st.balloons()

