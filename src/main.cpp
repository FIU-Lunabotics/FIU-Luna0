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

bool corruptData = false;
bool outOfOrderData = false;
byte tempBarr[100];
int sizeOfTempBarr = 0;

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
        byte barr[PACKET_SIZE];
        int32_t result = Serial.readBytes(barr, PACKET_SIZE+1);
    
        if (corruptData == true){
          if (result < PACKET_SIZE+1) {
            corruptData = false;
            outOfOrderData= true;
            int i = 0;
            sizeOfTempBarr = result;
            for (i =0; i <= result; i++){
              tempBarr[i] = barr[i];
              }
            //Serial.print("ERROR (CORRUPT): First and last byte spacer isn't 0."); Serial.print("\nSkipping and adding to temp\n");
            return -1;
            }
          else if (barr[0] & start_byte_bm != 0b10101000 || barr[PACKET_SIZE]&end_byte_bm != 0b00010101) {
            corruptData = false;
            outOfOrderData = true;
            int i = 0;
            sizeOfTempBarr = result;
            for(i = 0; i < result;i++){
              tempBarr[i] = barr[i];
            }
            //Serial.print("ERROR (CORRUPT): First and last byte Spacer are not Correct\nSkipping and adding to temp\n"); 
            return -1;
            }
          }
        else if (outOfOrderData == true) {
          byte mergedTemp[100];
    
          byte possibleStartBytes[100];
          byte possibleEndBytes[100];
          int possStartByteIndex[100];
          int possEndByteIndex[100];
          int indexStart = 0;
          int indexEnd = 0;
          int i=0;
          int sizeOfMergedTemp = sizeOfTempBarr + result;
    
          for(i = 0; i <= sizeOfTempBarr;i++){
              mergedTemp[i] = tempBarr[i];
            }
          for(i = 0; i <= result;i++){
              mergedTemp[i+sizeOfTempBarr] = barr[i];
            }
          if (sizeOfMergedTemp < PACKET_SIZE+1) {
            //Serial.print("WARN: tempBuff is either empty or recieved < than expected bytes\n"); Serial.print("\nSkipping\n");
            return -1;  
          }
          else{
            for(i = 0; i <= sizeOfMergedTemp - 6; i++){
              if (mergedTemp[i]&start_byte_bm == 0b10101000){
                possibleStartBytes[indexStart] = mergedTemp[i];
                possStartByteIndex[indexStart] = i;
                indexStart += 1;
              } 
              if(i > PACKET_SIZE && mergedTemp[i]&end_byte_bm == 0b00010101){
                possibleEndBytes[indexEnd] = mergedTemp[i];
                possEndByteIndex[indexEnd] = i;
                indexEnd += 1;
               }
            }
            int j=0;
            int z =0;
            for(i=0; i <= indexStart; i++){
                  for(j=0; j <= indexEnd; j++){
                    if(possStartByteIndex[i] + PACKET_SIZE == possEndByteIndex[j]){
                      int spacer = possStartByteIndex[i];
                      for(z = 0; z < PACKET_SIZE; z++){
                        barr[z] = mergedTemp[z+spacer];
                      }
                    }
                  }
                }
          }
        }
          
        else {
          if (result < PACKET_SIZE+1){
            corruptData = true;
            droppedBytes += PACKET_SIZE - result + 1;
            if (idle == false){
              //Serial.print("WARN: STDIN is either empty or recieved < than expected bytes\n");
              idle = true;
            }
            return -1;
          }
    
          else if (barr[0] & start_byte_bm != 0b10101000 || barr[PACKET_SIZE] & end_byte_bm != 0b00010101) {
            corruptData = true;
            droppedBytes += 6;
            droppedPackets += 1;
            //Serial.print("ERROR: First and last byte spacer isn't 0."); Serial.print("\nDropped Packets: "); Serial.print(droppedPackets); Serial.print("\nDropped Bytes: "); Serial.print(droppedBytes); Serial.print("\nSkipping\n");
            return -1;
          }
          else {
            idle = false;
          }
          Serial.end();
          Serial.begin(9600);
        }    
    
        this->start_byte = barr[0];
        this->joy_left_x = barr[1];
        this->joy_left_y = barr[2];
        this->joy_right_y = barr[3];
        this->trigger = barr[4];
        this->end_byte = barr[5];
    
        return result;
      }
    
      // Access methods
      int get_south_button() { return this->start_byte&south_button_bm; }
      int get_east_button() { return this->start_byte&east_button_bm; }
      int get_west_button() { return this->start_byte&west_button_bm; }
      int get_north_button() { return this->end_byte&north_button_bm; }
      int get_left_bumper() { return this->end_byte&left_bumper_bm; }
      int get_right_bumper() { return this->end_byte&right_bumper_bm; }
      int get_joy_left_x() { return this->joy_left_x; }
      int get_joy_left_y() { return map(this->joy_left_y, 0, 255, 255, 0); }
      int get_joy_right_y() { return map(this->joy_right_y, 0, 255, 255, 0); }
      int get_trigger() { return this->trigger; } 
    
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

void loop(){
  data.update();
  get_tank_state(data);
}

void tank_drive(){

}

void diff_drive(){

}

void digging(){
  
}