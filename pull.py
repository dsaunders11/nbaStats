import requests 
import json

class Player():
    def __init__(self, name, season='2021'):
        self.name = name
        self.season = season

        self.id, self.team_id = self.get_player_id()

        self.team = self.get_team_name()

        self.stats = self.get_player_stats()
        
    def get_player_id(self):
        url = 'https://www.balldontlie.io/api/v1/players'
        qwst = {'search':self.name}
        response = requests.get(url, params=qwst)
        data = response.text
        parse_json = json.loads(data)
        id = parse_json['data'][0]['id']
        team_id = parse_json['data'][0]['team']['id']

        return id, team_id
    def get_team_name(self):
        url = f'https://www.balldontlie.io/api/v1/teams/'
        response = requests.get(url)
        data = response.text
        parse_json = json.loads(data)
        team = parse_json['data'][self.team_id-1]['full_name']
        
        return team 
    def get_player_stats(self):
        # https://www.balldontlie.io/#get-all-stats
        url = "https://www.balldontlie.io/api/v1/stats"
        
        querystring = {"seasons[]":self.season,"player_ids[]":self.id}

        response = requests.get(url, params=querystring)
        data = response.text
        parse_json = json.loads(data)
        
        stats_season = [parse_json['data'][i] for i in range(len(parse_json['data']))]
        
        return stats_season
    def playoff_stats(self):
        url = "https://www.balldontlie.io/api/v1/stats"
        
        querystring = {"seasons[]":self.season,"player_ids[]":self.id, "postseason[]":True}

        response = requests.get(url, params=querystring)
        data = response.text
        parse_json = json.loads(data)
        
        stats_playoff = [parse_json['data'][i] for i in range(len(parse_json['data']))]
        
        return stats_playoff
    def get_future_game(self,date):
        url3 = 'https://www.balldontlie.io/api/v1/games'
        date = '2021-11-18'
        qwst3 = {'start_date': date, 'end_date': date, 'team_ids[]':self.team_id}
        response = requests.get(url3, params=qwst3)
        data = response.text
        parse_json = json.loads(data)

        upcoming = parse_json['data'][0]

        return upcoming 

def get_team_name(team_id): # sometimes this has to be done generally 
    url = f'https://www.balldontlie.io/api/v1/teams/'
    response = requests.get(url)
    data = response.text
    parse_json = json.loads(data)
    
    team_name = parse_json['data'][team_id-1]['full_name']
    return team_name