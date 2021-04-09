#include <FeedBackServo.h>

// define feedback signal pin and servo control pin
#define FEEDBACK_PIN 3
#define SERVO_PIN 5

// set feedback signal pin number
FeedBackServo servo = FeedBackServo(FEEDBACK_PIN);
void setup(){
  Serial.begin(9600);
  // set servo control pin number
  servo.setServoControl(SERVO_PIN);
  // set Kp to proportional controller
  servo.setKp(1.0);
}
void loop(){
  int angle; 
  if(Serial.available()){         //From RPi to Arduino
    String data = Serial.readStringUntil('\n');  //conveting the value of chars to integer
    angle = data.substring(6,8).toInt();
    servo.rotate(angle*3, 4);
    Serial.println(angle);
  }

  
  
}
