import update
import regression
from pymongo import MongoClient


#test = update.TeamUpdate(['Hou'])
#test.update_teams()
#
# test2 = update.PlayerUpdate(['JaylenBrown'])
# test2.update_player()

client = MongoClient()
players = client['players']

for player in ["DirkNowitzki"]:
    player_instance = players[player]
    player_data = player_instance.find()[0]['stats']
    projection = regression.Projection(player_data, player)
    print projection.project('points')
    print projection.project('rebounds')
    print projection.project('assists')
    print projection.project('steals')
    print projection.project('blocks')
    print projection.project('tpm')
    print projection.project('turnovers')

client.close()

