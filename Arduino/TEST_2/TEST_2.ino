// create array 0- x angle 1-x direction. 2-y angle. 3 y direction. 4- z direction.
int incoming[3]; 

void setup(){
  Serial.begin(9600);
  pinMode(LED_BUILTIN,OUTPUT);
}

void loop(){
  while(Serial.available() >= 4 )
  {
    // fill array
    for (int i = 0; i < 4; i++)
    {
      incoming[i] = Serial.read();
    }
    

    // use the values
    if((incoming[0] >= 0 && incoming[1] == 1) && (incoming[2] >= 0 && incoming[3] == 1))
    {
      digitalWrite(LED_BUILTIN,HIGH);
    }
    else
    { 
      digitalWrite(LED_BUILTIN,LOW);
    }

  }
}
