import pygame
print(pygame.__version__)

pygame.init()
joystick = pygame.joystick.Joystick(0)

while True:
	event = pygame.event.wait()
	if event.type == pygame.JOYDEVICEADDED:
		joystick.init()	
		break


print("Connected")

while True:
	print(joystick.get_axis(1))



