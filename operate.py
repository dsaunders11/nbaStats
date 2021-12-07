import streamlit as st
import time

from pull import Player 
from pre_process import compiler
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

    pl = Player(player)
    elapsed.progress(5)

    training_data = compiler(pl.stats)
    elapsed.progress(40)
    # statistics = compiler(pl.stats)
    elapsed.progress(60)
    plstats = training_data[['date', 'pts', 'reb', 'ast']]

    pred_model, pred_inputs = train_model(training_data)
    pred_modelfr, pred_inputsfr = training_forest(training_data)
    elapsed.progress(70)

    next_game, gamedate, opponent = nextgame(pl, training_data) 
    elapsed.progress(90)

    result = predict(next_game, pl, gamedate, pred_model, pred_inputs)
    result2 = predict_nn(training_data, next_game, pl, gamedate)
    result3 = predict_forest(next_game, pl, gamedate, pred_modelfr, pred_inputsfr)
    elapsed.progress(100)

    st.header('Next Game:' + result['Date'][0])

    st.subheader(result['Team'][0] + ' vs ' + opponent[0])

    st.header('Predictions:')

    st.header('Random Forest Regression Calculation')

    st.table({'PTS':result3['Pts'], 'REB':result3['Reb'], 'AST': result3['Ast']})
    st.write("Error: " + result3['Error'][0])
    st.write('Regression Score: ' + result3['Regression Score'][0])

    st.header('Linear Regression Calculation')

    st.table({'PTS':result['Pts'], 'REB':result['Reb'], 'AST': result['Ast']})
    st.write("Error: " + result['Error'][0])
    st.write('Regression Score: ' + result['Regression Score'][0])

    st.header('Neural Network Calculation')

    st.table({'PTS':result2['Pts'], 'REB':result2['Reb'], 'AST': result2['Ast']})
    st.write("Error (pts): " + result2['Error in Pts'][0])
    st.write("Error (reb): " + result2['Error in Reb'][0])
    st.write("Error (ast): " + result2['Error in Ast'][0])

    st.header('Season Statistics')

    st.table(plstats)

    st.balloons()

