/* Outside Elevator Arduino (SLAVE) - Floor Button + LCD */
#include "Wire.h"
#include <LiquidCrystal.h> 
#include <stdio.h>
LiquidCrystal lcd(11, 12, 3, 4, 5, 6);  
int currentFloor = 0;
int myFloor = 4; // Change if wants to change floor
int buttonPin = 7;

// variables will change:
int buttonState = 0;

int slave = 2;

bool buttonPressed = false;

const int controller = 0;

void setup() {
  // Starts serial for output
  Serial.begin(9600);

  pinMode(buttonPin, INPUT); // pushbutton pin as an input

  analogWrite(2,100); // lcd contrast
  lcd.begin(16, 2); // lcd number of columns and rows
  lcd.setCursor(0, 0); // lcd start position

  Wire.begin(slave);

  Wire.onReceive(receiveEvent); // when master sends a message
} 

void loop() {

  buttonState = digitalRead(buttonPin);

  if (buttonState == HIGH) { // if true the user called the elevator
    // send floor to master 
    sendMyFloor();
  }
}

// Triggered when the Access gets interrupted to read the message from the Controller
void receiveEvent(int howMany) {
  if (howMany == 1) {  // Extra security check (how many bytes were sent)
    char floor = Wire.read();
    currentFloor = (int) floor;
    printToLCD(currentFloor);
  }
  
}

void sendMyFloor() {
  Wire.beginTransmission(controller);  // transmit to device
  Serial.println("Sending msg to master");
  Wire.write(myFloor);                  
  Wire.endTransmission();
}


void printToLCD(int content) {
  lcd.begin(9,0);
  lcd.print(content);
}
