import serial
import sys
import time
import PyQt5
import PyQt5.QtWidgets
import dmx_gui


class DMX():
    '''Class to send desired DMX signal to Arduino
    to be sent to a DMX light.
    '''

    def __init__(self, order=['brightness', 'r', 'g', 'b'], port='/dev/ttyACM0', baud=115200, step_time=1000):
        '''Set up the serial port that the Arduino is connected to.'''
        self.ser = serial.Serial(port, baud, timeout=1)
        self.ser.flush()
        # Delay since the arduino resets upon opening serial port
        time.sleep(1)
        assert len(order) < 513, "DMX cannot send more than 512 frames"
        self.order = order
        self.step_time = step_time # ms

    def get_data(self, filename=None):
        '''Collect the data sent from the computer or by user
        input from the GUI.
        '''
        if filename is None:
            # If no file is specified then use the GUI
            app = PyQt5.QtWidgets.QApplication(sys.argv)
            widget = dmx_gui.DMX_GUI(self.order)
            widget.show()
            app.exec_()
            self.frames = self.dict_to_frames(widget.values)
        else:
            # Read in the binary file in sc2 format
            with open(filename, 'rb') as f:
                # Create of list of the integers passed in (Skip 2 size values)
                b = f.read()
            # Number of frames
            num_frames = int.from_bytes(b[0x1FC:0x200], byteorder='little')

            # Get the frames from the binary file
            self.frames = []
            for i in range(num_frames):
                # Get the bytes associated with each frame
                start = i*545 + 512
                stop = start + 512
                frame = b[start:stop]
                # Convert the bytes to integers
                # Ony grabbing bytes used for Arduino data size requirements
                frame_dict = {}
                for j in range(len(self.order)):
                    frame_dict[self.order[j]] = frame[j]
                # File input gives no brightness value so adding it here
                frame_dict['brightness'] = 255
                self.frames.append(self.dict_to_frames(frame_dict))            
        return self.frames

    def dict_to_frames(self, values):
        '''Put the color values into binary and in the
        correct order
        '''
        frames = b''
        for option in self.order:
            assert values[option] < 256, "Value must be < 256"
            assert values[option] >= 0, "Value must be positive"
            assert type(values[option]) == int, "Value must be an integer"
            # Converts the integer values 2 byte strings
            frames += values[option].to_bytes(1, 'little')
        return frames

    def send_data(self):
        '''Send the data frames over the serial port
        to the Arduino.
        '''
        # Send step time and number of channels
        self.ser.write(self.step_time.to_bytes(2, 'little'))
        self.ser.write(len(self.order).to_bytes(1, 'little'))
        if type(self.frames) == list:
            for i in range(len(self.frames)):
                self.ser.write(self.frames[i])
        else:
            self.ser.write(self.frames)

    def get_dmx_signal(self):
        '''Retrieve the converted binary output from
        the Arduino. Should only be used for testing.
        '''
        while True:
            if self.ser.in_waiting > 0:
                line = self.ser.readline().decode('utf-8').rstrip()
                return(line)

    @property
    def frames(self):
        return self.__frames

    @frames.setter
    def frames(self, frames):
        self.__frames = frames


if __name__ == '__main__':
    dmx = DMX()
    dmx.get_data()           # GUI
    #dmx.get_data('rgb.bin') # File
    dmx.send_data()
