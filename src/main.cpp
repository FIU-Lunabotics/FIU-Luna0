#include <Arduino.h>
//#include <CytronMotorDriver.h>

#define PACKET_SIZE 5 // size of packet read from pi in bytes

#define back_right 2
#define back_left 3
#define front_right 4
#define front_left 5
#define digger 6
#define tank__button 7
#define right_bumper 8
#define left_bumper 9


int droppedBytes = 0;
int droppedPackets = 0;

bool outOfOrderData = false;
byte barr[100];
int sizeOfBarr = 0;

//bm = bitmasks
const int north_button_bm = 0b10000000;
const int right_bumper_bm = 0b01000000;
const int left_bumper_bm  = 0b00100000;
const int start_byte_bm   = 0b11111000;
const int end_byte_bm     = 0b00011111;
const int south_button_bm = 0b00000100;
const int east_button_bm  = 0b00000010;
const int west_button_bm  = 0b00000001;

bool idle = false;
bool tank_button_temp = false;
bool tank_mode = false;

const int negative_deadzone = -15;
const int positive_deadzone =  15;





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
        byte tempBarr[PACKET_SIZE];
        int32_t result = Serial.readBytes(tempBarr, PACKET_SIZE+1);
        int result_ = result;
        int i = 0;

        for (i = 0; i <= result_; i++){ barr[i+sizeOfBarr] = tempBarr[i];}
        sizeOfBarr += result_;
        if (sizeOfBarr < PACKET_SIZE+1){
          return -1;
          }
        else if ((barr[0]&start_byte_bm) == 0b10101000 && (barr[PACKET_SIZE]&end_byte_bm) == 0b00010101){
          for (i = 0; i < PACKET_SIZE; i++){ tempBarr[i] = barr[i]; }
          for (i = 0; i <= sizeOfBarr; i++){ barr[i] = 0; }
          sizeOfBarr = 0;
        }
        else {
          byte possibleStartBytes[100];
          byte possibleEndBytes[100];
          int possStartByteIndex[100];
          int possEndByteIndex[100];
          int indexStart = 0;
          int indexEnd = 0;

          for(i = 0; i <= (sizeOfBarr - PACKET_SIZE); i++){
            if ((barr[i]&start_byte_bm) == 0b10101000){
              possibleStartBytes[indexStart] = barr[i];
              possStartByteIndex[indexStart] = i;
              indexStart += 1;
            } 
            if((barr[(i+PACKET_SIZE)]&end_byte_bm) == 0b00010101){
              possibleEndBytes[indexEnd] = barr[i+PACKET_SIZE];
              possEndByteIndex[indexEnd] = i+PACKET_SIZE;
              indexEnd += 1;
              }
          }
          int j=0;
          int z =0;
          bool foundPacket = false;
          int spacer = 0;
          for(i=0; i < indexStart; i++){
              for(j=0; j < indexEnd; j++){
                if(possStartByteIndex[i] + PACKET_SIZE == possEndByteIndex[j]){
                  foundPacket = true;
                  spacer = possStartByteIndex[i];
                  for(z = 0; z < PACKET_SIZE; z++){
                    barr[z] = tempBarr[z+spacer];
                  }
                }
              }
            }
          if (foundPacket){
            for (i = 0; i <= (spacer+PACKET_SIZE); i++){
              barr[i] = 0;
            }
            int extra_bytes = sizeOfBarr-spacer+PACKET_SIZE+1;
            if (extra_bytes != 0){
              for (i = 0; i<= extra_bytes; i++){
                barr[i] = barr[(i+(spacer+PACKET_SIZE+1))];
                barr[(i+(spacer+PACKET_SIZE+1))] = 0;
              }
            }
            sizeOfBarr = extra_bytes;
          }
          else { 
            Serial.print("\nPoss Start Byte Indexs:"); 
            for(i = 0; i < indexStart; i++){ 
              Serial.end();
              Serial.begin(9600);
              Serial.print(possStartByteIndex[i]);
              Serial.print("\n");
            }
            Serial.print("\n\nPoss End Byte Indexs:"); 
            for(i = 0; i < indexStart; i++){ 
              Serial.end();
              Serial.begin(9600);
              Serial.print(possStartByteIndex[i]);
              Serial.print("\n");
            }
            Serial.print("\n\nSize of buffer: "); Serial.print(sizeOfBarr);
            Serial.print("\n\n All Bytes in Barr: ");
            for(i = 0; i <= sizeOfBarr; i++){
              Serial.end();
              Serial.begin(9600);
              Serial.print("\n\n"); for (int8_t aBit = 7; aBit >= 0; aBit--) Serial.write(bitRead(barr[i], aBit) ? '1' : '0');
            }
            Serial.print("\n\nPacket not found.\nSkipping.\n");
            return -1;
          }
        }

        this->start_byte = tempBarr[0];
        this->joy_left_x = tempBarr[1];
        this->joy_left_y = tempBarr[2];
        this->joy_right_y = tempBarr[3];
        this->trigger = tempBarr[4];
        this->end_byte = tempBarr[5];
    
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
      int get_joy_left_y() { return map(this->joy_left_y, 0, 255, 255, 0); }
      int get_joy_right_y() { return map(this->joy_right_y, 0, 255, 255, 0); }
      int get_trigger() { return this->trigger; } 
      int get_start_byte() { return this->start_byte; }
      int get_end_byte() { return this->end_byte; }
    
    };


