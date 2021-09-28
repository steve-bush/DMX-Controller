import PyQt5
import PyQt5.QtWidgets
import PyQt5.QtGui
import sys
import numpy as np


class DMX_GUI(PyQt5.QtWidgets.QMainWindow):

    def __init__(self, order=['brightness', 'r', 'g', 'b']):
        PyQt5.QtWidgets.QMainWindow.__init__(self)

        # Dictionary to track the values of each input
        self.__values = {}
        self.order = order

        # Set up the closing action
        self.leave = PyQt5.QtWidgets.QAction("&Quit", self)

        # Define and set main and sub widget
        self.widget = PyQt5.QtWidgets.QWidget()
        self.subwidget = PyQt5.QtWidgets.QWidget()

        # Set up the layout of the widgets
        layout_box = PyQt5.QtWidgets.QVBoxLayout()
        layout_grid = PyQt5.QtWidgets.QGridLayout()

        # Create the line edits and sliders for inputs
        # and create the layout for the subwidget
        self.labels = {}
        self.sliders = {}
        self.edits = {}
        row = 0
        for option in order:
            # Create labels
            self.labels[option] = PyQt5.QtWidgets.QLabel('{}:'.format(option))
            # Create sliders
            self.sliders[option] = PyQt5.QtWidgets.QSlider(
                PyQt5.QtCore.Qt.Horizontal)
            self.sliders[option].setMinimum(0)
            self.sliders[option].setMaximum(255)
            self.sliders[option].setSingleStep(1)
            # Create line edits
            self.edits[option] = PyQt5.QtWidgets.QLineEdit()
            self.edits[option].setText('0')
            # Initialize the values to 0
            self.__values[option] = 0
            # Put each widget into the grid layout
            layout_grid.addWidget(self.labels[option], row, 0)
            layout_grid.addWidget(self.sliders[option], row, 1)
            layout_grid.addWidget(self.edits[option], row, 2)
            row += 1
            # Connect the widgets to actions
            self.sliders[option].valueChanged.connect(self.update_color_slider)
            self.edits[option].textChanged.connect(self.update_color_text)

        # Add the grid layout to the subwidget
        self.subwidget.setLayout(layout_grid)

        # Button that actually is the selected color
        self.color = PyQt5.QtWidgets.QPushButton()
        self.color.isFlat()
        # Initialize the collor
        self.color.setStyleSheet("background-color:rgb(0,0,0)")

        # Button to close the GUI
        self.exit = PyQt5.QtWidgets.QPushButton("Submit")
        self.exit.clicked.connect(self.close)

        # Add the subwidget and buttons to the main widget
        layout_box.addWidget(self.subwidget)
        layout_box.addWidget(self.color)
        layout_box.addWidget(self.exit)
        self.widget.setLayout(layout_box)

        # Set the central widget
        self.setCentralWidget(self.widget)

    def update_color_slider(self):
        '''Set the color button to the input color when a slider changes'''
        # Update the values dictionary and line edits
        for option in self.order:
            self.__values[option] = self.sliders[option].value()
            self.edits[option].setText(str(self.sliders[option].value()))
        # Update the color button
        self.color.setStyleSheet(
            "background-color:rgb({0},{1},{2})".format(self.__values['r'], self.__values['g'], self.__values['b']))

    def update_color_text(self):
        '''Set the color button to the input color when a line edit changes'''
        # Update the values dictionary and sliders
        for option in self.order:
            text = self.edits[option].text()
            # Test if number is positive and numeric
            if text != '' and text.isnumeric():
                # If a number is input assign the value
                value = int(text)
            elif text == '':
                # If nothing is input assign 0
                value = 0
            else:
                # If the text is not numeric assign 0 and change line edit
                value = 0
                self.edits[option].setText('0')
            # Update value dictionary and slider
            self.__values[option] = value
            self.sliders[option].setValue(value)
        # Update the color
        self.color.setStyleSheet(
            "background-color:rgb({0},{1},{2})".format(self.__values['r'], self.__values['g'], self.__values['b']))

    @property
    def values(self):
        return self.__values


if __name__ == '__main__':
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    widget = DMX_GUI()
    widget.show()
    app.exec_()
