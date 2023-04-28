#include <Servo.h>
#include <UltrasonicSensor.h>

UltrasonicSensor ultrasonic(11, 12);

int mm=0;
int cm=0;
Servo myservo;  
int distanc=0;
int pos = 0;  

void setup() {
  
  myservo.attach(9);
  Serial.begin(9600);
  // attaches the servo on pin 9 to the servo object

}

void loop() {
  
  distance = ultrasonic.distanceInMillimeters();
  pos= Serial.read();
  Serial.println("position to go");
  Serial.print(pos);
  if (pos > distance){
    Serial.println(distance);
   
    if (pos!=distance){
      myservo.write(180); 
       if(pos==distance){
      myservo.detach();
    }
    }
   
    Serial.println(distance);

  }

  if(pos<distance){
     if (pos!=distance){
      myservo.write(0); 
       if(pos==distance){
      myservo.detach();
    }
  }}

   if(pos==distance){
      myservo.detach();
    }

//  for (mm = 0; mm <= 11; mm += 1) { // goes from 0 degrees to 180 degrees
//    // in steps of 1 degree
//    myservo.write(180);              // tell servo to go to position in variable 'pos'
//    delay(1130);  
//    Serial.println(mm);            // waits 15ms for the servo to reach the position
//  }
// 
//  mm=0;
//  cm=cm+1;
//  Serial.println(cm);

}
