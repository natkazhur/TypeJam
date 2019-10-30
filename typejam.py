import sys
import time
import threading

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QTextCursor, QTextCharFormat
from PyQt5.QtMultimedia import QSound
from PyQt5.QtWidgets import QLabel


class UserInputClass(QtWidgets.QLineEdit):
    def __init__(self):
        QtWidgets.QLineEdit.__init__(self)
        self.wasPressed = False

    def keyPressEvent(self, keyEvent):
        super(UserInputClass, self).keyPressEvent(keyEvent)
        if keyEvent.key() == Qt.Key_Backspace:
            print('Backspace pressed')


class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("TypeJam")
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.setGeometry(300, 300, 800, 500)
        self.initUserInput()
        self.initTextForTyping()
        self.initButtons()
        self.initCheckboxes()
        self.initProgressBars()
        self.initLabels()
        self.addLayouts()
        self.inputProcessing()
        self.initMistakeSound()

    def initTextForTyping(self):
        self.textForTyping = QtWidgets.QTextEdit(self)
        self.textForTyping.setGeometry(30, 30, 580, 280)
        fontTextForTyping = QtGui.QFont()
        fontTextForTyping.setFamily("Arial")
        fontTextForTyping.setPointSize(20)
        self.textForTyping.setFont(fontTextForTyping)
        self.textForTyping.setReadOnly(True)
        self.textForTyping.setText(self.GetTextFromFile())
        self.list_textForTyping = self.textForTyping.toPlainText().split(" ")
        self.currentWordIndex = 0

        self.str_textForTyping = self.textForTyping.toPlainText()
        self.allsymbols_greenText = 0
        self.currentsymbols_greenText = 0
        self.fillColoredText()

    def initUserInput(self):
        self.userInput = UserInputClass()
        self.userInput.setGeometry(30, 320, 580, 40)
        fontUserInput = QtGui.QFont()
        fontUserInput.setFamily("Arial")
        fontUserInput.setPointSize(20)
        self.userInput.setFont(fontUserInput)
        self.list_userInput = list()
        self.current_word_from_userInput = str()
        self.current_symbolIndex = 0
        self.len_previous_userInput = 0
        self.userInput.textChanged.connect(self.inputProcessing)

    def initButtons(self):
        self.buttonStart = QtWidgets.QPushButton("Start", self)
        self.buttonStart.clicked.connect(self.countdownProcessing)
        self.buttonStop = QtWidgets.QPushButton("Stop", self)
        self.buttonSetText = QtWidgets.QPushButton("Set text", self)
        self.buttonStats = QtWidgets.QPushButton("Stats", self)

    def addLayouts(self):
        self.gridLayout.addWidget(self.textForTyping, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.userInput, 1, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.addWidget(self.buttonStart)
        self.verticalLayout.addWidget(self.buttonStop)
        self.verticalLayout.addWidget(self.buttonSetText)
        self.verticalLayout.addWidget(self.buttonStats)
        self.verticalLayout.addWidget(self.checkboxMistakeSound)
        self.verticalLayout.addWidget(self.label_Mistakes)
        self.verticalLayout.addWidget(self.label_MistakesValue)
        self.verticalLayout.addWidget(self.label_Speed)
        self.verticalLayout.addWidget(self.label_SpeedValue)
        self.verticalLayout.addWidget(self.label_Countdown)
        self.spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(self.spacerItem)
        self.gridLayout.addLayout(self.verticalLayout, 0, 1)
        self.gridLayout.addWidget(self.player1ProgressBar, 2, 0, 1, 1)

    def initCheckboxes(self):
        self.checkboxMistakeSound = QtWidgets.QCheckBox(self.centralwidget)
        self.checkboxMistakeSound.setText("Звук")
        self.checkboxMistakeSound.setChecked(True)

    def initProgressBars(self):
        self.player1ProgressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.value_player1ProgressBar = 0.0
        self.player1ProgressBar.setFormat("{0:.1f}".format(self.value_player1ProgressBar) + "%")

    def initLabels(self):
        self.label_Mistakes = QLabel(self.centralwidget)
        self.label_MistakesValue = QLabel(self.centralwidget)

        self.label_Speed = QLabel(self.centralwidget)
        self.label_SpeedValue = QLabel(self.centralwidget)

        self.label_Countdown = QLabel(self.centralwidget)

        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_Mistakes.setFont(font)
        self.label_Speed.setFont(font)
        self.label_Countdown.setFont(font)

        font.setBold(True)
        self.label_MistakesValue.setFont(font)
        self.label_SpeedValue.setFont(font)

        self.label_Mistakes.setText("Mistakes")
        self.label_MistakesValue.setText("0")
        self.label_Speed.setText("Speed")
        self.label_SpeedValue.setText("0")

        self.MistakesValue = 0
        self.wasMistake = False

    def progressBarProcessing(self):
        self.value_player1ProgressBar = (self.allsymbols_greenText + self.currentsymbols_greenText) / len(self.str_textForTyping)*100
        self.player1ProgressBar.setFormat("{0:.1f}".format(self.value_player1ProgressBar) + "%")
        self.player1ProgressBar.setValue(self.value_player1ProgressBar)

    def countdownProcessing(self):
        self.countdownValue = 5
        while(self.countdownValue != 0):
            self.label_Countdown.setText("Starts in " + str(self.countdownValue))
            print(("Starts in " + str(self.countdownValue)))
            self.countdownValue -= 1
            time.sleep(1)

    def GetTextFromFile(self):
        textfile = open("text.txt", "r")
        self.TextFromFile = textfile.read()
        textfile.close()
        return self.TextFromFile

    def initMistakeSound(self):
        self.sound = QSound("typo.wav")

    def fillColoredText(self):
        self.textForTyping.setText(("<u><font color='green'>" + self.str_textForTyping[
                                                                0:self.allsymbols_greenText + self.currentsymbols_greenText] +
                                    "</font></u>" + "<font color='black'>" + self.str_textForTyping[
                                                                             self.allsymbols_greenText + self.currentsymbols_greenText:]
                                    + "</font>"))
    def MistakesProcessing(self):
        if self.wasMistake == False:
            self.MistakesValue += 1
            self.wasMistake = True
            self.label_MistakesValue.setText(str(self.MistakesValue))

    def inputProcessing(self):
        current_userInput = self.userInput.text()
        current_wordForTyping = self.list_textForTyping[self.currentWordIndex]

        if len(current_userInput) == 0:
            self.userInput.setStyleSheet("background: rgb(255, 255, 255)")
            self.currentsymbols_greenText = 0
            self.fillColoredText()
            self.progressBarProcessing()
        else:
            lastSymbol = current_userInput[len(current_userInput) - 1]
            if current_wordForTyping.find(current_userInput) == 0:
                self.userInput.setStyleSheet("background: rgb(255, 255, 255)")
                self.currentsymbols_greenText = len(current_userInput)
                self.fillColoredText()
                self.progressBarProcessing()
                self.wasMistake = False
            elif " " in self.userInput.text() and current_wordForTyping.find(
                    current_userInput[:-1]) == 0 \
                    and len(current_wordForTyping) == len(current_userInput) - 1:
                self.list_userInput.append(self.current_word_from_userInput)
                self.current_word_from_userInput = str()
                self.len_previous_userInput = 0
                self.currentWordIndex += 1
                self.allsymbols_greenText += len(current_userInput)
                self.currentsymbols_greenText = 0
                self.fillColoredText()
                self.userInput.clear()
            else: 
                self.userInput.setStyleSheet("background: rgb(255, 80, 80)")
                self.MistakesProcessing()
                if self.checkboxMistakeSound.isChecked() and len(current_userInput) != self.len_previous_userInput:
                    self.sound.play()

        self.len_previous_userInput = len(current_userInput) - 1 if len(current_userInput) >= 1 else 0



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()

    sys.exit(app.exec_())
