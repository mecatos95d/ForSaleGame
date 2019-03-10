import Const
from Player import Player
from Card import Card

import random
import sys

def get_lc(size):
	return max(0, 18 - 4 * size)

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
		self.__gl__ = 11 - self.__size__ # Game Length

		# If setting is completed
		self.__estate__ = []
		for price in range(1, 31): # 1-30
			self.__estate__.append(Card("Estate", price))

		self.__money__ = []
		for dup in range(2):
			self.__money__.append(Card("Money", 0))
			for price in range(2, 16): # 0 & 2-15
				self.__money__.append(Card("Money", price))

		random.shuffle(self.__estate__)
		random.shuffle(self.__money__)
		
		if Const.DPO:
			print("Game Run -", self.__gid__)
			print("Player List...")
			for p in self.__players__:
				print("Player :", p.pid)			

		self.play()

	def play(self):
		begin = 0
		for turn in range(self.__gl__):
			begin = self.turn_estate(turn, begin) # Begin code is currently fixed.
		for turn in range(self.__gl__):
			begin = self.turn_money(turn, begin) # Begin code is currently fixed.
		self.close()
	
	def verify(self, turn, mode): # mode = 9 for estate / mode = 1 for money turn
		if not mode in [0, 1]:
			print("Error #G0201 Wrong_Verify_Mode : ", self.__gid__, turn, mode)
			return False
		clear = True
		
		print(">>> Verification Begin - Mode", mode, "Turn", turn)
		spes = self.__gl__ * mode + turn * (1 - mode * 2) # Single - PEcS
		spms = mode * turn # Single - PMcS
		
		pecs = 30 - self.__size__ * spes # Proper Estate Container Size
		pmcs = 30 - self.__size__ * spms # Proper Money Container Size
		
		# Verification layer
		if pecs != len(self.__estate__):
			print("Critical error : Improper estate container global,", pecs, "!=", len(self.__estate__))
		if pmcs != len(self.__money__):
			print("Critical error : Improper money container global,", pmcs, "!=", len(self.__money__))
			
		for player in self.__players__:
			clear &= player.verify(spes, spms)
		
		print(">>> Verification Finished - Mode", mode, "Turn", turn)
		
		return clear
	
	# Turn : 0~ / Begin : begin user indicator code. Currently unused.
	def turn_estate(self, turn, begin = 0):
		self.verify(turn, 0) # Verification. Result will be returned...
		if Const.DPO:
			print(">>> Playing Turn Estate #", turn+1)
		
		market = [] # Candidate cards. Save with sorted states.
		for i in range(self.__size__):
			market.append(self.__estate__.pop())
		market.sort(reverse=True)

		price = 0 # Bidding price
		bidder = self.__players__[::-1] # Reverse - to use pop & insert

		while 1 != len(bidder):
			player = bidder.pop()
			print(player.name, "> ", end="")
			result = player.turn_estate(price) # new-bet case
			if 0 == result: # DIe - get lowest card
				player.die(market.pop())
			elif 0 < result: # Newly bet
				price = result
				bidder.insert(0, player)
			else: # Wrong code return
				print("Error #5 WrongCodeSTE : ", self.gid, player.name, player.pid, result)
				sys.exit(0)

		### Last Card distribution - len(bidder) must be 1
		print("Final User ->\n" + str(bidder[0].name), "> ", end="")
		bidder[0].die(market.pop(), True)
		
		### Verification
		if 0 != len(market):
			print("Error #6 NonEmptyMarket : ", self.gid, len(market), market)
		
		### Next begin user return
		return begin # Currently, fixed begin user.

	def turn_money(self, turn, begin = 0):
		self.verify(turn, 1) # Verification. Result will be returned...
		if Const.DPO:
			print(">>> Playing Turn Money #", turn+1)
		
		market = [] # Candidate cards. Save with sorted states.
		for i in range(self.__size__):
			market.append(self.__money__.pop())
		market.sort(reverse=True)
		
		deck = []
		for player in self.__players__:
			deck.append((player.turn_money(), player))
		deck.sort()
		
		for pair in deck:
			self.__estate__.append(pair[0])
			new_money = market.pop()
			new_money.set_owner(pair[1])
			pair[1].__money__.append(new_money)
			pair[1].__balance__ += new_money.value
			if Const.DPO:
				print(pair[1].name, "> Estate", pair[0].value, "-> Money", new_money.value)
		
		### Next begin user return
		return begin # Currently, fixed begin user.
	
	def close(self):
		print("\n>>> Game Ended <<<")
		self.__players__.sort(reverse = True)
		rank = 1
		for player in self.__players__:
			print("Rank #" + str(rank), player)
			rank += 1