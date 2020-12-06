////Sen-Sphere Receiver MARK I

#include <SPI.h>
#include <SD.h>
#include <RF24.h>
#include <avr/io.h>

RF24 radio(1, 0);

const byte addresses [][6] = {"10917" , "10911" }; // MSN, MSG Reversed from transmitters

int refPin = 6;
int ntcPin = 7;
int ledPin = 3;

void setup() {
  
Serial.begin(115200);
  
  pinMode(refPin, INPUT);
  pinMode(ntcPin, INPUT);
  pinMode(ledPin, OUTPUT);

  Serial.println("Starting Up Radio!");
  radio.begin();
  radio.openWritingPipe(addresses[1]);
  radio.openReadingPipe(1, addresses[0]);      
  radio.setPALevel(RF24_PA_MIN);
  radio.startListening();  
  Serial.println("Radio has been started!");
  Serial.println("Ready to begin!");

}

void loop() {

  print_radio();

}

void print_radio() {
  
  radio.startListening();

  if (radio.available()) {                      //Looking for the data.{
      
      char incoming[100] = "";                      //Saving the incoming data
      radio.read(&incoming, sizeof(incoming));    //Reading the data
      Serial.println(incoming);
      digitalWrite(ledPin, HIGH);
      delay(10);
      digitalWrite(ledPin, LOW);
      delay(10);

    }
}
