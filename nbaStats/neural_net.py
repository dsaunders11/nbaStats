import pandas as pd 
import numpy as np 
from sklearn.model_selection import train_test_split

# https://realpython.com/python-ai-neural-network/

# https://towardsdatascience.com/inroduction-to-neural-networks-in-python-7e0b422e6c24

# https://stats.stackexchange.com/questions/31641/do-inputs-to-a-neural-network-need-to-be-in-1-1
# normalize the inputs by df['pts'] maximum... 

class NeuralNet:
    def __init__(self, X, y, alpha=0.1):
        """
        Sets up the neural network training data and weights / bias. 

        Parameters 
        ----------
        X: pandas dataframe 
            the input data 
        Y: pandas dataframe 
            the target outputs 
        alpha: float (optional)
            the learning rate (default 0.1)
        
        """
        self.learning_rate = alpha 
        self.inputs = X 
        self.outputs = y 
        self.bias = np.random.randn()

        # SET the weights properly! (it works like this for the stochastic version done until self.train)
        self.weights = [np.random.randn() for i in X.columns] 

        self.errhistory = []
    
    def sigmoid_fn(self, x):
        """
        Activation function for the given input layer 

        Parameters 
        ----------
        x: float
            the computed first layer 

        Returns 
        ----------
        1 / (1 + np.exp(-1.*x)): float 
            x, activated via a sigmoid function 
        
        """
        return 1 / (1 + np.exp(-1.*x))

    def delsig(self, x):
        """
        Derivative of the activation function for the given input layer 

        Parameters 
        ----------
        x: float
            the computed first layer 

        Returns 
        ----------
        (1 / (1 + np.exp(-1.*x))) * (1- 1 / (1 + np.exp(-1.*x))): float
            the derivative of the sigmoid function  
        
        """
        return (1 / (1 + np.exp(-1.*x))) * (1- 1 / (1 + np.exp(-1.*x)))

    def costfn(self, calculated, real): # using mean-squared error, this is what you want to minimize!  
        """
        the mean squared error of the calculation 

        Parameters 
        ----------
        calculated: float 
            the computed result 
        real: float 
            the target result 

        Returns 
        ----------
        (calculated-real)**2: float 
            mean squared error 
        
        """
        return (calculated-real)**2

    def back_propagation(self, sample, result):
        """
        updates the weights and bias using back propagation 

        Parameters 
        ----------
        sample: pandas dataframe
            the sample inputs 
        result: float 
            the target result 

        """
        layer1 = np.dot(sample, self.weights) + self.bias # a number 
        layer2 = self.sigmoid_fn(layer1) # a number 

        derr_dpred = (layer2-result)*2 # a number 
        derr_sig = self.delsig(layer1) # a number 

        derr_l1 = 1

        derr_db = derr_dpred * derr_l1 * derr_sig

        # back propagation to update the weights (dot product deriv)

        dw_l1 = sample
        derr_dw = dw_l1 * derr_dpred * derr_sig

        self.bias = self.bias - (derr_db * self.learning_rate)
        self.weights = self.weights - (derr_dw * self.learning_rate)
        self.error = self.costfn(layer2, result)

    def train(self, iterations = 1000):
        """
        trains the neural network using back propagation and updates the errors 

        Parameters 
        ----------
        iterations: int, optional 
            the number of training cycles (default 1000)

        """
        for iter in range(iterations):
            random_sample = np.random.randint(len(self.inputs))
            sample = self.inputs.iloc[random_sample]
            result = self.outputs.iloc[random_sample]

            self.back_propagation(sample, result)

            self.errhistory.append(np.abs(self.error))
                              
    def predict(self, inp):
        """
        performs a prediction using the trained neural network 

        Parameters 
        ----------
        inp: pandas dataframe 
            a set of inputs for the upcoming game 

        Returns 
        ----------
        l2: float 
            the calculated result 
        self.error: float 
            the mean squared error in the calculated value 
        
        """
        l1 = np.dot(inp, self.weights) + self.bias 
        l2 = self.sigmoid_fn(l1)
        return l2, self.error

def neural_inputs(final, y):
    """
    Splits the categories of data into the inputs (X) and ouput (Y) for ML. 

    Parameters 
    ----------
    final: pandas dataframe 
        The training dataset 
    y: str 
        the target stat to be computed 

    Returns 
    ----------
    X: list 
        the input variables 
    Y: list 
        the desired output variable 
    
    """
    X = final[['home', 'Atlanta Hawks',
        'Charlotte Hornets', 'Denver Nuggets', 'Golden State Warriors',
        'Houston Rockets', 'LA Clippers', 'Los Angeles Lakers',
        'Memphis Grizzlies', 'Miami Heat', 'Milwaukee Bucks',
        'Minnesota Timberwolves', 'New Orleans Pelicans',
        'Oklahoma City Thunder', 'Phoenix Suns', 'Sacramento Kings',
        'San Antonio Spurs', 'Toronto Raptors', 'Utah Jazz', 'Boston Celtics',
        'Brooklyn Nets', 'Chicago Bulls', 'Cleveland Cavaliers',
        'Dallas Mavericks', 'Detroit Pistons', 'Indiana Pacers',
        'New York Knicks', 'Orlando Magic', 'Philadelphia 76ers',
        'Portland Trail Blazers', 'Washington Wizards', 'pts-1', 'pts-2',
        'pts-3', 'pts-4', 'pts-5', 'reb-1', 'reb-2', 'reb-3', 'reb-4', 'reb-5',
        'ast-1', 'ast-2', 'ast-3', 'ast-4', 'ast-5']]
        
    Y = final[y]

    return X, Y

def predict_nn(final, next_game, player, date):

    """
    Trains and predicts using the simple neural network for each statistic. 

    Parameters 
    ----------
    final: pandas dataframe 
        The training dataset 
    next_game: pandas dataframe 
        the organized information about the next game 
    player: class obj 
        the player's information 
    date: str 
        the game date 

    Returns 
    ----------
    df_final: pandas dataframe 
        the results of each neural network prediction 
    
    """

    result = []
    errors = []

    for i in ['pts', 'reb', 'ast']:

        X, y = neural_inputs(final, i)
        nn = NeuralNet(X, y * (1/(1.1*np.max(y)))) # normalize it by a little more than the max so it can get higher than the max 
        nn.train()

        r, err = nn.predict(next_game)

        result.append(r * np.max(y) * 1.1)
        errors.append(err)

    results = {'Player': player.name, 'Date': date, 'Team': player.team, 'Pts': [result[0][0]], 'Reb': [result[1][0]], 'Ast':[result[2][0]],
        'Error in Pts': [errors[0]], 'Error in Reb': [errors[1]], 'Error in Ast': [errors[2]]
    }

    df_final = pd.DataFrame(results)
    return df_final


