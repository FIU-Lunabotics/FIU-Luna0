//controller input
int north_button = 0;
int east_button = 0;
int south_button = 0;
int west_button = 0;
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
int left_bumper = 0;
int right_bumper = 0;
// int select = 0;
// int start = 0;
bool tank_drive_mode = true;

//serial buffer data wtf tha fuc
const int byte_read_resolution = 8;
int bytes_transferred = 0;
byte buffer[byte_read_resolution-1];

int button1Byte = buffer[0];
int left_joystick_x = buffer[1];
int left_joystick_y = buffer[2];
int right_joystick_y = buffer[3]; 
int button2Byte = buffer[4];

void read_serial(){
  if(Serial.available() != 0){
    bytes_transferred = Serial.readBytes(buffer, byte_read_resolution);
  }
}

void interpret_serial(){

}