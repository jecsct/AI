/* Inside Elevator Arduino (SLAVE) - LCD */
#include "Wire.h"
#include <LiquidCrystal.h> 
#include <stdio.h>
LiquidCrystal lcd(11, 12, 3, 4, 5, 6);  
int currentFloor = 0;
int buttonPin = 7;

// variables will change:
int buttonState = 0;

int slave = 2;

const int controller = 0;

void setup() {
  // Starts serial for output
  Serial.begin(9600);

  analogWrite(2,100); // lcd contrast
  lcd.begin(16, 2); // lcd number of columns and rows
  lcd.setCursor(0, 0); // lcd start position

  Wire.begin(slave);

  Wire.onReceive(receiveEvent); // when master sends a message
} 

void loop() {

}

// Triggered when the Access gets interrupted to read the message from the Controller
void receiveEvent(int howMany) {
  if (howMany == 1) {  // Extra security check (how many bytes were sent)
    char floor = Wire.read();
    currentFloor = (int) floor;
    printToLCD(currentFloor);
  }
  
}

void printToLCD(int content) {
  lcd.begin(9,0);
  lcd.print(content);
}
