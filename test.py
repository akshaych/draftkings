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

for player in ['JaylenBrown']:
    player_instance = players[player]
    player_data = player_instance.find()[0]['stats']
    projection = regression.Projection(player_data, player)
    projected_points = projection.project_points()
    print projected_points

client.close()

