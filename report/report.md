# DMX Project Part 1

by: Steven Bush and Nicholas Clapp

## 1. Introduction

The goal of this project was to create the equivalent of a usb to DMX device. For the first part of the project, we decided to focus on 3 goals. The first is transferring data from a PC to a Raspberry Pi. The second is processing the user input into a string of bytes to an Arduino. Lastly, the Arduino converts the byte string into DMX output and returns the DMX packet to the Raspberry Pi. Nicholas handled the transfer of data from the PC to the Raspberry Pi. Steve worked on processing the user input into a byte string, the Arduino, and creating a GUI for easy user input.

## 2. Technical Overview

In section 2.1, we give a quick overview of DMX signals and how they are output. Section 2.2 contains the use of the Raspberry Pi and PC. Lastly, the explanation of why we decided to use the Arduino is discussed in section 2.3.

### 2.1 DMX Protocol

DMX serves as the industry standard for stage lighting applications in theaters. For this application the non-standard 3-pin XLR connector with one ground pin and two data pins is used. The two data pins are balanced signals where the non-inverting pin is labeled data+ and the inverting pin is labeled data-. Data+ corresponds with the desired output while data- will be the opposite. These data pins will be read in by the light at 250,000 baud or every 4 microseconds. The data that the lights read are sent in groups called frames which have the following layout when looking at the Data+ pin for 0 being the low state and 1 being the high state.

1. Start bit: 0
2. 8 bits or 1 byte of data 0-255 in value (LSB first)
3. Mark Between Frames (MBF): 1, 1

The individual frames are sent together in a DMX packet which can contain up to 512 frames. For lighting applications, three of the frames are used for a red, green, and blue value, allowing for a DMX packet of only three frames when one light is present. Below, is an overview of the data that would be sent for a DMX packet.

1. Mark After Break (MAB): 1, 1
2. Start Frame or Frame 0: 0x00 (lighting applications only)
3. 512 Frames
4. Mark Before Break (MBB): 1, 1
5. Break: 0 for ~44 bit cycles

The official protocol is simple to understand and implement, but in practice the abnormal clock speed and poor following of standards by manufacturers makes this a difficult problem.

### 2.2 Raspberry Pi and PC

The first goal when setting up this project is making the system as easy to use as possible. If we employ the use of the Raspberry Pi in the system, we can make the whole system lightweight and easy to move around. Using an ethernet connection, we can remotely access our Raspberry Pi from our PC in order to setup and execute the program.
In order to accomplish this, we need to setup a few things and find some of our IP settings to make everything connect. In November 2016, Raspian disables secure shell by default in order to help secure the Raspberry Pi system. There are a couple of ways to change this setting. The easiest method (and the one I used) is connecting the Raspberry Pi to a screen through HDMI and using a USB mouse to go to change the setting.

1. Go to Preferences->Raspberry Pi Configuration
2. Navigate to the Interfaces tab and Enable SSH.

The other method for changing this setting involves inserting the Raspberry Pi SD card into a computer and creating new files before returning it to the Pi.

1. Open the boot (l:) drive
2. Create a blank file named "ssh"  Note: this file can be empty, all that matters is that the name is correct.

Once that is complete, we need to find the IP addresses of both the desired PC and the Raspberry Pi. With this information, we can use a program such as PuTTY to connect to the RPi through its terminal.
From here we can now access all of the files available on the Raspberry Pi, and can run our program through the terminal on the Pi.

### 2.3 Arduino

Due to the lack of reliability of the Raspberry Pi for real timing application, a microcontroller is needed for this project. We decided to use an Arduino for its ease of prototyping and library availability. The Arduino used is a Mega 2560 since it was already owned. In theory, any Arduino could be used for this project.

The Arduino is used to collect the data from the Raspberry Pi over their serial connection, process the data into an array of ones and zeros, and send the processed data back to the Raspberry Pi for testing. As stated in section 2.2, the data from the Raspberry Pi will be a string of bytes for each frame which needs to be processed into the DMX protocol packet.

## 3. Implementation

The different software and libraries used are discussed in this section. An explanation of the Arduino code is given in section 3.1 while the python code is discussed in section 3.2.

### 3.1 Arduino code

The Arduino starts by initializing an array of 4,097 bytes. This array holds the data part of the DMX packet for the 512 data frames. It also creates an array of 5,649 bytes to hold the data+ pin values for 512 frames. Next it sits in the loop function forever, waiting for serial data to be sent to it. Once data becomes available, the string is read in, and each character is subtracted by ‘0’ (easy char to int conversion) and inserted into the data array. Lastly, the output of the Data+ pin is sent back to the Raspberry Pi following the protocol from section 2.1. For data transfer between the Arduino and Raspberry Pi, the print and readBytes functions of the Serial library are used. The code for storing the data+ pin values will not be used for this project, but could be used for implementing actual DMX output later.

### 3.2 Python Code

The two methods of collecting user input to send to the light are discussed in this section. The first method of binary file parsing is discussed in section 3.2.1. The second method with the GUI is discussed in section 3.2.2. Both of these methods are implemented in the DMX class.

#### 3.2.1 Input Processing

Since the other DMX team's binary input is not known yet, we decided on a format of the first two bytes in the file being the number of data frames to send followed by the individual bytes that make up the frames. Two of the DMX classes are used for the binary input. The first creates the binary file for the user. The second parses the file and stores the data to be sent.

