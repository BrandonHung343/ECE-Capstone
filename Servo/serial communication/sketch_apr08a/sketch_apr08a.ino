int r = 1;
void setup(){
  Serial.begin(9600);
}
void loop(){
  if(Serial.available()){         //From RPi to Arduino
    String data = Serial.readStringUntil('\n');  //conveting the value of chars to integer
    Serial.println(data);
  }
}
