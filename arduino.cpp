#include <Arduino.h>
#include <CytronMotorDriver.h>

#define PACKET_SIZE 8 // size of packet read from pi in bytes

CytronMD front_left(PWM_DIR, 3, 2);    //format is (specific h-drive connections), PWM pin, DIR pin
CytronMD back_left(PWM_DIR, 5, 4);
CytronMD front_right(PWM_DIR, 6, 7);
CytronMD back_right(PWM_DIR, 9, 8);

CytronMD digger(PWM_DIR, 13, 12);
const int linear_actuator_up = 10;
const int linear_actuator_down = 11;

class PiData {
private:
  bool tank_mode;
  byte joy_left_x;
  byte joy_left_y;
  byte joy_right_x;
  byte joy_right_y;
  byte dX;
  byte dY; //cCHANGE TO MATCH PYTHON 

public:
  /// Constructs a new empty PiData object
  PiData() {
    this->tank_mode = true; //false;
    this->joy_left_x = 127; // assume centered
    this->joy_left_y = 127;
//  this->joy_right_x = 127;
    this->joy_right_y = 127;
    this->dX = 127;
    this->dY = 127;
  }

  /// Attempts to read new data from the Pi in input buffer
  /// returns number of bytes read if successful, else -1
  int32_t update() {
    byte barr[PACKET_SIZE];
    int32_t result = Serial.readBytes(barr, PACKET_SIZE);

    if (result < PACKET_SIZE) {
      Serial.print("WARN: STDIN is either empty or recieved < than expected bytes\n");
      return -1;
    }

    if (barr[0] != 255 || barr[PACKET_SIZE - 1] != 255) {
      Serial.print("ERROR: First and last bytes are not 255. Skipping\n");
      return -1;
    }

    this->tank_mode = barr[1];
    this->joy_left_x = barr[2];
    this->joy_left_y = barr[3];
    this->dY = barr[4];
    this->joy_right_y = barr[5];
    this->dX = barr[6];
    //this->dY = barr[7];

    Serial.print("tank: ");
    Serial.print(this->tank_mode);
    Serial.print(" lx: ");
    Serial.print(this->joy_left_x);
    Serial.print(" ly: ");
    Serial.print(this->joy_left_y);
    Serial.print(" rx: ");
    Serial.print(this->joy_right_x);
    Serial.print(" ry: ");
    Serial.print(this->joy_right_y);
    Serial.print("Dpad x: ");
    Serial.print(this->dX);
    Serial.print("Dpad y: ");
    Serial.print(this->dY);
    Serial.print("\n");

    return result;
  }

  // Access methods
  bool get_tank_mode() { return this->tank_mode; }
  byte get_joy_left_x() { return this->joy_left_x; }
  byte get_joy_left_y() { return this->joy_left_y; }
  byte get_joy_right_x() { return this->joy_right_x; }
  byte get_joy_right_y() { return this->joy_right_y; }
  byte get_dpad_x() {return this->dX;}
  byte get_dpad_y() {return this->dY;}

};


PiData data; // new instance of PiData class to store our latest data

bool tank_set = PiData().get_tank_mode(); //allows us to flip the tank_mode
void tank_drive(PiData& data) {
  int left_pwm = map(data.get_joy_left_x(), 0, 255, -255, 255);     // Map joystick values (-min to max) to the PWM range (-255 to 255)
  int right_pwm = map(data.get_joy_left_y(), 0, 255, -255, 255);

  front_left.setSpeed(left_pwm);    // Set motors speeds
  back_left.setSpeed(left_pwm);
  front_right.setSpeed(right_pwm);
  back_right.setSpeed(right_pwm);
}

void differential_steering(PiData& data) {
  int left_x = map(data.get_joy_left_x(), 0, 255, -255, 255);
  int left_y = map(data.get_joy_left_y(), 0, 255, -255, 255);
// right_x
  int right_y = map(data.get_joy_right_y(), 0, 255, -255, 255);

  // Speed variables for both sides
  int left_speed = map(data.get_joy_left_y(), 0, 255, -255, 255);   // Speed for left motors (same for both)
  int right_speed = map(data.get_joy_right_y(), 0, 255, -255, 255);

  // Adjust speeds based on right_x (turning)
  if (left_x > 0) {
    right_speed *= 0.6;        // Move right motors slower when joystick is moved right
  } else if (left_x < 0) {
    left_speed *= 0.6;         // Move left motors slower when joystick is moved left
  }

  front_left.setSpeed(left_speed);
  back_left.setSpeed(left_speed);
  front_right.setSpeed(right_speed);
  back_right.setSpeed(right_speed);
}

void digging(PiData& data){
  int dpad_x = map(data.get_dpad_x(),-1,1,0,255);
  int dpad_y = map(data.get_dpad_y(),1,-1,0,255);

  if(dpad_x == 0) {tank_set = !tank_set;}
  if(dpad_x > 127) {digger.setSpeed(dpad_x);}

  
  if(dpad_y ==255) {digitalWrite(linear_actuator_up, HIGH); digitalWrite(linear_actuator_down, LOW);}
  else if(dpad_y == 0) {digitalWrite(linear_actuator_down, HIGH); digitalWrite(linear_actuator_up, LOW);}
  else {digitalWrite(linear_actuator_down, LOW); digitalWrite(linear_actuator_up, LOW);}
}

void setup() {
  Serial.begin(115200); // Start serial communication
}

void loop(){
  data.update();
  delay(1);
  digging(data); 
  if(tank_set) {tank_drive(data);}
  else {differential_steering(data);}
}