#### 3.2.2 GUI

The GUI is created through the use of the PyQt5 library. The GUI contains sliders and line edits that allow the user to change the red, green, and blue values, a button that changes color depending on the input, and a submit button to close out of the GUI. When the sliders are changed the value in the line edit box is changed accordingly and vice versa. The sliders and line edits both have their own actions to update the values in the code. The sliders are inherently protected from invalid inputs, but the line edits require additional processing to ensure a numeric value is input and to handle empty text boxes. If an invalid input is typed, the text function ignores the input and assigns a value of 0 for the color. Additionally, the value for each input is stored in a dictionary which is set up with appropriate protections. There is extra code in the GUI class allowing for additional inputs if a light is used that takes in more than the normal three frames of data.

## 4. Unit Tests

There were two main sections of the code that needed testing. The first is the GUI and binary input methods working as discussed in section 4.1. The second is the output for the different input methods as discussed in section 4.2.

### 4.1 Input Methods

The binary method is tested for an input of r:0, g:1, and b:2. This test checks both the binary file writing function and the binary to frames function. Additional tests were not needed due to the use of assert statements throughout both of these functions.

The GUI is tested using input from the QTest module in PyQt5. The tests check that changing the sliders affects the line edits and that the line edits affect the sliders. Next the line edits are checked for invalid inputs such as negative numbers, characters, and numbers over 255. The sliders are not checked since they cannot physically be set incorrectly. Lastly, the output from the GUI is checked to be correct for an input of r:1, g:1, and b:1.

### 4.2 Arduino Output

The Arduino’s output is tested for 3 cases. The first being whether the GUI works with the Arduino for an input of r:1, g:1, and b:1. The second test is for a binary file input of r:0, g:1, and b:2. The last test is whether the Arduino can handle an input of 512 frames.

## 5. Future Work

We have a nice start for creating a USB to DMX converting device. The work of converting the data from base 10 to binary then binary to DMX is done. From here we will need to look at the binary format that the other team has created and write code for the PC or Raspberry Pi to read their file. If they have multiple packets to send at varying times, the ability to control that will need to be added. Additionally, writing the C code for the Arduino to send the DMX bits at the correct speed will need to be worked on.

# DMX Project Part 2

by: Steven Bush

## 1. Introduction

The goal of this project was to create a DMX controller for transmitting DMX signal. I did this using an Arduino that is connected to either a PC or a Raspberry Pi. The process of getting the Arduino to send the signal took the bulk of the time while making the light change color over time did not. The goal of making this work for a Raspberry Pi failed due to me being electronically challenged. The files in this repo and in Kelli's repo work well together for making lightshows play with music.

## 2. Methods

The process of making the Arduino send the DMX signal in a way that the light would understand was not an easy task. I had started by trying to use the serial pin to send the data which would take care of the time for me. This seemed to work to make the light flash, but was not the right color. Then I tried using the 16-bit timer in the Arduino to accurately calculate 4 us. Setting up the timer took nearly 5 us, so it was useless. My last non-library attempt was to use an assembly command,`nop`, from the Atmel documents that causes nothing to happed for one cycle or 64.5 ns. This did the same as the serial method I first tried where the color was wrong and the light only pulsed.

In a last ditch attempt, I tried the DMXSerial library. This library suprisingly kept the light on by constantly sending the signal which I guess is a requirement. By testing with this code, I realized that the light channels were not 1-red, 2-green, 3-blue. They were actually 1-brightness, 2-red, 3-green, 4-blue. To get the library to use Serial1 for the output, uncomment line 33 of `DMXSerial_avr.h`. A picture of the circuitry to allow a DMX output is below. The MAX485 chip is an inverter which is needed for the inverting signal.

![DMX circuit diagram](circuit.png)

The last goal of the project was fairly simple to add into the original python code from project 1. I based my code off of the sample code given in Canvas, but changed it slightly for my application in how the frames are stored. Then I changed the function for sending serial data to pass the desired step time and number of channels to use to the Arduino. The channels for each DMX receiving setting for the light are:
A
1. brightness
2. red
3. green
4. blue
5. SOS
6. strobing
7. No clue the colors make no sense

d
1. brightness
2. red
3. green
4. blue

## 3. Results

Unlike project 1, the unit tests are not an indicator of this project working. To test that none of the original functionality works, the Arduino code that goes with the test script is in `test_arduino_dmx`. I have tested the code on the light for various inputs and that is the best I can do for this project. From what I have read, some libraries work with some lights while some will cause an error. The DMXSerial library seems more reliable than some of the other I tried, but there are some which do not use the serial port that may be more reliable. The non-serial libraries require additional boards, so they could not be tested by me.

## 4. Future Work

The project was mostly successful aside from failing to replace the Arduino with a Raspberry Pi. The binary file from running Kelli's `binarytodmx.py` script successfully controls the light. If I was to coninue this project, I would try to get a Raspberry Pi 400 (the keyboard one) to take place of the Arduino. From the bit of looking through the Broadcom chip documentitation, the code for the Arduino would look similar to that of the Raspberry Pi with less abstraction and different register names.

## 5. In Memoriam

This report is dedicated to both Dr. Robert's Raspberry Pi and my Raspberry Pi. I guess voltage dividers are harder to make than I thought.
