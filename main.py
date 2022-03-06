import sys

from PySide2 import QtGui, QtWidgets
from PySide2.QtCore import (Qt, QSignalMapper)
from PySide2.QtGui import (QFont)
from PySide2.QtWidgets import *

from ui_main import Ui_MainWindow

gray = "rgb(192, 192, 192)"
green = "rgb(0, 255, 0)"
yellow = "rgb(253,255,144)"
lightGray = "rgb(211, 214, 218)"

expectedWord = "KUMAR"  # ANSWER MUST BE SPECIFIED HERE.
expectedWord = expectedWord.lower()
activeRow = 1

txt = ""

answers = ['?????',
           '?????',
           '?????',
           '?????',
           '?????',
           '?????']
letters = []

answerColors = []
keyboardColors = ["rgb(211, 214, 218)",
                  "rgb(211, 214, 218)"]  # Appending 2 items to the list in order to match the length of keyboard buttons.
for x in range(30):
    answerColors.append("white")
    keyboardColors.append(lightGray)
    letters.append("?")


class MainWindow(QMainWindow):
    def __init__(self):
        global wordsLayout
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.answerButtons = []
        self.keyboardButtons = []

        self.initUI()

        self.show()

        self.ui.actionInfo.triggered.connect(lambda: QMessageBox.about(self, "INFO", "Developed for educational purposes.\nBy https://github.com/burkisilin/"))
        self.ui.actionShow_Answer.triggered.connect(lambda: QMessageBox.about(self, "ANSWER", f"Answer: {expectedWord.upper()}"))
        self.ui.actionRestart.triggered.connect(self.restart)

    def initUI(self):
        p = self.palette()
        gradient = QtGui.QLinearGradient(0, 0, 0, 400)
        gradient.setColorAt(0.0, QtGui.QColor('#f1f1f1'))
        gradient.setColorAt(1.0, QtGui.QColor('#00a1de'))
        p.setBrush(QtGui.QPalette.Window, QtGui.QBrush(gradient))
        p.setColor(QtGui.QPalette.Button, QtGui.QColor('orange'))
        self.setPalette(p)

        self.frameButtons = QtWidgets.QFrame()

        # self.createAnswersTable()
        # self.createKeyboardUI()
        self.keyboardUI()
        self.answersUI()

    def restart(self):
        global answers, letters, answerColors, keyboardColors
        answers = ['?????',
                   '?????',
                   '?????',
                   '?????',
                   '?????',
                   '?????']
        letters = []

        answerColors = []
        keyboardColors = ["rgb(211, 214, 218)", "rgb(211, 214, 218)"]
        for x in range(30):
            answerColors.append("white")
            keyboardColors.append(lightGray)
            letters.append("?")

        self.updateAnswersUI()
        self.updateKeyboardUI()

    def answersUI(self):

        self.gridLayout = QtWidgets.QGridLayout()

        letters = []
        for answer in answers:
            for letter in answer:
                letters.append(letter)
        positions = [(i + 1, j) for i in range(6) for j in range(5)]
        for position, name in zip(positions, letters):
            if name == '':
                continue

            button = QPushButton(name)
            button.setFont(QFont('Arial', 15))
            button.setFixedHeight(60)
            button.setFixedWidth(60)
            button.setStyleSheet(f"background-color: white;")
            button.KEY_CHAR = ord(name.upper())
            button.setEnabled(False)
            self.answerButtons.append(button)

            self.gridLayout.addWidget(button, *position)

        self.ui.frame_top.setLayout(self.gridLayout)

    def submitGuess(self, guess):
        global activeRow, letters
        print("guess: ", guess)

        answers[activeRow - 1] = guess

        commonLetters = [w for w in guess.lower() if w in (expectedWord.lower())]
        print(f"commonLetters: {commonLetters}")

        result = "?????"

        for letter in commonLetters:
            index = expectedWord.index(letter)
            if expectedWord[guess.lower().index(letter)] == expectedWord[index]:
                letter = letter.upper()
            result = result[:index] + letter + result[index + 1:]

        print("RESULT: ", result)

        if result.isupper():
            print("CONGRATULATIONS")

        letters = []
        for answer in answers:
            print("->", answer)
            for letter in answer:
                letters.append(letter)

        for l in commonLetters:
            for k in guess.lower():
                if l == k:
                    answerColors[guess.lower().index(k) + (activeRow - 1) * 5] = yellow

                    for b in self.keyboardButtons:
                        if (chr(b.KEY_CHAR)) == k.upper():
                            if keyboardColors[self.keyboardButtons.index(b)] != green:
                                keyboardColors[self.keyboardButtons.index(b)] = yellow
                                break

        for x in range(5):
            if result[x] != "?":
                if result[x].isupper():
                    answerColors[x + (activeRow - 1) * 5] = green
                    for b in self.keyboardButtons:
                        if (chr(b.KEY_CHAR)) == result[x].upper():
                            keyboardColors[self.keyboardButtons.index(b)] = green
                            break
            if guess[x].lower() not in expectedWord:
                answerColors[x + (activeRow - 1) * 5] = "background-color: gray"
                for b in self.keyboardButtons:
                    if (chr(b.KEY_CHAR)) == guess[x].upper():
                        keyboardColors[self.keyboardButtons.index(b)] = "rgb(255, 0, 0)"
                        break

        activeRow += 1
        if activeRow < 7:
            self.updateAnswersUI()
            self.updateKeyboardUI()
        else:
            ret = QMessageBox.question(self, 'FAILED', "Would you like to restart?", QMessageBox.Yes | QMessageBox.No)

            if ret == QMessageBox.Yes:
                self.restart()

    def updateAnswersUI(self):
        for btn in self.answerButtons:
            btn.setText(letters[self.answerButtons.index(btn)])
            btn.setStyleSheet(f"background-color: {answerColors[self.answerButtons.index(btn)]};")

    def updateKeyboardUI(self):
        for btn in self.keyboardButtons:
            btn.setStyleSheet(f"background-color: {keyboardColors[self.keyboardButtons.index(btn)]};")

    def keyboardUI(self):
        self.currentTextBox = None

        self.signalMapper = QSignalMapper(self)
        self.signalMapper.mapped[int].connect(self.buttonClicked)

        layout = QGridLayout()
        layout.setAlignment(Qt.AlignCenter)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()

        self.setAutoFillBackground(True)

        names = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'Ğ', 'Ü',
                 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Ş', 'İ', '',
                 '', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', 'Ö', 'Ç']

        positions = [(i + 1, j) for i in range(3) for j in range(12)]

        for position, name in zip(positions, names):

            if name == '':
                continue
            button = QPushButton(name)
            button.setFont(QFont('Arial', 12))
            button.setFixedHeight(30)
            button.setFixedWidth(30)
            button.setStyleSheet(
                f"background-color: {lightGray};\nborder-style: outset;\nborder-width: .5px;\nborder-radius: 3px;\nborder-color: black;\npadding: 2px;")

            button.KEY_CHAR = ord(name)
            button.clicked.connect(self.signalMapper.map)
            self.signalMapper.setMapping(button, button.KEY_CHAR)
            self.keyboardButtons.append(button)
            layout.addWidget(button, *position)

        # Back button
        back_button = QPushButton('Back')
        back_button.setFixedHeight(30)
        back_button.setFont(QFont('Arial', 12))
        back_button.KEY_CHAR = Qt.Key_Backspace
        layout.addWidget(back_button, 5, 9, 1, 2)
        back_button.clicked.connect(self.signalMapper.map)
        self.signalMapper.setMapping(back_button, back_button.KEY_CHAR)
        back_button.setFixedWidth(60)

        # Enter button
        enter_button = QPushButton('Enter')
        enter_button.setFixedHeight(30)
        enter_button.setFont(QFont('Arial', 12))
        enter_button.KEY_CHAR = Qt.Key_Enter
        layout.addWidget(enter_button, 5, 11, 1, 2)
        enter_button.clicked.connect(self.signalMapper.map)
        self.signalMapper.setMapping(enter_button, enter_button.KEY_CHAR)
        enter_button.setFixedWidth(60)

        self.ui.frame_bottom.setLayout(layout)

    def updateAnswersRow(self, txt):

        for x in range(0, 5):
            try:
                self.answerButtons[(x + ((activeRow - 1) * 5))].setText(txt[x])

                self.answerButtons[(x + ((activeRow - 1) * 5))].setFont(
                    QtGui.QFont("Arial", 15, weight=QtGui.QFont.Bold))
                self.answerButtons[(x + ((activeRow - 1) * 5))].setStyleSheet(
                    f"background-color: white;\nborder-style: outset;\nborder-width: 1.5px;\nborder-radius: 3px;\nborder-color: black;\npadding: 2px;")

            except:
                self.answerButtons[(x + ((activeRow - 1) * 5))].setText("?")
                self.answerButtons[(x + ((activeRow - 1) * 5))].setStyleSheet(f"background-color: {lightGray};")

    def buttonClicked(self, char_ord):
        global txt
        try:
            if char_ord == Qt.Key_Backspace:
                txt = txt[:-1]
                MainWindow.updateAnswersRow(self, txt)

            elif char_ord == 16777221 or char_ord == 16777220:  # ENTER

                if len(txt) == 5:
                    MainWindow.submitGuess(self, txt)
                    txt = ""

            elif char_ord == Qt.Key_Space:
                pass
            elif chr(char_ord).isdigit():
                pass
            elif len(txt) < 5:
                txt += chr(char_ord)
                MainWindow.updateAnswersRow(self, txt)

            # self.text_box.setText(txt)
        except Exception as e:
            print("Exception: ", e, f"?char: {(char_ord)}")

    def keyPressEvent(self, e):
        # self.setFocus()
        # self.setFocusPolicy(Qt.ClickFocus)
        # print(e.key())
        self.buttonClicked(e.key())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
