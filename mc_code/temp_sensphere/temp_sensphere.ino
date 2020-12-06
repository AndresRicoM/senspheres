// Temperature Sen-Sphere MARK I

#include <SPI.h>
#include <SD.h>
#include <RF24.h>
#include <math.h>
#include <avr/io.h>

RF24 radio(1, 0);

int refPin = 6;
int ntcPin = 7;
int ledPin = 3;

const byte addresses [][6] = {"10911", "10917"}; // MSN, MSG

const char myID[6] = "IDT001";

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
  // put your main code here, to run repeatedly:
  Serial.print("Temperature is: ");
  //Serial.println(read_temp());
  send_rf_data(read_temp());
  digitalWrite(ledPin, HIGH);
  delay(250);
  digitalWrite(ledPin, LOW);
  delay(250);
  Serial.println("Sent New Data!");

}

float read_temp() {
  
  float Vref = analogRead(refPin);  //Reference Voltage.
  float Vntc = analogRead(ntcPin);  //Tension on NTC.
  float Intc = ((2*Vref) - Vntc) / 10000;
  float Rntc = Vntc / Intc;  //NTC Resistance Calculation.
  float Tk = 1 / ((log(Rntc / 10000) / 3750) + (1 / 298.15)); //Scale resistance to temperature in kelvin.
  float Tc = Tk - 273.15;  //Convert from Kelvin to Celsius. 

  return Tc;
  
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
