/* Wall Elevator Arduino (MAYBE MASTER) - Floor Buttons */
#include "Wire.h"

#define FLOORS_NUM 8

#define HOLD_PERIOD 2000
#define FLOOR_CHANGE_PERIOD 2000
#define CLOSE_PERIOD 2000
#define LIGHT_PERIOD 10000

// Controller identification
const int controller = 0;

// Floors
const int buttonPins[FLOORS_NUM] = {2, 3, 4, 5, 6, 7, 8, 9};
const int floors[FLOORS_NUM] = {-1, 0, 1, 2, 3, 4, 5, 6};

const int light = 12;

int currentButtonState[FLOORS_NUM];
int lastButtonState[FLOORS_NUM];

bool buttonPressed[FLOORS_NUM] = {false, false, false, false, false, false, false, false};

int currentFloor = 0;
int destinationFloor = 0;
int sourceFloor = 0;
bool doorIsOpen = false;

unsigned long previousMillisFloorChange = 0; // Will store last time X was updated

unsigned long handleDoorStartTime = 0;
unsigned long handleLightStartTime = 0;

bool buttonPressedFlag = false;
unsigned long startTime = 0;
bool flag = false;
bool travelFlag = false;
bool pendingTravel = false;

bool handleDoorFlag = false;
bool handleLightFlag = false;

bool destinationArrived = true;

bool started = false;

bool outsideRequest = false;

void setup() {
  Serial.begin(9600);

  // Initialize the pushbutton pins as inputs:
  for(int i=0; i<FLOORS_NUM; i++)
    pinMode(buttonPins[i], INPUT);

  pinMode(light, OUTPUT);
  

  // Master communication
  Wire.begin(controller);

  Wire.onReceive(receiveEvent);
}

void loop() {

  if(!started) {
    started = true;
    for(int i=0; i<FLOORS_NUM; i++)
      buttonPressed[i]=false;
    sendCurrentFloor();
  }

  for(int i=0; i<FLOORS_NUM; i++)
    checkButtonPressed(i);
  
  handlePressButtonTime();

  if(travelFlag) handleFloorChange();

  if(doorIsOpen) digitalWrite(light, HIGH);

  if(destinationArrived) handleDoorTime();

  if(!doorIsOpen && !travelFlag) {
    handleLight();
  }

  if (Serial.available() > 0) {
    int data = Serial.read() - '0';

    if (data == 7) { // -1 floor
      data = -1;
    }

    Serial.print("You sent me: ");
    Serial.println(data);
    buttonPressed[data+1] = true;
    travel();
  }

}

void receiveEvent(int howMany) {
  if(howMany == 1) {
    char floor = Wire.read();

    int nextStop = (int)floor;

    Serial.print("Floor ");
    Serial.print(nextStop);
    Serial.print(" called!!");

    buttonPressed[nextStop+1] = true;
    travel();

    outsideRequest = true;
  }
}

void sendCurrentFloor() {
  int destination = 2; // MUDAR
  Wire.beginTransmission(destination);  // transmit to device
  Wire.write(currentFloor);                  
  Wire.endTransmission();
}

void handleDoorTime() {
  if (!handleDoorFlag) {
    handleDoorFlag = true;
    handleDoorStartTime = millis();
  }
  if ((millis() - handleDoorStartTime >= CLOSE_PERIOD) && handleDoorFlag) {
    if(doorIsOpen) closeDoor();
    handleDoorFlag = false;
  }
}

void handleLight() {
  if (handleLightFlag) {
    handleLightFlag = false;
    handleLightStartTime = millis();
  }
  if ((millis() - handleLightStartTime >= LIGHT_PERIOD) && !handleLightFlag) {
    digitalWrite(light, LOW);
  }
}


void checkButtonPressed(int i) {
  lastButtonState[i] = currentButtonState[i];          // Stores the previous state of the push button
  currentButtonState[i] = digitalRead(buttonPins[i]);  // Stores the present state of the push button
  if (lastButtonState[i] == HIGH && currentButtonState[i] == LOW) {
    if(!buttonPressed[i]) {
      buttonPressedFlag = true;
      sendDestinationToPi(floors[i]);
    }
    
    buttonPressed[i] = true;
    
    Serial.print("Button floor ");
    Serial.print(floors[i]);
    Serial.println(" has been pressed.");
  }
}

