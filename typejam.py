import sys
 
from PyQt5 import QtGui, QtWidgets, QtCore
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
 
 
class AddTextWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()
 
    def setupUi(self):
        self.setWindowTitle("AddText")
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self.resize(500, 250)
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.textForAdding = QtWidgets.QTextEdit()
        font = QtGui.QFont()
        font.setPointSize(14)
        self.textForAdding.setFont(font)
        self.buttonAddText = QtWidgets.QPushButton()
        self.buttonAddText.setText("Add Text")
        self.buttonAddText.clicked.connect(self.clickedAddText)
        self.gridLayout.addWidget(self.textForAdding)
        self.gridLayout.addWidget(self.buttonAddText)
 
    def clickedAddText(self):
        if self.textForAdding.toPlainText() != "":
            self.parent().strListOfAllTexts.append(self.textForAdding.toPlainText())
            self.parent().updateTxtFile()
            self.close()
        else:
            self.ShowEmptyTextMessage()
 
    def ShowEmptyTextMessage(self):
        message = QtWidgets.QMessageBox()
        message.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        message.setWindowTitle("Error")
        message.setText("You haven't entered the text")
        x = message.exec_()
 
 
class ChangeTextWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent, QtCore.Qt.Window)
        self.setupUi()
        self.initWindows()
 
    def setupUi(self):
        self.setWindowTitle("Change Text")
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self.resize(600, 400)
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.currentTextFromSelector = QtWidgets.QTextEdit()
        font = QtGui.QFont()
        font.setPointSize(14)
        self.currentTextFromSelector.setFont(font)
        self.currentTextFromSelector.setReadOnly(True)
        self.gridLayout.addWidget(self.currentTextFromSelector, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
 
        self.buttonChooseText = QtWidgets.QPushButton(self)
        self.buttonChooseText.setText("Choose Text")
        self.buttonChooseText.clicked.connect(self.buttonChooseTextClicked)
        self.horizontalLayout.addWidget(self.buttonChooseText)
        self.buttonAddText = QtWidgets.QPushButton(self)
        self.buttonAddText.clicked.connect(self.addTextProcessing)
        self.buttonAddText.setText("Add Text")
        self.horizontalLayout.addWidget(self.buttonAddText)
 
        self.buttonDeleteText = QtWidgets.QPushButton(self)
        self.buttonDeleteText.setText("Delete Text")
        self.buttonDeleteText.clicked.connect(self.buttonDeleteTextClicked)
        self.horizontalLayout.addWidget(self.buttonDeleteText)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 1, 1, 1)
 
        self.TextSelector = QtWidgets.QListWidget(self)
        self.TextSelector.itemClicked.connect(self.itemClickedProcessing)
 
        self.listOfAllTexts = list()
        self.initTextSelector()
        self.gridLayout.addWidget(self.TextSelector, 0, 1, 1, 1)
 
    def initWindows(self):
        self.addTextWindow = AddTextWindow(self)
 
    def initTextSelector(self):
        file = open("temptext.txt", "r", encoding='utf-8-sig')
        self.listOfAllTexts = file.read().split("||||")
        file.close()
        self.TextSelector.clear()
        for i in range(len(self.listOfAllTexts)):
            item = QtWidgets.QListWidgetItem()
            item.setText("Text {}".format(i + 1))
            self.TextSelector.addItem(item)
 
    def updateTxtFile(self):
        file = open("temptext.txt", "w", encoding='utf-8-sig')
        for i in range(len(self.listOfAllTexts)):
            file.write(self.listOfAllTexts[i])
            if i != len(self.listOfAllTexts) - 1:
                file.write("||||")
        file.close()
        self.initTextSelector()
 
    def buttonChooseTextClicked(self):
        if self.TextSelector.currentRow() == -1:
            message = QtWidgets.QMessageBox()
            message.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            message.setWindowTitle("Error")
            message.setText("You haven't chosen a text")
            x = message.exec_()
        else:
            self.parent().updateTextForTyping(self.listOfAllTexts[self.TextSelector.currentRow()])
            self.close()
 
    def buttonDeleteTextClicked(self):
        if self.TextSelector.currentRow() == -1:
            message = QtWidgets.QMessageBox()
            message.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            message.setWindowTitle("Error")
            message.setText("You haven't chosen a text")
        else:
            self.listOfAllTexts.remove(self.listOfAllTexts[self.TextSelector.currentRow()])
            self.updateTxtFile()
            self.currentTextFromSelector.setText("")
 
 
    def itemClickedProcessing(self):
        self.currentTextFromSelector.setText(self.listOfAllTexts[self.TextSelector.currentRow()])
 
    def addTextProcessing(self):
        self.addTextWindow.show()
 
 
