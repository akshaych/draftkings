from sklearn import linear_model
from pymongo import MongoClient
import csv

class Projection:

    def __init__(self, player_data, player):
        self.player_data = player_data
        self.player = player
        self.client = MongoClient()
        self.player_instance = self.client['players'][player]
        self.teams = self.client['teams']


    def project_points(self):

        #check if home or away
        is_home = self.player_instance.find()[0]['home']
        mpg = self.player_instance.find()[0]['mpg']
        position = self.player_instance.find()[0]['pos1']

        print is_home, mpg, position

        points_data = []
        points_value = []

        for key in self.player_data:
            if is_home == self.player_data[key]['home']:

                mins = self.player_data[key]['min']
                # ftm = self.player_data[key]['ftm']
                # fgm = self.player_data[key]['fgm']
                # tpm = self.player_data[key]['tpm']

                team = self.player_data[key]['team']
                team_instance = self.teams[team]

                points_allowed = team_instance.find()[0]['positionstats'][position]['opp_points']

                if is_home:
                    team_data = team_instance.find()[0]['away']
                else:
                    team_data = team_instance.find()[0]['home']

                opp_fg = team_data['fg']
                opp_ft = team_data['ft']
                opp_three = team_data['threes']
                pace = team_data['possessions']
                points = self.player_data[key]['points']

                points_data.append([mins, points_allowed, opp_fg, opp_ft, opp_three, pace])
                points_value.append(points)

        regr = linear_model.LinearRegression()
        regr.fit()

        current_team = self.player_instance.find()[0]['opp_team']
        team_instance = self.teams[current_team]

        points_allowed = team_instance.find()[0]['positionstats'][position]['opp_points']

        if is_home:
            team_data = team_instance.find()[0]['away']
        else:
            team_data = team_instance.find()[0]['home']

        opp_fg = team_data['fg']
        opp_ft = team_data['ft']
        opp_three = team_data['threes']
        pace = team_data['possessions']

        return regr.predict([[mpg, points_allowed, opp_fg, opp_ft, opp_three, pace]])



