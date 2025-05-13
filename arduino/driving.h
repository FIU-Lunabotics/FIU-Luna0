void tank_drive() {
  int left_pwm = map(left_y, 255, -255, -255, 255);     // Map joystick values (-min to max) to the PWM range (-255 to 255)
  int right_pwm = map(right_y, 255, -255, -255, 255);

  front_left.setSpeed(left_pwm);    // Set motors speeds
  back_left.setSpeed(left_pwm);
  front_right.setSpeed(right_pwm);
  back_right.setSpeed(right_pwm);
}

void differential_steering() {
  // Speed variables for both sides
  int left_speed = right_y;   // Speed for left motors (same for both)
  int right_speed = right_y;  // Speed for right motors (same for both)

  // Adjust speeds based on right_x (turning)
  if (right_x > 0) {
    right_speed *= 0.6;        // Move right motors slower when joystick is moved right
  } else if (right_x < 0) {
    left_speed *= 0.6;         // Move left motors slower when joystick is moved left
  }

  front_left.setSpeed(left_speed);
  back_left.setSpeed(left_speed);
  front_right.setSpeed(right_speed);
  back_right.setSpeed(right_speed);
}