from sklearn import linear_model
from pymongo import MongoClient
import matplotlib.pyplot as plt

class Projection:

    def __init__(self, player_data, player):
        self.player_data = player_data
        self.player = player
        self.client = MongoClient()
        self.player_instance = self.client['players'][player]
        self.teams = self.client['teams']

    def determine_list(self, stat):
        if stat == 'points':
            features = ['opp_points', 'fg', 'ft', 'threes']
        elif stat == 'rebounds':
            features = ['opp_rebounds', 'off_reb_pct', 'def_reb_pct', 'fg_missed']
        elif stat == 'assists':
            features = ['opp_assists', 'ast_pos']
        elif stat == 'steals':
            features = ['opp_steals', 'stl_pct']
        elif stat == 'blocks':
            features = ['opp_blocks', 'block_pct']
        elif stat == 'tpm':
            features = ['opp_threes', 'pct_from_threes', 'threes']
        elif stat == 'turnovers':
            features = ['opp_tos', 'to_pos']
        return features


    def project(self, stat):

        features = self.determine_list(stat)

        is_home = self.player_instance.find()[0]['home']
        try:
            mpg = self.player_instance.find()[0]['mpg']
        except KeyError:
            return 0
        position = self.player_instance.find()[0]['pos1']

        data = []
        value = []

        for key in self.player_data:
            if is_home == self.player_data[key]['home']:

                mins = self.player_data[key]['min']
                if mins == '0':
                    continue
                team = self.player_data[key]['team'].strip()

                if team not in ['GS', 'LAL', 'LAC', 'NO', 'NY', 'SA']:
                    team = team.title()

                #print key, team

                if team == 'Phx':
                    team = 'Pho'

                if team == 'Wsh':
                    team = 'Was'

                team_instance = self.teams[team]

                if is_home:
                    try:
                        team_data = team_instance.find()[0]['away']
                    except IndexError:
                        continue
                else:
                    try:
                        team_data = team_instance.find()[0]['home']
                    except IndexError:
                        continue

                temp_list = []
                temp_list.append(float(mins))
                temp_list.append(float(team_data['possessions']))
                temp_list.append(float(team_instance.find()[0]['positionstats'][position][features[0]]))

                for i in range(1, len(features)):
                    temp_list.append(float(team_data[features[i]]))

                data.append(temp_list)
                value.append(float(self.player_data[key][stat]))

        regr = linear_model.LinearRegression()
        regr.fit(data, value)

        current_team = self.player_instance.find()[0]['opp_team']
        team_instance = self.teams[current_team]

        predict_list = []
        predict_list.append(float(mins))
        predict_list.append(float(team_data['possessions']))
        predict_list.append(float(team_instance.find()[0]['positionstats'][position][features[0]]))

        for i in range(1, len(features)):
            predict_list.append(float(team_data[features[i]]))

        return regr.predict([predict_list])[0]

    def close(self):
        self.client.close()

