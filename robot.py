#!/usr/bin/env python3

import magicbot
import wpilib
import ctre

class Robot(magicbot.MagicRobot):
    def createObjects(self):
        """Create motors and stuff here."""
        self.joystick = wpilib.Joystick(0)
        self.climb_motor = ctre.WPI_TalonSRX(1)
        

    def teleopInit(self):
        """Initialise driver control."""
        pass

    def teleopPeriodic(self):
        """Allow the drivers to control the robot."""
        y = -self.joystick.getY()
        self.climb_motor.set(ctre.ControlMode.PercentOutput,y/2)
    
    def disabledInit(self):
        self.climb_motor.set(ctre.ControlMode.PercentOutput,0)


if __name__ == "__main__":
    wpilib.run(Robot)

