# nbaStats
Predicts basic NBA statlines (points, rebounds, assists) for a given player in the next upcoming game using different forms of ML. 

## Citations 

This package makes use of the balldontlie API (https://github.com/ynnadkrap/balldontlie or https://www.balldontlie.io/#introduction). 

ML algorithms are drawn from the scikit-learn library:

Scikit-learn: Machine Learning in Python, Pedregosa et al., JMLR 12, pp. 2825-2830, 2011.

Found at https://scikit-learn.org/stable/index.html. 

## Installation 

Clone the repository and install it using... 

> pip install .

from within the home directory (nbaStats/)

## Use

To use the statline predictor without downloading the code, go to https://share.streamlit.io/dsaunders11/nbastats/main/operate.py

To follow a more involved process, you can import the code into a python file or notebook and follow the process given below...

```
from nbaStats import * 

player = 'Your Input'
pl = Player(player)

training_data = compiler(pl.stats)

pred_model, pred_inputs = train_model(training_data)
pred_modelfr, pred_inputsfr = training_forest(training_data)

next_game, gamedate, opp = nextgame(pl, training_data) 

forest_prediction = predict_forest(next_game, pl, gamedate, pred_modelfr, pred_inputsfr)
linear_prediction = predict(next_game, pl, gamedate, pred_model, pred_inputs)
neuralnet_prediction = predict_nn(training_data, next_game, pl, gamedate)
```

### Breakdown of Use 

First you instantiate the player class object and compile the training data to be used for the regressions. The sklearn models (linear and random forest regressions) have to be trained, saving the predictions on the test data as well as the test data. Next, the sample for the next game has to be generated via API requests, and finally each prediction can be run on said sample. The final prediction results are returned, as well as the relevant errors. 
