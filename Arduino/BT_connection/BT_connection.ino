#include <SoftwareSerial.h>

SoftwareSerial BTSerial(2,3);

void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);
Serial.println("Arduino Hardware Initialized");
BTSerial.begin(9600);
Serial.println("HC-05 Bluetooth Initialized at 9600 Baud.");
}

void loop() {
  // put your main code here, to run repeatedly:
if (BTSerial.available()){
  Serial.write(BTSerial.read());
}
if (Serial.available()){
  BTSerial.write(Serial.read());
}
}
