#define back_right 2
#define back_left 3
#define front_right 4
#define front_left 5
#define digger 6
#define tank__button 7
#define right_bumper 8
#define left_bumper 9

bool increasing = true;
int pwm = 0;


void setup() {
  // put your setup code here, to run once:

}

void loop() {
  analogWrite(front_left, pwm); 
  analogWrite(back_left, pwm);
  analogWrite(front_right, pwm);
  analogWrite(back_right, pwm);
  analogWrite(digger, pwm);
  analogWrite(tank__button, pwm);
  analogWrite(right_bumper, pwm);
  analogWrite(left_bumper, pwm);
  if (pwm == 255){
    increasing = false;
  }
  if (pwm == 0){
    increasing = true;
  }
  if (increasing){
    pwm += 1;
  }
  else{
    pwm -= 1;
  }
  delay(10);
}
