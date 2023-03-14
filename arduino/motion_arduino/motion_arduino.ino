// define pins
#define  motionSensorPin  2;  
#define ledPin 3;           

int alertedRasPi = 0;

void setup() 
{
  pinMode(motionSensorPin, INPUT);
  pinMode(ledPin, OUTPUT);

  Serial.begin(9600);
}

void loop() 
{
  if (detectsMotion() && alertedRasPi ) 
  {
    sendMessageToRasPi();
  } 
  
  if ( hasMessageToRead() )
  {
    readRasPiMessage();
  }
}

int detectsMotion() 
{
  return digitalRead(motionSensorPin);
}

void sendMessageToRasPi()
{
  Serial.println("Tenho aqui gente");

  alertedRasPi = 1;
}

void readRasPiMessage()
{
  String data = Serial.readStringUntil('\n');
  Serial.print("You sent me: ");
  Serial.println(data);

  alertedRasPi = 0;
}

void hasMessageToRead()
{
  return Serial.available() > 0;
}


