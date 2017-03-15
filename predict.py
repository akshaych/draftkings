import initial
import update

init = initial.Initialize()
init.retrieve_url()
lists = init.assign_teams()

team_update = update.TeamUpdate(lists[0])
team_update.update_teams()

test2 = update.PlayerUpdate(['JamesHarden'])
test2.update_player()