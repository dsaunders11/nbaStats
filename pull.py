import requests 
import json

class Player():
    def __init__(self, name, season='2021'):
        self.name = name
        self.season = season
    def get_player_id(self):
        url = 'https://www.balldontlie.io/api/v1/players'
        qwst = {'search':player}
        response = requests.get(url, params=qwst)
        data = response.text
        parse_json = json.loads(data)
        self.id = parse_json['data'][0]['id']
        self.team_id = parse_json['data'][0]['team']['id']
    def get_team_name(self):
        url = f'https://www.balldontlie.io/api/v1/teams/'
        response = requests.get(url)
        data = response.text
        parse_json = json.loads(data)
        self.team = parse_json['data'][self.team_id-1]['full_name']
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

def get_future_game(date):
    url3 = 'https://www.balldontlie.io/api/v1/games'
    date = '2021-11-18'
    qwst3 = {'start_date': date, 'end_date': date, 'team_ids[]':team_id}
    response = requests.get(url3, params=qwst3)
    data = response.text
    parse_json = json.loads(data)

    upcoming = parse_json['data'][0]

    return upcoming 