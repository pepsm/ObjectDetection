#include <Servo.h> 
String readString;

int servoPin = 3; 
Servo sv;
int svVal = 90;
int svSpeed = 1;

void setup() {
  Serial.begin(115200);
  sv.attach(servoPin);
  delay(50);
  sv.write(svVal); 
}

void loop()
{
  
  readString = "";  
  while (Serial.available())
  {
    delay(20);  //delay to allow buffer to fill 
    if (Serial.available() >0)
    {
      char c = Serial.read();  
      readString += c;
    }
  }
  
  if(readString == "-1")
  {
    svVal -= svSpeed;
  }else if(readString == "1"){
    svVal += svSpeed;
  }

  
  if(svVal < 0){
    svVal = 0;
  }else if(svVal > 180){
    svVal = 180;  
  }
  
  sv.write(svVal);
  delay(20); 
  
  Serial.print(readString);

  
}
