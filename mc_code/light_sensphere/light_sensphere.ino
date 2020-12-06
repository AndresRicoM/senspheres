// Light Sen-Sphere MARK I

#include <SPI.h>
#include <SD.h>
#include <RF24.h>
#include <math.h>
#include <avr/io.h>

RF24 radio(1, 0);

int photoPin = 6;
int ledPin = 3;

const byte addresses [][6] = {"10911", "10917"}; // MSN, MSG

const char myID[6] = "IDL002";

void setup() {

  Serial.begin(115200);
  
  pinMode(photoPin, INPUT);
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
  // put your main code here, to run repeatedly:
  Serial.print("Light is: ");
  //Serial.println(read_light());
  send_rf_data(read_light());
  digitalWrite(ledPin, HIGH);
  delay(250);
  digitalWrite(ledPin, LOW);
  delay(250);
  Serial.println("Sent New Data!");

}

float read_light() {

  float lightread = analogRead(photoPin);

  return lightread;
  
}

void send_rf_data(float message) { //Function sends a command via radio. Takes string as argument and converts to char to send. 

  //char mess[4] = "000";
  char temperatureValue[6];
  char fullmessage[14];
  strcpy(fullmessage, myID);
  strcat(fullmessage, ":");
  dtostrf(message, 6, 2, temperatureValue);
  strcat(fullmessage, temperatureValue);
  //strcpy(mess, message.c_str());
  Serial.println(fullmessage);
  radio.stopListening();
  radio.write(&fullmessage, sizeof(fullmessage));
  
}
