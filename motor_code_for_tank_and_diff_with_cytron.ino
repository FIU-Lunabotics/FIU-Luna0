#include "communication.h"
#include "config.h"
#include "driving_modes.h"

void setup() {
  Serial.begin(9600); // Start serial communication
}

void loop(){
  if (resolution > 0) {       // Check if data is available (has to be send as four values separated by comma)


    if (north_button == 1){
      tank_drive_mode = !tank_drive_mode;
    }
    if (tank_drive_mode){
      tank_drive();
    }else{
      differential_steering();
    }
  }
}