from Server import *

from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
		QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
		QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
		QSlider, QSpinBox, QTableWidget, QTabWidget, QTextEdit,
		QVBoxLayout, QWidget)


class WidgetGallery(QDialog):
	def __init__(self, parent=None):
		super(WidgetGallery, self).__init__(parent)

		self.setWindowTitle("For Sale Game Client Test v0")
		
		self.originalPalette = QApplication.palette()
		
		self.player_boxes = [None] * 6
		self.money = [13] * 6
		self.create_pregame_box()
		for code in range(6):
			self.create_player_box(code)
		
		self.create_response_estate_box()
		self.create_response_money_box()
		self.createTopRightGroupBox()
		self.create_note_box()
		self.createProgressBar()


		self.disableWidgetsCheckBox.toggled.connect(self.num_players.setDisabled)
		self.disableWidgetsCheckBox.toggled.connect(self.advanced_ai.setDisabled)
		self.disableWidgetsCheckBox.toggled.connect(self.show_known_cards.setDisabled)
		self.disableWidgetsCheckBox.toggled.connect(self.disableWidgetsCheckBox.setDisabled)
		
		self.disableWidgetsCheckBox.toggled.connect(self.response_estate_box.setDisabled)
		self.disableWidgetsCheckBox.toggled.connect(self.response_money_box.setDisabled)
		self.disableWidgetsCheckBox.toggled.connect(self.topRightGroupBox.setDisabled)

		mainLayout = QGridLayout()
		mainLayout.addLayout(self.topLayout, 0, 0, 1, 6)
		
		for pos in range(6):
			mainLayout.addWidget(self.player_boxes[pos], 1, pos)
		
		# 0-1 : Interaction / 2-3 : Previous Turn Result / 4-5 : Note
		
		mainLayout.addWidget(self.response_estate_box, 2, 0, 1, 2)
		mainLayout.addWidget(self.response_money_box, 3, 0, 1, 2)
		#mainLayout.addWidget(self.topRightGroupBox, 2, 2, 1, 2)
		mainLayout.addWidget(self.note_box, 2, 4, 2, 2)
		#mainLayout.addWidget(self.progressBar, 4, 0, 1, 6)
		mainLayout.setRowStretch(1, 1)
		mainLayout.setRowStretch(2, 1)
		mainLayout.setColumnStretch(0, 1)
		mainLayout.setColumnStretch(1, 1)
		self.setLayout(mainLayout)

	def advanceProgressBar(self):
		curVal = self.progressBar.value()
		maxVal = self.progressBar.maximum()
		self.progressBar.setValue(curVal + (maxVal - curVal) / 100)

	def create_pregame_box(self):
		self.num_players = QComboBox()
		self.num_players.addItems(["3", "4", "5", "6"])

		num_players_label = QLabel("&Number of Players :")
		num_players_label.setBuddy(self.num_players)

		self.advanced_ai = QCheckBox("&Use Advanced AI")
		# self.advanced_ai.setChecked(True)
		
		self.show_known_cards = QCheckBox("&Show Known Cards")
		self.show_known_cards.setChecked(True)

		self.disableWidgetsCheckBox = QCheckBox("&Disable widgets")
		
		self.start_button = QPushButton("Start Game!")
		
		self.topLayout = QHBoxLayout()
		self.topLayout.addWidget(num_players_label)
		self.topLayout.addWidget(self.num_players)
		self.topLayout.addStretch(1)
		self.topLayout.addWidget(self.advanced_ai)
		self.topLayout.addWidget(self.show_known_cards)
		self.topLayout.addWidget(self.start_button)
		# self.topLayout.addWidget(self.disableWidgetsCheckBox)

	def create_player_box(self, num): # 0 = Player
		if 0 == num:
			box_name = "Player"
		else:
			box_name = "AI #" + str(num)
		self.player_boxes[num] = QGroupBox(box_name)
		balance_label = QLabel("Money : " + str(self.money[num]))
		estate_box = QGroupBox("Estates")
		estate_label = QLabel(" " * 31)
		money_box = QGroupBox("Money")
		money_label = QLabel(" " * 31)
		
		layout_e = QHBoxLayout()
		layout_e.addWidget(estate_label)
		estate_box.setLayout(layout_e)
		
		layout_m = QHBoxLayout()
		layout_m.addWidget(money_label)
		money_box.setLayout(layout_m)
		
		layout = QGridLayout()
		layout.addWidget(balance_label, 0, 0)
		layout.addWidget(estate_box, 1, 0)
		layout.addWidget(money_box, 2, 0)
		
		self.player_boxes[num].setLayout(layout)
		
	def create_response_estate_box(self):
		self.response_estate_box = QGroupBox("Estate Response")
		
		slider = QSlider(Qt.Horizontal, self.response_estate_box)
		slider.setMinimum(0)
		slider.setValue(0)
		slider.setMaximum(self.money[0]) # Player Money
		slider.setTickInterval(1)
		
		slider_label = QLabel(str(slider.value()))
		slider.valueChanged.connect(slider_label.setNum)
		
		self.bet_button = QPushButton("Bet")
		self.fold_button = QPushButton("Fold")
		
		layout = QGridLayout()
		layout.addWidget(slider, 0, 0, 1, 1)
		layout.addWidget(slider_label, 0, 1, 1, 1)
		layout.addWidget(self.bet_button, 1, 0, 1, 1)
		layout.addWidget(self.fold_button, 1, 1, 1, 1)
		self.response_estate_box.setLayout(layout)

	def create_response_money_box(self):
		self.response_money_box = QGroupBox("Money Response")
		
		self.estate_list = QComboBox()
		for num in range(8):
			self.estate_list.addItems(["Card " + str(num+1)])
			
		self.confirm_button = QPushButton("Confirm")
		
		layout = QGridLayout()
		layout.addWidget(self.estate_list, 0, 0, 1, 1)
		layout.addWidget(self.confirm_button, 0, 1, 1, 1)
		self.response_money_box.setLayout(layout)

	def createTopRightGroupBox(self):
		self.topRightGroupBox = QGroupBox("Player 2")

		defaultPushButton = QPushButton("Default Push Button")
		defaultPushButton.setDefault(True)

		togglePushButton = QPushButton("Toggle Push Button")
		togglePushButton.setCheckable(True)
		togglePushButton.setChecked(True)

		flatPushButton = QPushButton("Flat Push Button")
		flatPushButton.setFlat(True)

		layout = QVBoxLayout()
		layout.addWidget(defaultPushButton)
		layout.addWidget(togglePushButton)
		layout.addWidget(flatPushButton)
		layout.addStretch(1)
		self.topRightGroupBox.setLayout(layout)

	def create_note_box(self):
		self.note_box = QGroupBox("Note")

		note = QTextEdit()
		note.setPlainText("Please Note Here")
		
		layout = QVBoxLayout()
		layout.addWidget(note)
		self.note_box.setLayout(layout)

	def createProgressBar(self):
		self.progressBar = QProgressBar()
		self.progressBar.setRange(0, 10000)
		self.progressBar.setValue(0)

		timer = QTimer(self)
		timer.timeout.connect(self.advanceProgressBar)
		timer.start(1000)

if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
	gallery = WidgetGallery()
	gallery.show()
	sys.exit(app.exec_()) 