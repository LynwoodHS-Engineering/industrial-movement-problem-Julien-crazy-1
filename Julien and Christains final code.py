from vex import *
import urandom


brain = Brain()


left_drive_smart = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
right_drive_smart = Motor(Ports.PORT10, GearSetting.RATIO_18_1, True)
drivetrain = DriveTrain(left_drive_smart, right_drive_smart, 319.19, 295, 40, MM, 1)
claw_motor = Motor(Ports.PORT11, GearSetting.RATIO_18_1, False)
arm_motor = Motor(Ports.PORT20, GearSetting.RATIO_18_1, False)



ai_vision_5__GreenBall = Colordesc(2, 72, 190, 72, 24, 0.28)
ai_vision_5 = AiVision(Ports.PORT5, ai_vision_5__GreenBall)


wait(30, MSEC)




# Set speeds
drivetrain.set_drive_velocity(30, PERCENT)
drivetrain.set_turn_velocity(30, PERCENT)
arm_motor.set_velocity(50, PERCENT)
claw_motor.set_velocity(50, PERCENT)


# Target bounding box properties with tolerance
TARGET_CENTER_X = 130
TARGET_CENTER_Y = 220
TARGET_WIDTH = 225
TARGET_HEIGHT = 40
TOLERANCE = 10  # pixels


def is_target_position(obj):
   return (
       abs(obj.centerX - TARGET_CENTER_X) <= TOLERANCE and
       abs(obj.centerY - TARGET_CENTER_Y) <= TOLERANCE and
       abs(obj.width - TARGET_WIDTH) <= TOLERANCE and
       abs(obj.height - TARGET_HEIGHT) <= TOLERANCE
   )


def perform_task():
   # Open claw before approaching ball
   claw_motor.spin_for(REVERSE, 200, DEGREES)


   # Vision loop to find and approach ball
   while True:
       ai_vision_5_objects = ai_vision_5.take_snapshot(ai_vision_5__GreenBall)


       if ai_vision_5_objects[0].exists:
           if ai_vision_5_objects[0].centerX > 190:
               drivetrain.turn_for(RIGHT, 5, DEGREES)
           elif ai_vision_5_objects[0].centerX < 130:
               drivetrain.turn_for(LEFT, 5, DEGREES)
           else:
               # Drive forward if ball is smaller or not at target bounding box
               if not is_target_position(ai_vision_5_objects[0]):
                   drivetrain.drive(FORWARD)
               else:
                   drivetrain.stop()
                   # Close claw to grab ball when bounding box matches target
                   claw_motor.spin_for(FORWARD, 90, DEGREES)
                   break
       else:
           drivetrain.stop()


       wait(5, MSEC)


   # Part 2: Deliver and reset
  
    drivetrain.drive_for( REVERSE, 10, INCHES)
    wait(1.5, SECONDS)
    arm_motor.spin_for(REVERSE, 100, DEGREES)
    wait(1,SECONDS)
    drivetrain.turn_for(LEFT, 190, DEGREES)
    wait(2,SECONDS)
    drivetrain.drive_for(FORWARD, 80, INCHES)
    wait(1,SECONDS)
    arm_motor.spin_for(FORWARD, 730, DEGREES)
    wait(1,SECONDS)
    drivetrain.drive_for(FORWARD, 35, INCHES)
    arm_motor.spin_for(REVERSE, 110, DEGREES)
    claw_motor.spin_for(FORWARD, 150, DEGREES)
    wait(.5,SECONDS)
    claw_motor.spin_for(REVERSE,150, DEGREES)
    wait(.5,SECONDS)
    arm_motor.spin_for(FORWARD, 110, DEGREES)
    wait(1,SECONDS)
    drivetrain.drive_for(REVERSE, 15, INCHES)
    wait(1,SECONDS)
    arm_motor.spin_for(REVERSE,730,DEGREES)
    wait(2,SECONDS)
    drivetrain.turn_for(RIGHT, 190, DEGREES)
    drivetrain.drive_for(FORWARD, 20, INCHES)
