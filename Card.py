class Card:
	def __init__(self, type, value): 
		self.value = value # 1-30
		self.type = type # "Money" or "Estate"
		self.__owner__ = None # Card owner. None means "on deck"
	
	def __repr__(self):
		rp = "[ " + str(self.type) + " Value = " + str(self.value)
		if self.__owner__ is None:
			rp += " | On Deck ]"
		else:
			rp += " | Owner =" + str(self.__owner__.__pid__) + " ]"
		return rp
	
	def __lt__(self, other):
		return self.value < other.value
	
	def set_owner(self, player):
		if self.__owner__ is None:
			self.__owner__= player
		else:
			print("Error #C0201 Double_Card_Allocation : ", self, player)
	
	def release(self, player): # Player input is for verify.
		if self.__owner__ == player:
			self.__owner__= None
		else:
			print("Error #C0301 Wrong_Owner_Release : ", self, player)
	
	def verify(self, player):
		if self.__owner__ == player:
			return True
		else:
			print("Error #C0401 Wrong_Owner_Verify : ", self, player)
			return False