// create array
int incoming[3];

void setup(){
  Serial.begin(9600);
  pinMode(LED_BUILTIN,OUTPUT);
}

void loop(){
  while(Serial.available() >= 4)
  {
    // fill array
    for (int i = 0; i < 4; i++)
    {
      incoming[i] = Serial.read();
    }

    // use the values
    for(int i=0;i<incoming[1];i++)
    {
      digitalWrite(LED_BUILTIN,HIGH);
      delay(200);
      digitalWrite(LED_BUILTIN,LOW);
      delay(200);
    }
    delay(1000);
    for(int i=0;i<incoming[1];i++)
    {
      digitalWrite(LED_BUILTIN,HIGH);
      delay(200);
      digitalWrite(LED_BUILTIN,LOW);
      delay(200);
    }
    delay(1000);
    for(int i=0;i<incoming[1];i++)
    {
      digitalWrite(LED_BUILTIN,HIGH);
      delay(200);
      digitalWrite(LED_BUILTIN,LOW);
      delay(200);
    }   
    delay(1000);
    for(int i=0;i<incoming[1];i++)
    {
      digitalWrite(LED_BUILTIN,HIGH);
      delay(200);
      digitalWrite(LED_BUILTIN,LOW);
      delay(200);
    }
  }
}
