#include <SPI.h>
#include <LoRa.h>

#define SS_PIN    10
#define RST_PIN    9
#define DIO0_PIN   2


String btBuffer = "";


void setup() {

  Serial.begin(115200);      // USB debug
  Serial1.begin(9600);       // HC-05

  delay(1000);

  Serial.println("NERVVE Mega Sender Starting");


  LoRa.setPins(SS_PIN, RST_PIN, DIO0_PIN);


  if (!LoRa.begin(433E6)) {

    Serial.println("LoRa INIT FAILED");

    while (1);

  }


  Serial.println("LoRa Ready");


  // Maximum reliable settings
  LoRa.setTxPower(17, PA_OUTPUT_PA_BOOST_PIN);

  LoRa.setSpreadingFactor(12);

  LoRa.setSignalBandwidth(125E3);

  LoRa.setCodingRate4(8);

  LoRa.enableCrc();


  Serial.println("NERVVE Sender Ready");

}



void loop() {


  // Read HC-05 without blocking

  while (Serial1.available()) {

    char c = Serial1.read();


    if (c == '\n') {


      btBuffer.trim();


      if (btBuffer.length() > 0) {


        Serial.print("BT RX: ");
        Serial.println(btBuffer);


        sendLoRa(btBuffer);


      }


      btBuffer = "";

    }

    else {

      btBuffer += c;

    }

  }

}



void sendLoRa(String message) {


  Serial.println("Sending LoRa packet...");

  Serial.print("Length: ");
  Serial.println(message.length());


  LoRa.beginPacket();


  LoRa.print(message);


  int result = LoRa.endPacket();


  if (result == 1) {

    Serial.println("LoRa SENT");

  }

  else {

    Serial.println("LoRa FAILED");

  }


  Serial.println("----------------");

}