void handlePressButtonTime() {
  if (buttonPressedFlag) {
    buttonPressedFlag = false;
    startTime = millis();
    flag = true;

    if (travelFlag) {
      pendingTravel = true;
      //Serial.println("Estrou aqui crl");
    }
  }

  if ((millis() - startTime >= HOLD_PERIOD) && flag) {
    flag = false;
    Serial.println("PASSOU 3 SEGUNDOS.");
    if(!travelFlag)
      travel();
  }
}

void travel() {
  int* pressedFloors = getPressedFloors();

  int floor = getClosestDestinationFloor(pressedFloors);

  destinationFloor = floor;
  sourceFloor = currentFloor;

  if(currentFloor == destinationFloor && !doorIsOpen) {
    Serial.print("You're already at your destination: floor ");
    Serial.println(currentFloor);
    openDoor();
    return;
  }

  if(doorIsOpen) closeDoor();

  previousMillisFloorChange = millis();
  travelFlag = true;
}

void handleFloorChange() {
  if (millis() - previousMillisFloorChange >= FLOOR_CHANGE_PERIOD) {
    
    if(destinationFloor < currentFloor) 
      currentFloor--;
    else
      currentFloor++;

    sendCurrentFloor();

    Serial.print("Floor changed to ");
    Serial.println(currentFloor);
    
    if(currentFloor == destinationFloor) {
      Serial.println("Arrived at destination!!!!!");
      openDoor();
      travelFlag = false;
      buttonPressed[currentFloor+1] = false;
      destinationArrived = true;
      
      if(outsideRequest) {
        sendSourceToPi(currentFloor);
        outsideRequest = false;
      }
      
      if(isTravelPending()) {
        Serial.println("Going to next pending floor!");
        destinationArrived = false;
        travel();
      } 
      return;
    }

    previousMillisFloorChange = millis(); // update the previous time
  }
}

void sendSourceToPi(int floorSource) {
  // send message
  switch(floorSource) {
    case -1: Serial.println("SRC-1"); break;
    case 0: Serial.println("SRC0"); break;
    case 1: Serial.println("SRC1"); break;
    case 2: Serial.println("SRC2"); break;
    case 3: Serial.println("SRC3"); break;
    case 4: Serial.println("SRC4"); break;
    case 5: Serial.println("SRC5"); break;
    case 6: Serial.println("SRC6"); break;
    default: break;
  }
}

void sendDestinationToPi(int floorDestination) {
  // send message
  switch(floorDestination) {
    case -1: Serial.println("DST-1"); break;
    case 0: Serial.println("DST0"); break;
    case 1: Serial.println("DST1"); break;
    case 2: Serial.println("DST2"); break;
    case 3: Serial.println("DST3"); break;
    case 4: Serial.println("DST4"); break;
    case 5: Serial.println("DST5"); break;
    case 6: Serial.println("DST6"); break;
    default: break;
  }
}

void openDoor() {
  doorIsOpen = true;
  //Serial.println("OPEN");
  Serial.println("OPENING DOOR");
}

void closeDoor() {
  doorIsOpen = false;
  handleLightFlag = true;
  //Serial.println("CLOS");
  Serial.println("CLOSING DOOR");
}

bool isCloser(int a, int b, int cur) {
    return abs(a - cur) < abs(b - cur);
}

int myAbs(int x) {
  if (x < 0)
    return -x;
  else 
    return x; 
}

bool isTravelPending() {
  int n = 0;
  for(int i = 0; i<FLOORS_NUM; i++) {
    if(buttonPressed[i])
      n++;
  }
  if(n>0) return true;
  return false;
}


int* getPressedFloors() {
  int num = 0;
  for(int i=0; i<FLOORS_NUM; i++) {
    if (buttonPressed[i]) {
      num++;
    }
  }

  if(num == 0) return 0;

  int* res = new int[num];
  int index = 0;
  for(int i=0; i<FLOORS_NUM; i++) {
    if (buttonPressed[i]) {
      res[index++] = floors[i];
    }
  }
  return res;
}

int getClosestDestinationFloor(int dest[]) {
  if(sizeof(dest) == 1) {
    return dest[0];
  }
  int closest = dest[0];
  for(int i=0; i<sizeof(dest); i++) {
    if(isCloser(dest[i], closest, currentFloor))
      closest = dest[i];
  }
  return closest;
}
