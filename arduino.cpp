#include <Arduino.h>
#include <CytronMotorDriver.h>

#define PACKET_SIZE 5 // size of packet read from pi in bytes

#define back_right 2
#define back_left 3
#define front_right 4
#define front_left 5
#define digger 6
#define tank__button 7
#define right_bumper 8
#define left_bumper 9

//bm = bitmasks
const int north_button_bm = 0b10000000;
const int right_bumper_bm = 0b01000000;
const int left_bumper_bm  = 0b00100000;
const int start_byte_bm   = 0b00111000;
const int end_byte_bm     = 0b00011100;
const int south_button_bm = 0b00000100;
const int east_button_bm  = 0b00000010;
const int west_button_bm  = 0b00000001;

bool idle = false;
bool tank_button_temp = false;
bool tank_mode = false;

const int negative_deadzone = -5;
const int positive_deadzone =  5;

class PiData {
private:
  byte start_byte;
  byte joy_left_x;
  byte joy_left_y;
  byte joy_right_y;
  byte trigger;
  byte end_byte; //cCHANGE TO MATCH PYTHON 

public:
  /// Constructs a new empty PiData object
  PiData() {
    this->start_byte = 0b00000000; //false;
    this->joy_left_x = 127; // assume centered
    this->joy_left_y = 127;
    this->joy_right_y = 127;
    this->trigger = 0;
    this->end_byte = 0b00000000;
  }

  /// Attempts to read new data from the Pi in input buffer
  /// returns number of bytes read if successful, else -1
  int32_t update() {
    byte barr[PACKET_SIZE];
    int32_t result = Serial.readBytes(barr, PACKET_SIZE+1);

    if (result < PACKET_SIZE+1) {
      if (idle == false){
        Serial.print("WARN: STDIN is either empty or recieved < than expected bytes\n");
        idle = true;
      }
      return -1;
    }
    idle = false;

    if (barr[0] & start_byte_bm != 0b00101000 || barr[PACKET_SIZE] & end_byte_bm != 0b00010100) {
      Serial.print("ERROR: First and last bytes spacer are not correct. Skipping\n");
      return -1;
    }

    this->start_byte = barr[1];
    this->joy_left_x = barr[2];
    this->joy_left_y = barr[3];
    this->joy_right_y = barr[4];
    this->trigger = barr[5];
    this->end_byte = barr[6];

    //Serial.print("tank: ");
    //Serial.print(this->tank_mode);
    Serial.print(" lx: ");
    Serial.print(this->joy_left_x);
    Serial.print(" ly: ");
    Serial.print(this->joy_left_y);
    //Serial.print(" rx: ");
    //Serial.print(this->joy_right_x);
    Serial.print(" ry: ");
    Serial.print(this->joy_right_y);
    //Serial.print("Dpad x: ");
    //Serial.print(this->dX);
    //Serial.print("Dpad y: ");
    //Serial.print(this->dY);
    Serial.print("\n");

    Serial.end();
    Serial.begin(9600);

    return result;
  }

  // Access methods
  bool get_south_button() { return this->start_byte&south_button_bm; }
  bool get_east_button() { return this->start_byte&east_button_bm; }
  bool get_west_button() { return this->start_byte&west_button_bm; }
  bool get_north_button() { return this->end_byte&north_button_bm; }
  bool get_left_bumper() { return this->end_byte&left_bumper_bm; }
  bool get_right_bumper() { return this->end_byte&right_bumper_bm; }
  int get_joy_left_x() { return this->joy_left_x; }
  int get_joy_left_y() { return this->joy_left_y; }
  int get_joy_right_y() { return this->joy_right_y; }
  int get_trigger() { return this->trigger; } 

};


PiData data; // new instance of PiData class to store our latest data

void setup() {
  Serial.begin(9600); // Start serial communication
}

void loop(){
  data.update();
  delayMicroseconds(1);
  get_tank_state();
  if(tank_mode) {tank_drive(data);}
  else {differential_steering(data);}
  digging(data); 
}                         

void get_tank_state(){
  bool tank_button = data.get_north_button();
  if (tank_button == true && tank_button_temp == false){
    tank_mode = !tank_mode;
  }
  tank_button_temp = tank_button;
  if(tank_mode == true){
    analogWrite(tank__button, HIGH);
  } 
  else{
    analogWrite(tank__button, LOW);
  }
}

void tank_drive(PiData& data) {
  int left_pwm = map(data.get_joy_left_x(), 0, 255, -255, 255);     // Map joystick values (-min to max) to the PWM range (-255 to 255)
  int right_pwm = map(data.get_joy_left_y(), 0, 255, -255, 255);

  if (negative_deadzone < left_pwm < positive_deadzone){
    left_pwm = 0;
  }
  if (negative_deadzone < right_pwm < positive_deadzone){
    right_pwm = 0;
  }

  analogWrite(front_left, left_pwm);    // Set motors speeds
  analogWrite(back_left, left_pwm);
  analogWrite(front_right, right_pwm);
  analogWrite(back_right, right_pwm);
}

void differential_steering(PiData& data) {
  int left_x = map(data.get_joy_left_x(), 0, 255, -255, 255);
  int left_y = map(data.get_joy_left_y(), 0, 255, -255, 255);

  if (negative_deadzone < left_y < positive_deadzone){
    left_y = 0;
  }

  // Speed variables for both sides
  int left_speed = left_y;   // Speed for left motors (same for both)
  int right_speed = left_speed;

  // Adjust speeds based on right_x (turning)
  if (left_x > 0) {
    right_speed *= map(left_x, -255, 255, 1.6, 0.6 );        // Move right motors slower when joystick is moved right
  } else if (left_x < 0) {
    left_speed *= map(left_x, -255, 255, 0.6, 1.6 );         // Move left motors slower when joystick is moved left
  }

  analogWrite(front_left, left_speed); 
  analogWrite(back_left, left_speed);
  analogWrite(front_right, right_speed);
  analogWrite(back_right, right_speed);
}

void digging(PiData& data){
  int trigger = data.get_trigger();
  bool bumper_left = data.get_left_bumper();
  bool bumper_right = data.get_right_bumper();

  if (bumper_left == true) {
    analogWrite(left_bumper, HIGH);
  }
  else {
    analogWrite(left_bumper, LOW);
  }
  if (bumper_right == true) {
    analogWrite(right_bumper, HIGH);
  }
  else{
    analogWrite(right_bumper, LOW);
  }
  analogWrite(digger, trigger);
}
