class Card:
	def __init__(self, value): 
		self.value = value # 1-30
		self.__owner__ = None # Card owner. None means "on deck"
		
	def __lt__(self, other):
		return self.value < other.value