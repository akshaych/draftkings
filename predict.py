import initial
import update

init = initial.Initialize()
init.retrieve_url()
team_list, player_list = init.assign_teams()

team_update = update.TeamUpdate(team_list)
team_update.update_teams()

test2 = update.PlayerUpdate(player_list)
test2.update_player()