class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle("TypeJam")
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.setGeometry(560, 300, 800, 500)
        self.initUserInput()
        self.initTextForTyping()
        self.initButtons()
        self.initCheckboxes()
        self.initProgressBars()
        self.initLabels()
        self.addLayouts()
        self.initMistakeSound()
        self.initWindows()
        self.initStopwatch()
 
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
 
        self.allTextIsTyped = False
 
    def initUserInput(self):
 
        self.userInput = QtWidgets.QLineEdit()  # UserInputClass()
        self.userInput.setGeometry(30, 320, 580, 40)
        fontUserInput = QtGui.QFont()
        fontUserInput.setFamily("Arial")
        fontUserInput.setPointSize(20)
        self.userInput.setFont(fontUserInput)
        self.userInput.setEnabled(False)
        self.prevLenForSpeed = 0
        self.len_previous_userInput = 0
        self.sumOfEverySecondSpeed = 0
        self.userInput.textChanged.connect(self.inputProcessing)
 
    def initButtons(self):
        self.buttonStart = QtWidgets.QPushButton("Start", self)
        self.buttonStart.clicked.connect(self.buttonStartClicked)
        self.buttonStop = QtWidgets.QPushButton("Stop", self)
        self.buttonStop.clicked.connect(self.buttonStopClicked)
        self.buttonChangeText = QtWidgets.QPushButton("Change text", self)
        self.buttonChangeText.clicked.connect(self.changeTextProcessing)
        self.buttonStats = QtWidgets.QPushButton("Stats", self)
 
 
    def addLayouts(self):
        self.gridLayout.addWidget(self.textForTyping, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.userInput, 1, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.addWidget(self.buttonStart)
        self.verticalLayout.addWidget(self.buttonStop)
        self.verticalLayout.addWidget(self.buttonChangeText)
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
        self.checkboxMistakeSound.setChecked(False)
 
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
        font.setPointSize(12)
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
 
    def initWindows(self):
        self.changeText = ChangeTextWindow(self)
 
    def initStopwatch(self):
        self.msec = 0
        self.sec = 0
        self.min = 0
        self.stopwatch = QtCore.QTimer(self)
        self.stopwatch.timeout.connect(self.stopwatchProcessing)
 
    def progressBarProcessing(self):
        self.value_player1ProgressBar = (self.allsymbols_greenText + self.currentsymbols_greenText) / len(
            self.str_textForTyping) * 100
        self.player1ProgressBar.setFormat("{0:.1f}".format(self.value_player1ProgressBar) + "%")
        self.player1ProgressBar.setValue(self.value_player1ProgressBar)
 
    def timerProcessing(self):
        if self.countdownValue > 0:
            self.countdownValue -= 1
            print(self.countdownValue)
            self.label_Countdown.setText(str(self.countdownValue+1))
            QTimer().singleShot(1000, self.timerProcessing)
        else:
            self.label_Countdown.setText("")
            self.buttonStop.setEnabled(True)
            self.userInput.setEnabled(True)
            self.userInput.setFocus()
            self.inputProcessing()
            self.stopwatch.start(100)
 
    def speedProcessing(self):
        self.sumOfEverySecondSpeed += self.allsymbols_greenText - self.prevLenForSpeed
        self.label_SpeedValue.setText("{0:.1f}".format(self.sumOfEverySecondSpeed/self.sec*60) + " cpm")
        self.prevLenForSpeed = self.allsymbols_greenText
 
    def stopwatchProcessing(self):
        if self.msec < 9:
            self.msec += 1
        else:
            if self.sec < 59:
                self.msec = 0
                self.sec += 1
                self.speedProcessing()
            elif self.sec == 59:
                self.min += 1
                self.sec = 0
                self.msec = 0
 
        time = "{0}:{1}:{2}".format(self.min, self.sec, self.msec)
        self.label_Countdown.setText(time)
 
 
    def buttonStartClicked(self):
        self.countdownValue = 5
        self.userInput.setEnabled(False)
        self.buttonStart.setEnabled(False)
        self.buttonStop.setEnabled(False)
        self.timerProcessing()
 
    def buttonStopClicked(self):
        self.stopwatch.stop()
        self.msec = 0
        self.sec = 0
        self.min = 0
        self.allTextIsTyped = True
        self.currentWordIndex = 0
        self.allsymbols_greenText = 0
        self.currentsymbols_greenText = 0
        self.MistakesValue = 0
        self.label_MistakesValue.setText(str(self.MistakesValue))
        self.label_Countdown.setText("")
        self.fillColoredText()
        self.userInput.clear()
        self.player1ProgressBar.setValue(0)
        self.userInput.setEnabled(False)
        self.buttonStart.setEnabled(True)
 
    def changeTextProcessing(self):
        self.changeText.show()
 
    def GetTextFromFile(self):
        textfile = open("text.txt", "r")
        self.TextFromFile = textfile.read()
        textfile.close()
        return self.TextFromFile
 
    def initMistakeSound(self):
        self.sound = QSound("typo.wav")
 
    def updateTextForTyping(self, textarg):
        self.textForTyping.setText(textarg)
        self.list_textForTyping = self.textForTyping.toPlainText().split(" ")
        self.currentWordIndex = 0
        self.str_textForTyping = self.textForTyping.toPlainText()
        self.allsymbols_greenText = 0
        self.currentsymbols_greenText = 0
        self.MistakesValue = 0
        self.label_MistakesValue.setText(str(self.MistakesValue))
        self.allTextIsTyped = False
        self.userInput.setEnabled(False)
        self.fillColoredText()
        self.player1ProgressBar.setValue(0)
        self.userInput.clear()
 
 
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
                # self.list_userInput.append(self.current_word_from_userInput)
                # self.current_word_from_userInput = str()
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
        if self.userInput.text() == self.list_textForTyping[-1]:
            self.allTextIsTyped = True
            self.currentWordIndex = 0
            self.allsymbols_greenText = 0
            self.currentsymbols_greenText = 0
            self.MistakesValue = 0
            self.label_MistakesValue.setText(str(self.MistakesValue))
            self.fillColoredText()
            self.userInput.clear()
            self.player1ProgressBar.setValue(0)
            self.userInput.setEnabled(False)
            message = QtWidgets.QMessageBox()
            message.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            message.setWindowTitle("TypeJam")
            message.setText("Done!")
            x = message.exec_()
 
 
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()
 
    sys.exit(app.exec_())
