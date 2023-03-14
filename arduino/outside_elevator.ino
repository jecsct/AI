#include <LiquidCrystal.h> 
#include <stdio.h>
LiquidCrystal lcd(11, 12, 3, 4, 5, 6);  
bool onCurrentFloor = false;
int previousFloor = -1; //ask the other arduino
int currentFloor = 4;
int whereToGo = 7; //ask the other arduino
int buttonPin = 7;
int timeToChangeFloor = 1000;

// variables will change:
int buttonState = 0;

 void setup()
 {
    pinMode(buttonPin, INPUT); // pushbutton pin as an input

    analogWrite(2,100); // lcd contrast
    lcd.begin(16, 2); // lcd number of columns and rows
    lcd.setCursor(0, 0); // lcd start position
    lcd.print("Current: ");
  } 
void loop(){
  buttonState = digitalRead(buttonPin);

  lcd.setCursor(9, 0);
  lcd.print(previousFloor);

  if (buttonState == HIGH){ // if true the user called the elevator
  int direction = (currentFloor > previousFloor) ? 1 : -1;
  for (int i = previousFloor; i != currentFloor + direction; i += direction){
    lcd.setCursor(9, 0);
    lcd.print(i);
    delay(timeToChangeFloor); 
    lcd.setCursor(9, 0);
    lcd.print("  ");
    previousFloor = i;
  }
}
  }

  // tem aqui um bug
  if(previousFloor == currentFloor){
    if (whereToGo != currentFloor){
      currentFloor = whereToGo;
    }
  }
}
