#include <Arduino.h>
#include <CytronMotorDriver.h>

#define PACKET_SIZE 5 // size of packet read from pi in bytes

int droppedBytes = 0;
int droppedPackets = 0;

bool corruptData = false;
bool outOfOrderData = false;
byte tempbarr[];

CytronMD front_left(PWM_DIR, 3, 2);    //format is (specific h-drive connections), PWM pin, DIR pin
CytronMD back_left(PWM_DIR, 5, 4);
CytronMD front_right(PWM_DIR, 6, 7);
CytronMD back_right(PWM_DIR, 9, 8);
int count = 0;
int diff_speed = 0.6;
int positive_deadzone = 5;
int negative_deadzone = -5;
bool temp_tank_button = 0;

//controller input
// int left_x = 0;
// int left_y = 0;
// int right_x = 0;
// int right_y = 0;
// int left_stick = 0;
// int right_stick = 0;
// int dpad_x = 0;
// int dpad_y = 0;
// int left_trigger = 0;
// int right_trigger = 0;
// int select = 0;
// int start = 0;
bool north_button = 0;
bool east_button = 0;
bool south_button = 0;
bool west_button = 0;
bool left_bumper = 0;
bool right_bumper = 0;
char trigger = 0;

bool tank_drive_mode = false;

//bm = bitmasks
int north_button_bm = 0b10000000;
int right_bumper_bm = 0b01000000;
int left_bumper_bm  = 0b00100000;
int start_byte_bm   = 0b00111000;
int end_byte_bm     = 0b00011100;
int south_button_bm = 0b00000100;
int east_button_bm  = 0b00000010;
int west_button_bm  = 0b00000001;


class PiData {
private:
  byte start_byte;
  byte joy_left_x;
  byte joy_left_y;
  byte joy_right_y;
  char trigger;
  byte end_byte;

public:
  /// Constructs a new empty PiData object
  PiData() {
    this->start_byte = 0b00000000;
    this->joy_left_x = 127; // assume centered
    this->joy_left_y = 127;
    this->joy_right_y = 127;
    this->trigger = 0;
    this->end_byte_byte = 0b00000000;
  }

