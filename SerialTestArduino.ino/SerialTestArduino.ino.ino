void setup() {
  //first thing that runs:
  Serial.begin(115200);

  while (!Serial){
    ; //wait for serial port to connect
  }
}
const char TERMINATOR = '|';

void loop() {
  //waiting for command from Jetson...
  if (Serial.available() > 0){
    String commandFromJetson = Serial.readStringUntil(TERMINATOR);

    //confirm
    String ackMsg = "This is what I got from the jetson: " + commandFromJetson;

    Serial.print(ackMsg);
    //serial.flush
  }
  delay(500);
}
