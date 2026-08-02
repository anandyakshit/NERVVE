#include <SPI.h>
#include <LoRa.h>


#define SS_PIN    10
#define RST_PIN    9
#define DIO0_PIN   2


volatile bool packetReceived = false;



void dioISR() {

  packetReceived = true;

}



void setup() {


  Serial.begin(115200);


  delay(3000);


  Serial.println("NERVVE R4 Receiver Starting");



  LoRa.setPins(
    SS_PIN,
    RST_PIN,
    DIO0_PIN
  );



  if(!LoRa.begin(433E6)) {


    Serial.println("LoRa INIT FAILED");

    while(1);


  }



  Serial.println("LoRa READY");



  LoRa.setSpreadingFactor(12);

  LoRa.setSignalBandwidth(125E3);

  LoRa.setCodingRate4(8);

  LoRa.enableCrc();



  attachInterrupt(
    digitalPinToInterrupt(DIO0_PIN),
    dioISR,
    RISING
  );



  LoRa.receive();



  Serial.println("NERVVE Listening");


}



void loop() {


  if(packetReceived) {


    packetReceived = false;


    int packetSize = LoRa.parsePacket();



    if(packetSize) {


      String data = "";


      while(LoRa.available()) {

        data += (char)LoRa.read();

      }
      Serial.println(data);
    }


    LoRa.receive();


  }


}