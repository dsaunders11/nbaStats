import requests 
import json

class Player():
    def __init__(self, name, season='2021'):
        """
        Define some class variables and run some methods to gather player information. 

        Parameters 
        ----------
        name: str
            player name 
        season: str (optional)
            the NBA season (default 2021)
        
        """
        self.name = name
        self.season = season

        self.id, self.team_id = self.get_player_id()

        self.team = self.get_team_name()

        self.stats = self.get_player_stats()
        
    def get_player_id(self):
        """
        Uses an API search on balldontlie.io to get the unique ID for a given player. 

        Returns 
        ----------
        id: int
            the player's unique ID 
        team_id: int 
            the unique ID of the player's team 
        
        """
        url = 'https://www.balldontlie.io/api/v1/players'
        qwst = {'search':self.name}
        response = requests.get(url, params=qwst)
        data = response.text
        parse_json = json.loads(data)
        id = parse_json['data'][0]['id']
        team_id = parse_json['data'][0]['team']['id']

        return id, team_id
    def get_team_name(self):
        """
        Use an API search on balldontlie.io to identify the player's team name from the ID. 

        Returns 
        ----------
        team: str 
            the team of the given player 
        
        """
        url = 'https://www.balldontlie.io/api/v1/teams/'
        response = requests.get(url)
        data = response.text
        parse_json = json.loads(data)
        team = parse_json['data'][self.team_id-1]['full_name']
        
        return team 
    def get_player_stats(self):
        """
        Gets the seasons stats for the specified player. 

        Returns 
        ----------
        stats_season: list 
            the stats for the given player on the given season (up to the current date)
        
        """
        # https://www.balldontlie.io/#get-all-stats
        url = "https://www.balldontlie.io/api/v1/stats"
        
        querystring = {"seasons[]":self.season,"player_ids[]":self.id}

        response = requests.get(url, params=querystring)
        data = response.text
        parse_json = json.loads(data)
        
        stats_season = [parse_json['data'][i] for i in range(len(parse_json['data']))]
        
        return stats_season
    def playoff_stats(self):
        """
        Gets the playoff stats for a given player in a particular season. 

        Returns 
        ----------
        stats_playoff: list 
            the stats for the given player on the given playoff run (up to the current date)
        
        """
        url = "https://www.balldontlie.io/api/v1/stats"
        
        querystring = {"seasons[]":self.season,"player_ids[]":self.id, "postseason[]":True}

        response = requests.get(url, params=querystring)
        data = response.text
        parse_json = json.loads(data)
        
        stats_playoff = [parse_json['data'][i] for i in range(len(parse_json['data']))]
        
        return stats_playoff
    def get_future_game(self,date):
        """
        Searches for the next game a player will play based on the inputted date. 

        Parameters 
        ----------
        date: str 
            the current date (or specified date)

        Returns 
        ----------
        upcoming: list 
            information from balldontlie.io API on an upcoming game  
        
        """
        url3 = 'https://www.balldontlie.io/api/v1/games'
        qwst3 = {'start_date': date, 'team_ids[]':self.team_id}
        response = requests.get(url3, params=qwst3)
        data = response.text
        parse_json = json.loads(data)

        dates = [] # getting the next date properly 

        for game in parse_json['data']:
            dates.append(game['date'][:10])

        date_new = sorted(dates)[0] + "T00:00:00.000Z"

        for game in parse_json['data']:
            if game['date'] == date_new:
                upcoming = game

        return upcoming 

def get_team_name(team_id): # sometimes this has to be done generally 
    """
    Use an API search on balldontlie.io to identify the player's team name from the ID. 

    Parameters
    ----------
    team_id: int 
        the unique ID of the player's team 

    Returns 
    ----------
    team_name: str 
        the team of the given player 
        
    """
    url = 'https://www.balldontlie.io/api/v1/teams/'
    response = requests.get(url)
    data = response.text
    parse_json = json.loads(data)
    
    team_name = parse_json['data'][team_id-1]['full_name']
    return team_name