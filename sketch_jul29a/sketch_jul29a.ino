#include <SPI.h>
#include <LoRa.h>

#define SS_PIN    10
#define RST_PIN    9
#define DIO0_PIN   2


void setup() {

  Serial.begin(115200);

  delay(1000);

  Serial.println("NERVVE R4 Receiver");


  LoRa.setPins(SS_PIN, RST_PIN, DIO0_PIN);


  if (!LoRa.begin(433E6)) {

    Serial.println("LoRa FAILED");

    while (1);

  }


  LoRa.setSpreadingFactor(12);
  LoRa.setSignalBandwidth(125E3);
  LoRa.setCodingRate4(8);
  LoRa.enableCrc();


  Serial.println("READY");

}



void loop() {


  int packetSize = LoRa.parsePacket();


  if (packetSize) {

c
    String data = "";


    while (LoRa.available()) {

      data += (char)LoRa.read();

    }


    Serial.println(data);

    Serial.print("RSSI:");
    Serial.println(LoRa.packetRssi());


    Serial.print("SNR:");
    Serial.println(LoRa.packetSnr());


    Serial.println("----------------");


  }

}