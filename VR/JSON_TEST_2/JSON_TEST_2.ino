#define ARDUINOJSON_USE_LONG_LONG 1
#define ARDUINOJSON_USE_DOUBLE 1


#include <ESP8266WiFi.h>
#include <WiFiClient.h> 
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>

const char* wifiName = "Home";
const char* wifiPass = "welcome@123";


const char *host = "http://192.168.0.2:8080/sensors.json";

DynamicJsonDocument doc(8192);
float ACC_X_Y_Z()
{
  float accel_data[2] = {0};
  HTTPClient http;    //Declare object of class HTTPClient
  http.begin(host);
  http.useHTTP10(true);
  int httpCode = http.GET();
  if(httpCode == 200)
  {
    DeserializationError error = deserializeJson(doc, http.getStream());
    if (error) 
    {
      Serial.print(F("deserializeJson() failed: "));
      Serial.println(error.f_str());

    }
    JsonObject accel = doc["accel"];
    JsonArray accel_data = accel["data"];
    JsonArray accel_data_74_1 = accel_data[74][1];
    accel_data[0] = accel_data_74_1[0]; // 0.14167748
    accel_data[1] = accel_data_74_1[1]; // 0.12245542
    accel_data[2] = accel_data_74_1[2]; // 9.820484
    return accel_data;

    
    Serial.println(accel_data_74_1[0]);
  }
  else
  {
    Serial.println("Error in response");    
  }

  http.end();
}


void setup() 

{
  
  Serial.begin(115200);
  delay(10);
  Serial.println();
/*********************************WIFI*******************************/
  Serial.print("Connecting to ");
  Serial.println(wifiName);
  WiFi.begin(wifiName, wifiPass);
  while (WiFi.status() != WL_CONNECTED) 
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());   //You can get IP address assigned to ESP
/***********************************************************************/

}


void loop() 
{
 //float xyz[2] = {0};
 ACC_X_Y_Z();
// Serial.println(xyz[1]);
}
