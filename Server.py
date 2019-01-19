import Const
from Player import Player
from Card import Card

import random
import sys

# Player Number + Turns = 11 (3P = 8Turns, 4P = 7Turns, 5P = 6Turns, 6P = 5Turns)

class Game:
	def __init__(self, players):
		self.__gid__ = Const.gid
		Const.gid += 1
		for player in players:
			pass # If type is not "Player", Error warn!
		if len(players) < 3 or len(players) > 6:
			print("Not enough players : ", len(players))

		#### All-verified case
		self.__players__ = players
		self.__size__ = len(self.__players__)

		# If setting is completed
		self.__estate__ = []
		for price in range(1, 31): # 1-30
			self.__estate__.append(Card(price))

		self.__money__ = []
		for dup in range(2):
			self.__money__.append(Card(0))
			for price in range(2, 16): # 0 & 2-15
				self.__money__.append(Card(price))

		random.shuffle(self.__estate__)
		random.shuffle(self.__money__)
		
		if Const.DPO:
			print("Game Run -", self.__gid__)
			print("Player List...")
			for p in self.__players__:
				print("Player : ", p.pid)			

		self.play()

	def play(self):
		for turn in range(1, 12-self.__size__):
			self.turn_estate(turn) # Begin code is currently fixed.
		for turn in range(1, 12-self.__size__):
			self.turn_money(turn)

	# Turn : 1~8(3P case).
	# Begin : begin user indicator code. Currently unused.
	def turn_estate(self, turn, begin = 0):
		if Const.DPO:
			print("Playing Turn Estate #", turn)
		# Verification layer
		if self.__size__ * (12-self.__size__-turn) != len(self.__estate__):
			print("Critical error : Improper estate container global,", 30 - self.__size__ * (turn-1), "!=", len(self.__estate__))
		if self.__size__ * (11-self.__size__) != len(self.__money__):
			print("Critical error : Improper money container global, 30 !=", len(self.__estate__))
		for player in self.__players__:
			if turn - len(player.__estate__) != 1: # Error - estate length different
				print("Critical error : Improper estate container,", player.name, turn, "!=", len(player.__estate__))
				# Exit & Recovery protocol
			if 0 != len(player.__money__):
				print("Critical error : Improper money container,", player.name, "0 !=", len(player.__money__))

		### Verification finished
		
		market = [] # Candidate cards. Save with sorted states.
		for i in range(self.__size__):
			market.append(self.__estate__.pop())
		market.sort()
		
		price = 0 # Bidding price
		bidder = self.__players__[::-1] # Reverse - to use pop & insert
		player = bidder.pop()

		while 1 != len(bidder):
			result = player.turn() # new-bet case
			if 1 == result: # DIe
				pass
			elif 2 == result: # Newly bet
				bidder.insert(player, 0)
			else: # Wrong code return
				print("Error #5 WrongCodeSTE : ", self.gid, player.pid, result)
				sys.exit(0)

		### Card distribution
		
		### Next begin user return
		return begin # Currently, fixed begin user.
