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
    plstats = training_data[['date', 'pts', 'reb', 'ast']]

    pred_model, pred_inputs = train_model(training_data)
    pred_modelfr, pred_inputsfr = training_forest(training_data)
    elapsed.progress(50)

    next_game, gamedate = nextgame(pl, training_data) 
    elapsed.progress(90)

    result = predict(next_game, pl, gamedate, pred_model, pred_inputs)
    result2 = predict_nn(training_data, next_game, pl, gamedate)
    result3 = predict_forest(next_game, pl, gamedate, pred_modelfr, pred_inputsfr)
    elapsed.progress(100)

    st.header('Linear Regression Calculation')

    st.table(result)

    st.header('Neural Network Calculation')

    st.table(result2)

    st.header('Random Forest Regression Calculation')

    st.write(result3)

    st.header('Season Statistics')

    st.write(plstats)

    st.balloons()