PiData data; // new instance of PiData class to store our latest data

void setup() {
  Serial.begin(9600); // Start serial communication
}

void get_tank_state(PiData& data){
  bool tank_button = data.get_north_button();
  if(tank_button == true && tank_button_temp == false){ tank_mode =! tank_mode; }
  tank_button_temp = tank_button;

  if (tank_mode){ analogWrite(tank__button, 255); }
  else{ analogWrite(tank__button, 0); }
}

void tank_drive(PiData& data){
  int left_pwm = data.get_joy_left_y(); //map(data.get_joy_left_x(), 0, 255, -255, 255);
  int right_pwm = data.get_joy_right_y(); //map(data.get_joy_left_y(), 0, 255, -255, 255);

  if (negative_deadzone < left_pwm && left_pwm < positive_deadzone){
    left_pwm = 0;
  }
  if (negative_deadzone < right_pwm && right_pwm < positive_deadzone){
    right_pwm = 0;
  }

  analogWrite(front_left, left_pwm);    // Set motors speeds
  analogWrite(back_left, left_pwm);
  analogWrite(front_right, right_pwm);
  analogWrite(back_right, right_pwm);
}

void diff_drive(PiData& data){
  int left_x = map(data.get_joy_left_x(), 0, 255, -255, 255);
  int left_y = map(data.get_joy_left_y(), 0, 255, -255, 255);

  if (negative_deadzone < left_y && left_y < positive_deadzone){
    left_y = 0;
  }

  int pwm_level = left_y + left_x*0.3;
  if (pwm_level > 255) { pwm_level = 255; }

  int left_pwm = pwm_level;
  int right_pwm = pwm_level;

  if (left_x > positive_deadzone){
    right_pwm *= map(left_x, -255, 255, 1.6, 0.6 );
  }
  else if (left_x < negative_deadzone){
    left_pwm *= map(left_x, -255, 255, 0.6, 1.6 );
  }

  analogWrite(front_left, left_pwm); 
  analogWrite(back_left, left_pwm);
  analogWrite(front_right, right_pwm);
  analogWrite(back_right, right_pwm);
}

void digging(PiData& data){
  bool bumper_left = data.get_left_bumper();
  bool bumper_right = data.get_right_bumper();

  if (bumper_left && bumper_right) {
    analogWrite(left_bumper, 0);
    analogWrite(right_bumper, 0);
  }
  else if (bumper_left == true) {
    analogWrite(left_bumper, 255);
  }
  else if (bumper_right == true) {
    analogWrite(right_bumper, 255);
  }
  else {
    analogWrite(left_bumper, 0);
    analogWrite(right_bumper, 0);
  }
}


void loop(){
  data.update();

  /*
  int Byte1 = data.get_start_byte();
  int Byte2 = data.get_joy_left_x();
  int Byte3 = data.get_joy_left_y();
  int Byte4 = data.get_joy_right_y();
  int Byte5 = data.get_trigger();
  int Byte6 = data.get_end_byte();
  Serial.end();
  Serial.begin(9600);
  Serial.print("\n\n"); for (int8_t aBit = 7; aBit >= 0; aBit--) Serial.print(bitRead(Byte1, aBit) ? '1' : '0');
  Serial.print("\n"); for (int8_t aBit = 7; aBit >= 0; aBit--) Serial.print(bitRead(Byte2, aBit) ? '1' : '0');
  Serial.print("\n"); for (int8_t aBit = 7; aBit >= 0; aBit--) Serial.print(bitRead(Byte3, aBit) ? '1' : '0');
  Serial.end();
  Serial.begin(9600);
  Serial.print("\n"); for (int8_t aBit = 7; aBit >= 0; aBit--) Serial.print(bitRead(Byte4, aBit) ? '1' : '0');
  Serial.print("\n"); for (int8_t aBit = 7; aBit >= 0; aBit--) Serial.print(bitRead(Byte5, aBit) ? '1' : '0');
  Serial.print("\n"); for (int8_t aBit = 7; aBit >= 0; aBit--) Serial.print(bitRead(Byte6, aBit) ? '1' : '0'); Serial.print("\n");
  
  Serial.print("\n");Serial.print("cycle");Serial.print("\n");
  Serial.end();
  Serial.begin(9600);
  */

  get_tank_state(data);
  if (tank_mode) { tank_drive(data); }
  else {diff_drive(data);}
  digging(data);
  Serial.end();
  Serial.begin(9600);
}