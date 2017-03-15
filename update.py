from bs4 import BeautifulSoup
import requests
import sys
from pymongo import MongoClient


class TeamUpdate:

    def __init__(self, team_list):
        #self.team_list = team_list
        self.team_list = ['Hou', 'Utah', 'Min', 'LAC', 'NO', 'Tor', 'Mil', 'NY', 'Ind', 'Det', 'Bos', 'Bkn', 'Phi',
                          'Chi', 'Cle', 'Atl', 'Mia', 'Orl', 'Was', 'Cha', 'Den', 'Okc', 'Por', 'GS',
                          'LAL', 'Pho', 'Sac', 'Dal', 'Mem', 'SA']
        self.teamranking_map = {'Bos': 'Boston', 'Bkn': 'Brooklyn', 'NY': 'New York', 'Phi': 'Philadelphia', 'Tor':'Toronto',
                                'Chi': 'Chicago', 'Cle': 'Cleveland', 'Det': 'Detroit', 'Ind': 'Indiana', 'Mil': 'Milwaukee',
                                'Atl': 'Atlanta', 'Cha':'Charlotte', 'Mia': 'Miami', 'Orl': 'Orlando', 'Was': 'Washington',
                                'Den': 'Denver', 'Min':'Minnesota', 'Okc':'Okla City', 'Por': 'Portland', 'Utah': 'Utah',
                                'GS': 'Golden State', 'LAC': 'LA Clippers', 'LAL': 'LA Lakers', 'Pho': 'Phoenix', 'Sac': 'Sacramento',
                                'Dal': 'Dallas', 'Hou': 'Houston', 'NO': 'New Orleans', 'Mem': 'Memphis', 'SA': 'San Antonio'}
        self.roto_map = {'Bos': 'Boston Celtics', 'Bkn': 'Brooklyn Nets', 'NY': 'New York Knicks', 'Phi': 'Philadelphia 76ers',
                         'Tor':'Toronto Raptors', 'Chi': 'Chicago Bulls', 'Cle': 'Cleveland Cavaliers', 'Det': 'Detroit Pistons',
                         'Ind': 'Indiana Pacers', 'Mil': 'Milwaukee Bucks', 'Atl': 'Atlanta Hawks', 'Cha':'Charlotte Hornets',
                         'Mia': 'Miami Heat', 'Orl': 'Orlando Magic', 'Was': 'Washington Wizards', 'Den': 'Denver Nuggets',
                         'Min':'Minnesota Timberwolves', 'Okc':'Oklahoma City Thunder', 'Por': 'Portland Trailblazers',
                         'Utah': 'Utah Jazz', 'GS': 'Golden State Warriors', 'LAC': 'Los Angeles Clippers', 'LAL': 'Los Angeles Lakers',
                         'Pho': 'Phoenix Suns', 'Sac': 'Sacramento Kings', 'Dal': 'Dallas Mavericks', 'Hou': 'Houston Rockets',
                         'NO': 'New Orleans Pelicans', 'Mem': 'Memphis Grizzlies', 'SA': 'San Antonio Spurs'}

    def update_teams(self):
        client = MongoClient()
        teams = client['teams']

        #stats needed for points are opp ft, opp 3 and opp 2
        urls = ['https://www.teamrankings.com/nba/stat/possessions-per-game',
                'https://www.teamrankings.com/nba/stat/opponent-three-pointers-attempted-per-game',
                'https://www.teamrankings.com/nba/stat/opponent-field-goals-attempted-per-game',
                'https://www.teamrankings.com/nba/stat/opponent-free-throws-attempted-per-game',
                'https://www.teamrankings.com/nba/stat/offensive-rebounding-pct',
                'https://www.teamrankings.com/nba/stat/defensive-rebounding-pct',
                'https://www.teamrankings.com/nba/stat/opponent-field-goals-made-per-game',
                'https://www.teamrankings.com/nba/stat/opponent-three-pointers-made-per-game',
                'https://www.teamrankings.com/nba/stat/opponent-assists-per-possession',
                'https://www.teamrankings.com/nba/stat/opponent-percent-of-points-from-3-pointers',
                'https://www.teamrankings.com/nba/stat/opponent-turnovers-per-possession',
                'https://www.teamrankings.com/nba/stat/opponent-block-pct',
                'https://www.teamrankings.com/nba/stat/opponent-steals-perpossession'
                ]

        keys = ['possessions', 'threes', 'fg', 'ft', 'off_reb_pct', 'def_reb_pct', 'fg_missed', 'threes_missed',
                'ast_pos', 'pct_from_threes', 'to_pos', 'block_pct', 'stl_pct']

        positions = ['PG', 'SG', 'G', 'SF', 'PF', 'F', 'C']
        roto_url = 'http://www.rotowire.com/daily/nba/defense-vspos.php?site=DraftKings&astatview=season&pos='
        count = 0
        self.fgcount_away = {}
        self.fgcount_home = {}
        self.threecount_away = {}
        self.threecount_home = {}

        for url in urls:
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            table = soup.find("table").find("tbody").find_all("tr")
            for row in table:
                labels = row.find_all("td")
                for team in self.team_list:
                    if labels[1].get_text() == self.teamranking_map[team]:

                        team_instance = teams[team]

                        home_value = labels[5].get_text().split("%")[0]
                        away_value = labels[6].get_text().split("%")[0]

                        if url == 'https://www.teamrankings.com/nba/stat/opponent-field-goals-attempted-per-game':
                            self.fgcount_away[team] = away_value
                            self.fgcount_home[team] = home_value

                        if url == 'https://www.teamrankings.com/nba/stat/opponent-three-pointers-attempted-per-game':
                            self.threecount_away[team] = away_value
                            self.threecount_home[team] = home_value

                        if url == 'https://www.teamrankings.com/nba/stat/opponent-field-goals-made-per-game':
                            away_value = float(self.fgcount_away[team]) - float(away_value)
                            home_value = float(self.fgcount_home[team]) - float(home_value)

                        if url == 'https://www.teamrankings.com/nba/stat/opponent-three-pointers-made-per-game':
                            away_value = float(self.threecount_away[team]) - float(away_value)
                            home_value = float(self.threecount_home[team]) - float(home_value)

                        if url == 'https://www.teamrankings.com/nba/stat/opponent-assists-per-possession':
                            away_value = away_value[2] + '.' + away_value[3] + away_value[4]
                            home_value = home_value[2] + '.' + home_value[3] + home_value[4]

                        team_instance.update_one({'team':team}, {'$set': {'away.' + keys[count]: away_value},
                                                 "$currentDate": {"lastModified": True}}, upsert = True)
                        team_instance.update_one({'team':team}, {'$set': {'home.' + keys[count]: home_value},
                                                                 "$currentDate": {"lastModified": True}}, upsert=True)

            count += 1

        for pos in positions:
            page = requests.get(roto_url + pos)
            soup = BeautifulSoup(page.content, 'html.parser')
            table = soup.find("table").find("tbody").find_all("tr")
            roto_keys = ['opp_points', 'opp_rebounds', 'opp_assists', 'opp_steals', 'opp_blocks', 'opp_threes',
                             'opp_fg', 'opp_ft', 'opp_tos']
            count = 5

            for row in table:
                labels = row.find_all("td")
                for team_name in self.team_list:
                    if labels[0].get_text() == self.roto_map[team]:
                        for key in roto_keys:
                            team_instance = teams[team_name]
                            team_instance.update_one({'team': team_name}, {'$set': {'positionstats.' + pos + '.' + key: labels[count].get_text()},
                                                         "$currentDate": {"lastModified": True}}, upsert=True)
                            count += 1
                    count = 5

        client.close()


class PlayerUpdate:

    def __init__(self, player_list):
        self.player_list = player_list

    def update_player(self):
        client = MongoClient()
        players = client['players']

        for player in self.player_list:
            player_instance = players[player]

            profile_url = player_instance.find({},{'player_link':1}).__getitem__(0)['player_link']

            page = requests.get(profile_url)
            soup = BeautifulSoup(page.content, 'html.parser')
            table = soup.find('table', class_ = 'tablehead').find_all("tr")

            for row in table:
                print row