import Const

import random

class Player:
	def __init__(self, name=None):
		self.name = name
		if self.name is None:
			self.name = "Player #" + str(Const.pid)
		self.pid = Const.pid
		Const.pid += 1
		self.__estate__ = [] # Deck for estate cards. Verify by "Game Turn" & "Deck Length"
		self.__money__ = [] # Deck for money cards. Verify by "Game Turn" & "Deck Length"
		self.__balance__ = Const.PIB # Total balance
		self.__bet__ = 0 # Amount of bet
		self.__isAI__ = (name is None) 
	
	def __repr__(self):
		rp = "[ Player Name = " + str(self.name)
		rp += " | Estate #" + str(len(self.__estate__))
		rp += " | Money #" + str(len(self.__money__))
		rp += " | Balance = " + str(self.__balance__)
		rp += " ]"
		return rp
		
	def __lt__(self, other):
		return self.__balance__ < other.__balance__
	
	def verify(self, spes, spms):
		clear = True
		if len(self.__estate__) != spes:
			print("Critical error : Improper estate container,", self.name, spes, "!=", len(self.__estate__))
		if len(self.__money__) != spms:
			print("Critical error : Improper money container,", self.name, spms, "!=", len(self.__money__))
		for card in self.__estate__:
			clear &= card.verify(self)
		for card in self.__money__:
			clear &= card.verify(self)
		return clear
	
	def get_response(self, mode, min = 0): # mode = 0 (estate) or 1 (money)
		if 0 == mode:
			if min > self.__balance__:
				return 0 # Cannot-bet-case
			else:
				return random.randrange(min, self.__balance__+1)
		elif 1 == mode:
			pick = random.choice(self.__estate__)
			pick.release(self) # Verify at here.
			self.__estate__.remove(pick)
			return pick
		else:
			print("Error #G0201 Wrong_Verify_Mode : ", self.pid, turn, mode)
			return -1
	
	def turn_estate(self, cur_bet): # Processing Turn Estate
		# NOTE : 
		retry = Const.RETRY_CNT # Retry maximum - Wait for Client.
		while retry > 0: # Wait until
			resp = self.get_response(0, cur_bet+1)
		
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
	
	def turn_money(self): # Processing Turn Money
		return self.get_response(1)

	def bet(self, amount, prev):
		if self.__balance__ >= amount and prev < amount:
			self.__bet__ = amount
		else:
			print("Error #2 BetError : ", self.pid, self.__bet__, prev, amount, self.__balance__)
			self.__bet__ = self.__balance__
		print("BET,", prev, "->", self.__bet__, "/", self.__balance__)
	
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
		card.set_owner(self)
		print("DIED, bought estate", card.value, "by pay", pay, "and gain", gain, "| balance", self.__balance__)
	
	def print_estate(self):
		print("Player", self.pid, "has...")
		self.__estate__.sort()
		for card in self.__estate__:
			print("   > Estate", card.value)