  /// Attempts to read new data from the Pi in input buffer
  /// returns number of bytes read if successful, else -1
  int32_t update() {
    
    byte barr[PACKET_SIZE];
    int32_t result = Serial.readBytes(barr, PACKET_SIZE+1);
    
    if (count == 3) {
      count = 0;
    
    if(corruptData == TRUE){
      if (result < PACKET_SIZE+1) {
        corruptData = FALSE
        outOfOrderData = TRUE
        count += 1;
        for(i = 0; i < (sizeof(barr));i++){
          tempBarr[i] = barr[i];
        }
        Serial.print("WARN (CORRUPT): STDIN is either empty or recieved < than expected bytes\n"); Serial.print("\nSkipping and adding to temp\n");
        return -1;  
      }
      else if (barr[0]&start_byte_bm != 0 || barr[PACKET_SIZE]&end_byte_bm != 0) {
        corruptData = FALSE
        outOfOrderData = TRUE
        count += 1;
        for(i = 0; i < (sizeof(barr));i++){
          tempBarr[i] = barr[i];
        }
        Serial.print("ERROR (CORRUPT): First and last byte spacer isn't 0."); Serial.print("\nSkipping and adding to temp\n");
        return -1;
      }
      else if (barr[0]>>6 != count || barr[PACKET_SIZE]&0b00000011 != count) {
        corruptData = FALSE
        outOfOrderData = TRUE
        count += 1;
        for(i = 0; i < (sizeof(barr));i++){
          tempBarr[i] = barr[i];
        }
        Serial.print("ERROR (CORRUPT): First and last byte Identifier are not "); Serial.print(count); Serial.print("\nSkipping and adding to temp\n"); 
        return -1;
      }
    }
    else if(outOfOrderData == TRUE){
      byte mergedTemp[];

      byte possibleStartBytes[];
      byte possibleEndBytes[];
      int possStartByteIndex[];
      int possEndByteIndex[];
      int indexStart = 0;
      int indexEnd = 0;

      for(i = 0; i < (sizeof(tempBarr));i++){
          mergedTemp[i] = tempBarr[i];
        }
      for(i = 0; i < (sizeof(barr));i++){
          mergedTemp[i+sizeof(tempBarr)-1] = barr[i];
        }
      
      if (mergedTemp < PACKET_SIZE+1) {
        count += 1;
        Serial.print("WARN: tempBuff is either empty or recieved < than expected bytes\n"); Serial.print("\nSkipping\n");
        return -1;  
      }
      else {
        for(i = 0; i < sizeof(mergedTemp); i++;){
          if (mergedTemp[i]&start_byte_bm == 0){
            possibleStartBytes[indexStart] = mergedTemp[i]
            possStartByteIndex[indexStart] = i
            indexStart += 1
          } 
          if(i > PACKET_SIZE && mergedTemp[i]&end_byte_bm == 0){
            possibleEndBytes[indexEnd] = mergedTemp[i]
            possEndByteIndex[indexEnd] = i
            indexEnd += 1
           }
        }
        for(i=0; i < sizeof(possibleStartBytes); i++;){
            for(j=0; j < sizeof(possibleEndBytes); j++;){
              if(possStartByteIndex[i] + PACKET_SIZE == possEndByteIndex[j] && possibleStartBytes[i]>>6 == possibleEndBytes[j] & 0b00000011){
                for(z = 0; z <= PACKET_SIZE; z++;){
                  barr[z] = mergedTemp[z+i];
                }
              }
            }
          }
        }
      }
      else {
       if (result < PACKET_SIZE+1) {
        corruptData = TRUE
        count += 1;
        droppedBytes += PACKET_SIZE - result;
        droppedPackets += 1;
        Serial.print("WARN: STDIN is either empty or recieved < than expected bytes\n"); Serial.print("\nDropped Packets: "); Serial.print(droppedPackets); Serial.print("\nDropped Bytes: "); Serial.print(droppedBytes); Serial.print("\nSkipping\n");
        return -1;  
      }
      else if (barr[0]&start_byte_bm != 0 || barr[PACKET_SIZE]&end_byte_bm != 0) {
        corruptData = TRUE
        droppedBytes += 6;
        droppedPackets += 1;
        count += 1;
        Serial.print("ERROR: First and last byte spacer isn't 0."); Serial.print("\nDropped Packets: "); Serial.print(droppedPackets); Serial.print("\nDropped Bytes: "); Serial.print(droppedBytes); Serial.print("\nSkipping\n");
        return -1;
      }
      else if (barr[0]>>6 != count || barr[PACKET_SIZE]&0b00000011 != count) {
        corruptData = TRUE
        Serial.print("ERROR: First and last byte Identifier are not "); Serial.print(count); Serial.print("\nDropped Packets: "); Serial.print(droppedPackets); Serial.print("\nDropped Bytes: "); Serial.print(droppedBytes); Serial.print("\nSkipping\n"); 
        if (count > barr[0]>>6) {
          droppedBytes += 4 - count + barr[0]>>6 + 1;
          droppedPackets += 1;
        }
        else {
          droppedBytes +=  barr[0]>>6 - count;
          droppedPackets += 1;
        }
        return -1;
      }
      else {
        count += 1;
      }
    }

    this->start_byte = barr[0];
    this->joy_left_x = barr[1];
    this->joy_left_y = barr[2];
    this->joy_right_y = barr[3];
    this->trigger = barr[4];
    this->end_byte = barr[PACKET_SIZE];

    /*
    Serial.print("Start: "); Serial.print(this->start_byte);
    Serial.print(" lx: "); Serial.print(this->joy_left_x);
    Serial.print(" ly: "); Serial.print(this->joy_left_y);
    Serial.print(" ry: "); Serial.print(this->joy_right_y);
    Serial.print("Trigger: "); Serial.print(this->trigger);
    Serial.print("End: "); Serial.print(this->end_byte);
    Serial.print("\n");
    */
  }

  // Access methods
  bool get_south_button() { return if(this->start_byte&south_button_bm); }
  bool get_east_button() { return if(this->start_byte&east_button_bm); }
  bool get_west_button() { return if(this->start_byte&west_button_bm); }
  bool get_north_button() { return if(this->end_byte&north_button_bm); }
  bool get_left_bumper() { return if(this->end_byte&left_bumper_bm); }
  bool get_right_bumper() { return if(this->end_byte&right_bumper_bm); }
  byte get_joy_left_x() { return this->joy_left_x; }
  byte get_joy_left_y() { return this->joy_left_y; }
  byte get_joy_right_y() { return this->joy_right_y; }
  byte get_trigger() { return this->trigger; }
};


PiData data; // new instance of PiData class to store our latest data

int (*tank_drive_button)() = data.get_north_button;

void setup() {
  Serial.begin(9600); // Start serial communication
}

void loop(){
  data.update();
  if (tank_drive_button == 1 && temp_tank_button == 0){!tank_drive_mode};
  temp_tank_button = tank_drive_button;
  if (tank_drive_mode == 1){`
    tank_drive(data);
  }
  else {
    differential_drive(data);
  }
  delay(1);
}

void tank_drive(const PiData& data) {
  int left_pwm = map(data.get_joy_left_y(), 0, 255, -255, 255);     // Map joystick values (-min to max) to the PWM range (-255 to 255)
  int right_pwm = map(data.get_joy_right_y(), 0, 255, -255, 255);

  if (negative_deadzone < left_pwm < positive_deadzone) {
    left_pwm = 0;
  }
  if (negative_deadzone < right_pwm < positive_deadzone) {
    left_pwm = 0;
  }

  front_left.setSpeed(left_pwm);    // Set motors speeds
  back_left.setSpeed(left_pwm);
  front_right.setSpeed(right_pwm);
  back_right.setSpeed(right_pwm);
}

void differential_drive(const PiData& data) {
  int left_pwm = map(data.get_joy_left_y(), 0, 255, -255, 255);   // Speed for left motors (same for both)
  int left_joy_x = map(data.get_joy_left_x(), 0, 255, -255, 255);
  
  if (negative_deadzone < left_pwm < positive_deadzone) {
    left_pwm = 0;
  }

  int right_pwm = left_pwm;
  
  // Adjust speeds based on right_x (turning)
  if (left_joy_x > positive_deadzone) {
    right_speed *= diff_speed*(left_x/255);        // Move right motors slower when joystick is moved right
  } 
  else if (left_joy_x < negative_deadzone) {
    left_speed *= diff_speed*(left_x/255)*(-1);         // Move left motors slower when joystick is moved left
  }

  front_left.setSpeed(left_speed);
  back_left.setSpeed(left_speed);
  front_right.setSpeed(right_speed);
  back_right.setSpeed(right_speed);
}

