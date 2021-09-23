// create array
int incoming[3];

// Include the Servo library 
#include <Servo.h> 
// Declare the Servo pin 
int servoPin = 3; 
// Create a servo object 
Servo Servo1; 

void setup(){
  Serial.begin(9600);
  pinMode(LED_BUILTIN,OUTPUT);
  Servo1.attach(servoPin); 
  Servo1.write(90);
}
int value;
void loop(){
  while(Serial.available() >= 4)
  {
    // fill array
    for (int i = 0; i < 4; i++)
    {
      incoming[i] = Serial.read();
    }

    if(incoming[1]==0)
    {
      value = 90 - (incoming[0]);
    }
    else
    {
      value = 90 + (incoming[0]);
    }
       Servo1.write(value); 

    }
  }
