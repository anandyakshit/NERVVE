void setup(){

  Serial.begin(115200);

}

void loop(){

  int raw = analogRead(A0);
  float voltage = raw * (5.0 /1023.0);

  Serial.print("Voltage: ");
  Serial.print(voltage, 3);
  Serial.println(" V");

}