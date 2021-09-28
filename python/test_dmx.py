import unittest
import os
import sys
import PyQt5
import PyQt5.QtWidgets
import PyQt5.QtTest
import PyQt5.QtCore
import dmx_gui
from dmx import DMX


class TestDMX(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestDMX, cls).setUpClass()
        # Start GUI for testing
        cls.dmx = DMX()
        cls.ui = dmx_gui.DMX_GUI()

    def test_GUI_value_changes(self):
        '''Test that changing the line edits will change
        the sliders and vice versa.
        '''
        test_value = 255
        for option in self.ui.order:
            # Test line edits changing sliders
            self.ui.edits[option].clear()
            PyQt5.QtTest.QTest.keyClicks(
                self.ui.edits[option], str(test_value))
            self.assertEqual(self.ui.sliders[option].value(), test_value)
            # Test sliders changing line edits
            test_value -= 1
            self.ui.sliders[option].setValue(test_value)
            self.assertEqual(self.ui.edits[option].text(), str(test_value))
            test_value -= 1

    def test_GUI_line_edits(self):
        '''Test for invalid input to line edits'''
        for option in self.ui.order:
            # Test for negative number
            self.ui.edits[option].clear()
            PyQt5.QtTest.QTest.keyClicks(
                self.ui.edits[option], '-1')
            self.assertEqual(self.ui.edits[option].text(), '1')
            self.assertEqual(self.ui.values[option], 1)
            # Test for character input
            self.ui.edits[option].clear()
            PyQt5.QtTest.QTest.keyClicks(
                self.ui.edits[option], 'h')
            self.assertEqual(self.ui.edits[option].text(), '0')
            self.assertEqual(self.ui.values[option], 0)
            # Test for out of range input
            self.ui.edits[option].clear()
            PyQt5.QtTest.QTest.keyClicks(
                self.ui.edits[option], '256')
            self.assertEqual(self.ui.edits[option].text(), '255')
            self.assertEqual(self.ui.values[option], 255)

    def test_GUI_data_return(self):
        '''Test that the GUI returns correct data'''
        expected = {}
        for option in self.ui.order:
            expected[option] = 1
            # Input data
            self.ui.sliders[option].setValue(1)
        # Press submit
        PyQt5.QtTest.QTest.mouseClick(self.ui.exit, PyQt5.QtCore.Qt.LeftButton)
        self.assertDictEqual(self.ui.values, expected)

    def test_dmx_output_GUI(self):
        '''Test the Arduinos ability to translate the
        binary input from GUI into the dmx signal.
        '''
        # Test for all values at 1
        expected = '1100000000011'
        for option in self.ui.order:
            expected += '01000000011'
            self.ui.sliders[option].setValue(1)
        expected += '111'
        # Get the binary data
        PyQt5.QtTest.QTest.mouseClick(self.ui.exit, PyQt5.QtCore.Qt.LeftButton)
        test_frames = self.dmx.dict_to_frames(self.ui.values)
        self.dmx.frames = test_frames
        # Send the data to the arduino and test it
        self.dmx.send_data()
        output = self.dmx.get_dmx_signal()
        self.assertEqual(output, expected)

    def test_arduino_full_data(self):
        '''Test that 512 frames can be sent'''
        test_frames = b''
        expected = '1100000000011'
        for _ in range(512):
            test_frames += b'\x00'
            expected += '00000000011'
        expected += '111'

        self.dmx.frames = test_frames
        self.dmx.send_data()
        output = self.dmx.get_dmx_signal()
        self.assertEqual(expected, output)


if __name__ == '__main__':
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    unittest.main()
