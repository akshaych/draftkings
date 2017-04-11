import initial
import update
import regression
import csv
from operator import itemgetter
from pymongo import MongoClient
from twilio.rest import Client
import operator

init = initial.Initialize()
init.retrieve_url()
team_list, player_list = init.assign_teams()

print team_list

team_update = update.TeamUpdate(team_list)
team_update.update_teams()

test2 = update.PlayerUpdate(player_list)
test2.update_player()

client = MongoClient()
players = client['players']

projected_players = []
for player in player_list:
    player_instance = players[player]

    player_data = player_instance.find()[0]['stats']
    projection = regression.Projection(player_data, player)
    proj_list = []
    proj_list.append(projection.project('points'))
    proj_list.append(projection.project('rebounds'))
    proj_list.append(projection.project('assists'))
    proj_list.append(projection.project('steals'))
    proj_list.append(projection.project('blocks'))
    proj_list.append(projection.project('tpm'))
    proj_list.append(projection.project('turnovers'))

    count = 0

    for proj in proj_list:
        if proj == 'turnovers':
            continue
        if proj > 10:
            count += 1

    projection = proj_list[0] + 1.25 * proj_list[1] + 1.5 * proj_list[2] + 2 * proj_list[3] \
                 + 2 * proj_list[4] + .5 * proj_list[5] - .5 * proj_list[6]

    if count > 2:
        projection += 3
    elif count > 1:
        projection += 1.5


    salary = player_instance.find()[0]['salary']
    projected_players.append([player, projection, salary])

projected_players = sorted(projected_players, key = itemgetter(1), reverse=True)

message = ""

client.close()
with open('projections.csv', 'w') as csvfile:
    for projection in projected_players:
        fieldnames = ['player', 'projection', 'salary', 'value']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'player':projection[0], 'projection':projection[1], 'salary':projection[2], ''
                                                                                                     'value': projection[1] / projection[2]})

reader = csv.reader(open("files.csv"), delimiter=",")
sortedlist = sorted(reader, key=operator.itemgetter(3), reverse=True)


for i in range(0, 15):
    message = message + " " + sortedlist[i][0]

account_sid = "ACaa446eaf63a0b41917e88f80edbfee18"
#replaced for privacy
auth_token = "///////////////////////////"

client = Client(account_sid, auth_token)

#send out final output to people who want the results
final_message =  client.messages.create(
    to="+14089665979",
    from_="+14089665979",
    body=message)

