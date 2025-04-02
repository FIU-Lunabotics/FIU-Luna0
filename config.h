//tank drive and differential steering w/ Cytron library
//By Carlos Carroz
//Date: 3/20/2025
//Version: 1
#include <CytronMotorDriver.h>

CytronMD front_left(PWM_DIR, 3, 2);    //format is (specific h-drive connections), PWM pin, DIR pin
CytronMD back_left(PWM_DIR, 5, 4);
CytronMD front_right(PWM_DIR, 6, 7);
CytronMD back_right(PWM_DIR, 9, 8);
