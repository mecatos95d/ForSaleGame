from Server import *

players = []
for i in range(6):
	players.append(Player())

print("len (players) =", len(players))
test_game = Game(players)
print(test_game.__gid__)