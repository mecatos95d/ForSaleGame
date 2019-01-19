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
		self.__balance__ = 0 # Total balance
		self.__bet__ = 0 # Amount of bet
		self.__isAI__ = (None == name) 
	
	def get_response(self, min = 0): # From Client, minimum is 
		return random.randrange(min, self.__balance__+1)
	
	def turn(self): # Processing Turn
		retry = Const.RETRY_CNT # Retry maximum - Wait for Client.
		while retry > 0: # Wait until 
			resp = self.get_response()
		
			if 0 == resp: # Die
				self.die()
				return 1
			
			elif player.__balance__ < resp: # OverBet
				print("Error #3 OverBet : ", player.pid, player.__balance__, resp)
			elif player.__bet__ >= resp: # UnderBet
				print("Error #4 UnderBet : ", player.pid, player.__balance__, resp)
			
			else: # New bet
				self.bet(resp)
				return 2
				
			retry -= 1
		# Retry Chance Over
		self.die()
		return 1
	
	def bet(self, amount):
		if self.__balance__ >= amount and self.__bet__ < amount:
			self.__bet__ = amount
		else:
			print("Error #2 BetError : ", self.pid, self.__bet__, amount, self.__balance__)
			self.__bet__ = self.__balance__
	
	def die(self, last = False):
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
		