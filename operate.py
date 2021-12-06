import streamlit as st
import pandas as pd

from pull import Player 
from pre_process import compiler
from train import train_model
from prediction_set import nextgame
from train import predict
from neural_net import predict_nn

st.title('nbaStats: Player Stat Predictor')

st.text('Made by David Saunders')

player = st.text_input("Player:")

if len(player) > 0:

    pl = Player(player)

    training_data = compiler(pl.stats)
    plstats = training_data[['date', 'pts', 'reb', 'ast']]

    pred_model, pred_inputs = train_model(training_data)

    next_game, gamedate = nextgame(pl, training_data) 

    result = predict(next_game, pl, gamedate, pred_model, pred_inputs)
    result2 = predict_nn(training_data, next_game, pl, gamedate)

    st.header('Linear Regression Calculation')

    st.write(result)

    st.header('Neural Network Calculation')

    st.write(result2)

    st.header('Season Statistics')

    st.write(plstats)

