const byte MAB[2] = {1, 1};
const byte START_BIT = 0;
const byte START_FRAME[8] = {0, 0, 0, 0, 0, 0, 0, 0};
const byte STOP_BITS[2] = {1, 1};
const byte MBB[3] = {1, 1, 1};

byte data_out[512];
int num_frames;

void setup() {
  Serial.begin(115200);                                     // Start the serial connection at 115200 baud
  Serial.flush();
}

void loop() {
  // Get frames and send back DMX signal
  if (Serial.available() > 0) {                   // If the raspberry pi sends data and break time has passed
    num_frames = Serial.readBytes(data_out, 512); // Read the serial data into data_out

    Serial.print(MAB[0]);                         // Send mark after break bits
    Serial.print(MAB[1]);

    Serial.print(START_BIT);                      // Send the frame start bit
    for (int i = 7; i >= 0; i--) {
      Serial.print(START_FRAME[i]);               // Send the start frame
    }
    Serial.print(STOP_BITS[0]);                   // Send the stop bits for each frame
    Serial.print(STOP_BITS[1]);

    for (int i = 0; i < num_frames; i++) {        // Loop through the data frames
      Serial.print(START_BIT);                    // Send the frame start bit
      byte frame = data_out[i];
      for (int j = 0; j < 8; j++) {               // Loop through the bits in the frames
        Serial.print(frame & 01);                 // Send each bit LSB first
        frame >>= 1;                              // Shift bits to the left
      }
      Serial.print(STOP_BITS[0]);                 // Send the stop bits for each frame
      Serial.print(STOP_BITS[1]);
    }

    Serial.print(MBB[0]);                         // Send the mark before break bits
    Serial.print(MBB[1]);
    Serial.print(MBB[2]);
    Serial.print('\n');                           // Send 0 for break in data sending (\n for test)
  }
}
