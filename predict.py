import initial
import update
import regression
import csv
from operator import itemgetter
from pymongo import MongoClient

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
team_list = [u'Hou', u'Min', u'NO', u'Mil', u'Was', u'Chi', u'Bos', u'Mia', u'Tor', u'Phi', u'Orl', u'LAL', u'Pho', u'Det', u'Bkn', u'Dal']
for player in [u'JamesHarden', u'Karl-AnthonyTowns', u'AnthonyDavis', u'GiannisAntetokounmpo', u'DeMarcusCousins', u'JohnWall', u'JimmyButler', u'IsaiahThomas', u'BradleyBeal', u'HassanWhiteside', u'DeMarDeRozan', u'DarioSaric', u'ElfridPayton', u'RickyRubio', u'KyleLowry', u'NikolaVucevic', u'JuliusRandle', u'GoranDragic', u'DevinBooker', u'AndreDrummond', u'EricBledsoe', u'RobertCovington', u'BrookLopez', u'DionWaiters', u'AndrewWiggins', u'JrueHoliday', u'T.J.Warren', u'RajonRondo', u'OttoPorter', u"D'AngeloRussell", u'KhrisMiddleton', u'DirkNowitzki', u'HarrisonBarnes', u'AlanWilliams', u'DwyaneWade', u'AlHorford', u'MarkieffMorris', u'JeremyLin', u'AveryBradley', u'SergeIbaka', u'JordanClarkson', u'TobiasHarris', u'SethCurry', u'GregMonroe', u'LouWilliams', u'EvanFournier', u'TylerUlis', u'AaronGordon', u'JamesJohnson', u'PatrickBeverley', u'NerlensNoel', u'ClintCapela', u'JaeCrowder', u'ReggieJackson', u'IvicaZubac', u'KentaviousCaldwell-Pope', u'MarcusMorris', u'T.J.McConnell', u'JahlilOkafor', u'MarqueseChriss', u'TylerJohnson', u'TrevorAriza', u'GorguiDieng', u'RichaunHolmes', u'MalcolmBrogdon', u'TrevorBooker', u'JonasValanciunas', u'MarcinGortat', u'EricGordon', u'BrandonIngram', u'MarcusSmart', u'WesleyMatthews', u'CoryJoseph', u'TerrenceRoss', u'SeanKilpatrick', u'NemanjaBjelica', u'NormanPowell', u'BojanBogdanovic', u'YogiFerrell', u'RyanAnderson', u'BismackBiyombo', u'JordanCrawford', u'MichaelBeasley', u'NikolaMirotic', u'JoshRichardson', u'CarisLeVert', u'IshSmith', u'DenzelValentine', u'KellyOlynyk', u'RondaeHollis-Jefferson', u'JonLeuer', u'BrandonJennings', u'RobinLopez', u'AlexLen', u'TonySnell', u'LarryNance ', u'JaylenBrown', u'BobbyPortis', u'WayneEllington', u'NeneHilario', u'MatthewDellavedova', u'IsaiahWhitehead', u'MichaelCarter-Williams', u'SpencerDinwiddie', u'AmirJohnson', u'DeMarreCarroll', u'ShabazzMuhammad', u'WillieReed', u'J.J.Barea', u'NickYoung', u'ArchieGoodwin', u'P.J.Tucker', u'GeraldHenderson', u'AronBaynes', u'TimotheLuwawu-Cabarrot', u'JustinAnderson', u"E'TwaunMoore", u'SamDekker', u'BrandonKnight', u'JerianGrant', u'TomasSatoransky', u'IanMahinmi', u'NikStauskas', u'TimFrazier', u'QuincyAcy', u'SergioRodriguez', u'DanteCunningham', u'SolomonHill', u'LeandroBarbosa', u'JeffGreen', u'StanleyJohnson', u'JohnHenson', u'DemetriusJackson', u'TerryRozier', u'RandyFoye', u'JamesYoung', u'GeraldGreen', u'JoeHarris', u'K.J.McDaniels', u'AndrewNicholson', u'JonasJerebko', u'JordanMickey', u'JustinHamilton', u'TylerZeller', u'BenoUdrih', u'FredVanVleet', u'DelonWright', u'ReggieBullock', u'DarrunHilliard', u'MichaelGbinije', u'BrunoCaboclo', u'PatrickPatterson', u'LucasNogueira', u'PascalSiakam', u'HenryEllenson', u'BobanMarjanovic', u'JakobPoeltl', u'IsaiahCanaan', u'TreyBurke', u'CameronPayne', u'KellyOubre ', u'AnthonyMorrow', u'SheldonMcClellan', u'PaulZipser', u'JasonSmith', u'JoffreyLauvergne', u'ChrisMcCullough', u'DanielOchefu', u'CristianoFelicio', u'TyusJones', u'KrisDunn', u'RodneyMcGruder', u'BrandonRush', u'ZachLaVine', u'LanceStephenson', u'ChrisBosh', u'UdonisHaslem', u'JoshMcRoberts', u'JordanHill', u'LukeBabbitt', u'OkaroWhite', u'AdreianPayne', u'JustiseWinslow', u'ColeAldrich', u'NikolaPekovic', u'DevinHarris', u'JerrydBayless', u'BenSimmons', u'MannyHarris', u'NicolasBrussino', u'DorianFinney-Smith', u'ShawnLong', u'DwightPowell', u'JarrodUthoff', u'TiagoSplitter', u'SalahMejri', u'A.J.Hammons', u'JoelEmbiid', u'BobbyBrown', u'IsaiahTaylor', u'HollisThompson', u'TroyWilliams', u'WayneSelden ', u'QuincyPondexter', u'DonatasMotiejunas', u'KyleWiltjer', u'CheickDiallo', u'AlexisAjinca', u'OmerAsik', u'MontrezlHarrell', u'ChinanuOnuaku', u'C.J.Watson', u'RonniePrice', u'D.J.Augustin', u'JodieMeeks', u'C.J.Wilcox', u'JaredDudley', u'MarioHezonja', u'DerrickJones ', u'DamjanRudez', u'DraganBender', u'TysonChandler', u'StephenZimmerman ', u'TylerEnnis', u'JasonTerry', u'DavidNwaba', u'RashadVaughn', u'MettaWorld Peace', u'LuolDeng', u'CoreyBrewer', u'ThomasRobinson', u'TerrenceJones', u'MirzaTeletovic', u'JabariParker', u'SpencerHawes', u'TarikBlack', u'TimofeyMozgov', u'ThonMaker']:
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

client.close()
with open('projections.csv', 'w') as csvfile:
    for projection in projected_players:
        fieldnames = ['player', 'projection', 'salary']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'player':projection[0], 'projection':projection[1], 'salary':projection[2]})
