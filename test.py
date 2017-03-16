import update
import regression
from pymongo import MongoClient


#test = update.TeamUpdate(['Hou'])
#test.update_teams()

#test2 = update.PlayerUpdate(['JaylenBrown'])
#test2.update_player()

client = MongoClient()
players = client['players']

for player in ['JaylenBrown']:
    player_instance = players[player]
    data = player_instance.find()
    print data