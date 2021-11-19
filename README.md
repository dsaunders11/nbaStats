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

## Challenges 

I'm facing issues with the particular model's treatment of certain players who have scoring spikes (i.e Steph Curry). I think this may be a linear regression problem, or it could also have to do with how I set up the dataframe and the lack of data so far. Should I be using previous seasons, rather than just working back five games? This also doesn't work if a player hasn't been playing a lot, so I hope to make that arbitrary five-game reference more dynamic. 

I also struggled a lot with getting the modules to interact, and I'm having trouble understanding how to deal with the error. I think the most difficult part coming up will be implementing other predictive measures and comparing them (since it took a long time to get the data into nice dataframes, which may need different formats depending on the regression model). 
