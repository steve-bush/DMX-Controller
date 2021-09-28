#include <DMXSerial.h>

const int buffer_size = 5120;
byte dmx_out[buffer_size];

void setup() {
  Serial.begin(115200);
  DMXSerial.init(DMXController);
}

void loop() {
  if (Serial.available() > 0) {                                // If data is recaived sends data
    union                                                      // Union to read the integer step time in
    {
      int stepi;
      byte stepb[2];
    } step_time;
    
    Serial.readBytes(step_time.stepb, 2);                      // Read the step time

    byte num_channels_temp[1];
    Serial.readBytes(num_channels_temp, 1);                    // Read the number of channels from serial
    byte num_channels = num_channels_temp[0];

    size_t num_bytes = Serial.readBytes(dmx_out, buffer_size); // Read the dmx data into data_out
    size_t num_packets = num_bytes/num_channels;               // Number of times to change light values
    
    for (int i = 0; i < num_packets; i++) {
      for (int j = 0; j < num_channels; j++) {
        DMXSerial.write(j+1, dmx_out[i*num_channels+j]);       // Set the channel value to new one
      }
      delay(step_time.stepi);                                  // Delay until the time step is over
    }
    
  }
}
