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

  printToLCD(9, 0, previousFloor);

  if (buttonState == HIGH){ // if true the user called the elevator
  int direction = (currentFloor > previousFloor) ? 1 : -1;
  for (int i = previousFloor; i != currentFloor + direction; i += direction){
    printToLCD(9, 0, i);
    delay(timeToChangeFloor); 
    printToLCD(9, 0, " ");
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

/* NAO APAGAR
int readDistance() {
  const int trigPin = 4;
  const int echoPin = 5;
  
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  long duration = pulseIn(echoPin, HIGH);
  int distance = duration * 0.034 / 2;
  
  return distance;
}
*/

void printToLCD(int collumn, int row, char* content)
{
  lcd.setCursor(collumn, row, content);
  lcd.print(content);
}

