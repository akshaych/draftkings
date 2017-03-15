from bs4 import BeautifulSoup
import requests
import sys
from pymongo import MongoClient

class Initialize():

    def __init__(self):
        reload(sys)
        sys.setdefaultencoding('utf8')

    # get url, eventually dynamically find
    def retrieve_url(self):
        self.url = "https://www.draftkings.com/lineup/getavailableplayers?draftGroupId=12551"
        return

    #assign players to teams
    def assign_teams(self):
        lm_json = requests.get(self.url).json()
        client = MongoClient()
        players = client['players']
        team_list = []
        player_list = []
        out = False

        for row in lm_json['playerList']:

            name = row['fnu'] + row['lnu']
            if "Jr." in row['lnu']:
                idx = row['lnu'].find("Jr.")
                name = row['fnu'] + row['lnu'][0:idx]
            elif "Sr." in row['lnu']:
                idx = row['lnu'].find("Sr.")
                name = row['fnu']+ row['lnu'][0:idx]

            player_instance = players[name]
            player_list.append(name)

            team = ""
            opp_team = ""
            player_link = ""

            #print (row['lnu'])
            both_teams = [row['htabbr'], row['atabbr']]
            if row['htabbr'] == 'Uta':
                both_teams[0] = 'Utah'
            elif row['atabbr'] == 'Uta':
                both_teams[1] = 'Utah'

            # get team and player urls for further data collection
            for poss_team in both_teams:
                team_url = 'https://www.espn.com/nba/teams/roster?team=' + poss_team
                page = requests.get(team_url)
                soup = BeautifulSoup(page.content, 'html.parser')

                result = soup.find("a", text=row['fnu'] + ' ' + row['lnu'])

                #dealing with all anomaly players , eventually fix with regex
                if row['fnu'] == 'Guillermo':
                    result = soup.find("a", text="Willy " + row['lnu'])

                if row['fnu'] == 'Luc Richard':
                    result = soup.find("a", text="Luc " + row['lnu'])

                if row['fnu'] == 'Frank' and row['lnu'] == 'Kaminsky':
                    result = soup.find("a", text=row['fnu'] + ' Kaminsky III')

                if row['fnu'] == 'Otto':
                    result = soup.find("a", text=row['fnu'] + ' ' + row['lnu'] + ' Jr.')

                if row['lnu'] == 'Bembry':
                    result = soup.find("a", text="DeAndre " + row['lnu'])

                if row['fnu'] == 'C.J.' and row['lnu'] == 'Wilcox':
                    result = soup.find("a", text = 'CJ ' + row['lnu'])

                if row['fnu'] == 'Stephen' and row['lnu'] == 'Zimmerman Jr.':
                    result = soup.find("a", text = 'Stephen Zimmerman')

                if result:
                    team = poss_team
                    player_link = result['href']
                    break

            # determine opposing team
            if team == both_teams[0]:
                opp_team = both_teams[1]
                home = True
            elif team == both_teams[1]:
                opp_team = both_teams[0]
                home = False

            #add teams to team list
            if team not in team_list:
                print team
                print name
                team_list.append(team)

            # get possible positions of player
            if '/' in row['pn']:
                pos1 = row['pn'].split('/')[0]
                pos2 = row['pn'].split('/')[1]
            else:
                pos1 = row['pn']
                pos2 = 'None'

            if row['i'] == "Out":
                out = True

            teams = client['teams']
            team_instance = teams[team]

            team_instance.update_one({'team': team}, {'$addToSet': {'players.' + pos1: name},
                                                      "$currentDate": {"lastModified": True}}, upsert=True)

            if pos2 != 'None':
                team_instance.update_one({'team': team}, {'$addToSet': {'players.' + pos2: name},
                                                          "$currentDate": {"lastModified": True}}, upsert=True)

            rslt = player_instance.update_one({"name":name},
                                              {"$set":{"team":team, "opp_team":opp_team, "salary":row['s'],
                                                       "player_link":player_link, "pos1":pos1, "pos2" : pos2, "home":home, "out": out}
                                                        ,"$currentDate": {"lastModified": True}}, upsert=True)

        client.close()
        return team_list, player_list


