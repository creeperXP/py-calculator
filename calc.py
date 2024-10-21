

import sys
from functools import partial


from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
   QApplication,
   QGridLayout,
   QLineEdit,
   QMainWindow,
   QPushButton,
   QVBoxLayout,
   QWidget,
)


ERROR = "ERROR"

# calculator class creates GUI for calculator inheriting from QMainWindow
class calculator(QMainWindow):
   # constructor for calculator following from QMainWindow 
   def __init__ (self):
       super().__init__()

       # sets size, title, box (vertical) layout for calculator
       # implement colored buttons which changes color when hovered over
       self.setWindowTitle("Calculator")
       self.setFixedSize(250, 15)
       self.generalLayout = QVBoxLayout()
       self.setStyleSheet("""
           QPushButton {
               background-color: lightblue;  /* Background color */
               border: 2px solid darkblue;    /* Border color */
               border-radius: 5px;             /* Rounded corners */
           }
           QPushButton:hover {
               background-color: deepskyblue;  /* Change background on hover */
           }""")

       # create container for the calculator object 
       container = QWidget(self)

       # set to box layout 
       container.setLayout(self.generalLayout)
       # fills the window
       self.setCentralWidget(container)
       # create display/input area and number buttons
       self.makeDisplay()
       self.makeButtons()   


   # display creation
   def makeDisplay(self):
       self.display = QLineEdit() # single-line text box to display input/result
       self.display.setFixedHeight(DISPLAY_HEIGHT) 
       self.display.setAlignment(Qt.AlignmentFlag.AlignRight) # text right aligned
       self.generalLayout.addWidget(self.display)
       self.display.setReadOnly(True) # read only, no editing the output/input with keyboard

   # set current input/output using QLineEdit
   def setText(self, text):
       self.display.setText(text) # update input
       self.display.setFocus() # receive input

   # get current text in the display 
   def getText(self):
       return self.display.text() # shows the text

   # clear the text inside the display 
   def clearText(self):
       self.setText("") # clears text

   # define function to create the calculator buttons 
   def makeButtons(self):
       # dictionary for button easy access 
       self.buttonMap = {}
       # create grid layout for the buttons
       buttonsLayout = QGridLayout()
       # 2D list to display buttons
       keyBoard = [
           ["7", "8", "9", "/", "C"],
           ["4", "5", "6", "*", "("],
           ["1", "2", "3", "-", ")"],
           ["0", "00", ".","+", "="],
       ]

       # create buttons arrangement
       for row, keys in enumerate(keyBoard):
           for col, key in enumerate(keys):
               self.buttonMap[key] = QPushButton(key)
               self.buttonMap[key].setFixedSize(40, 40)
               buttonsLayout.addWidget(self.buttonMap[key], row, col)
       # add buttons to screen
       self.generalLayout.addLayout(buttonsLayout)

   # compute the value of the expression given 
   def evaluate(self, expression):
       try:
           result = str(eval(expression, {}, {})) # {} used to prevent access to variables
       except Exception:
           result = ERROR # invalid expression
       return result

# the controller gives user functionality towards the buttons
class controller:

   # constructor to be able to evaluate expression, show buttons, connecting the user signals to input/output 
   def __init__(self, model, view):
       self.evaluate = model
       self.view = view
       self.connect()

   # calculate the expression and update display
   def calculateResult(self):
       result = self.evaluate(expression=self.view.getText())
       self.view.setText(result)

   # build expression based on user input
   def buildExpression(self, sub):
       current_text = self.view.getText()


       # clear display if there was an error processing expression
       if current_text == ERROR:
           self.view.clearText()

       # insert multiplication for cases: number(
       if subExpression == "(" and current_text and current_text[-1].isdigit():
           subExpression = "*" + subExpression  # put multiplication sign

       # don't adding operators directly after another operator or after (
       if (sub in {"+", "-", "*", "/"} and
               (current_text == "" or current_text[-1] in {"(", "+", "-", "*", "/"})):
           return

       # adding the subExpression to get total value
       expression = current_text + sub
       self.view.setText(expression)

   # connect a button click to input to the display and calculation 
   def connect(self):
       for keySymbol, button in self._view.buttonMap.items():
           if keySymbol not in {"=", "C"}:
               button.clicked.connect(
                   partial(self.buildExpression, keySymbol)
               )
       # connect = to calculating a result and C to clear screen 
       self.view.buttonMap["="].clicked.connect(self.calculateResult)
       self.view.display.returnPressed.connect(self.calculateResult)
       self.view.buttonMap["C"].clicked.connect(self.view.clearText)

# create the window object (calculator instance)
def main():
   pycalcApp = QApplication([])
   window = calculator()
   window.show()
   # pass in window and evaluate so the controller class can calculate and display expression
   # from input
   controller(model=window.evaluate, view=window)
   sys.exit(pycalcApp.exec())

# script must be executed directly
if __name__ == "__main__":
   main()
