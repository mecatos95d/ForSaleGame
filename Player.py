import Const

import random

class Player:
	def __init__(self, name=None):
		self.name = name
		if None == self.name:
			self.name = "Player" + str(Const.pid)
		self.pid = Const.pid
		Const.pid += 1
		self.__estate__ = [] # Deck for estate cards. Verify by "Game Turn" & "Deck Length"
		self.__money__ = [] # Deck for money cards. Verify by "Game Turn" & "Deck Length"
		self.__balance__ = Const.PIB # Total balance
		self.__bet__ = 0 # Amount of bet
		self.__isAI__ = (None == name) 
	
	def get_response(self, min = 0): # From Client, minimum is 
		if min > self.__balance__:
			return 0 # Cannot-bet-case
		else:
			return random.randrange(min, self.__balance__+1)
	
	def turn(self, cur_bet): # Processing Turn
		# NOTE : 
		retry = Const.RETRY_CNT # Retry maximum - Wait for Client.
		while retry > 0: # Wait until
			resp = self.get_response(cur_bet+1)
		
			if 0 == resp: # Die signal
				return 0
			
			elif self.__balance__ < resp: # OverBet
				print("Error #3 OverBet : ", self.pid, self.__balance__, resp)
			elif cur_bet >= resp: # UnderBet
				print("Error #4 UnderBet : ", self.pid, self.__balance__, resp, cur_bet)
			
			else: # New bet
				self.bet(resp, cur_bet)
				return resp
				
			retry -= 1
		# Retry Chance Over
		return 0
	
	def bet(self, amount, prev):
		if self.__balance__ >= amount and prev < amount:
			self.__bet__ = amount
		else:
			print("Error #2 BetError : ", self.pid, self.__bet__, prev, amount, self.__balance__)
			self.__bet__ = self.__balance__
		print("   > BET,", prev, "->", self.__bet__, "/", self.__balance__)
	
	def die(self, card, last = False):
		if last:
			gain = 0
		else:
			gain = self.__bet__ // 2
		pay = self.__bet__ - gain
		self.__bet__ = 0
		
		if self.__balance__ >= pay:
			self.__balance__ -= pay
		else:
			print("Error #1 OverPay : ", self.pid, self.__balance__, pay)
			self.__balance__ = 0 # Recovery
		
		self.__estate__.append(card)
		print("   > DIED, bought estate", card.value, "by pay", pay, "and gain", gain, "| balance", self.__balance__)
	
	def print_estate(self):
		print("Player", self.pid, "has...")
		self.__estate__.sort()
		for card in self.__estate__:
			print("   > Estate", card.value)
