import rev
import ctre
import wpilib
from utilities.pid import PID


class Lift:
    lift_motor: rev.CANSparkMax
    drive_motor: ctre.TalonSRX

    left_limit_switch: wpilib.DigitalInput
    right_limit_switch: wpilib.DigitalInput

    # Lift Constants
    GROUND_OFFSET = 5  # motor rotations

    # TODO get values
    # heights in metres
    LIFT_METRES_PER_REV = 0.002

    UP_HEIGHT = 5
    DOWN_HEIGHT = 5

    THRESHOLD = 0.01

    up_PID = PID(0, 0, 0, 0)
    down_PID = PID(0, 0, 0, 0)

    # Drive Constants
    DRIVE_ENCODER_TYPE = ctre.FeedbackDevice.QuadEncoder

    drive_PID = PID(0, 0, 0, 0)

    def setup(self):
        self.lift_encoder = self.lift_motor.getEncoder()
        self.lift_pid_controller = self.lift_motor.getPIDController()

        self.limit_switches = [self.left_limit_switch, self.right_limit_switch]

        self.drive_motor.configSelectedFeedbackSensor(
            self.DRIVE_ENCODER_TYPE, 0, timeoutMs=10
        )
        self.drive_motor.config_kP(0, self.drive_PID.P, timeoutMs=10)
        self.drive_motor.config_kI(0, self.drive_PID.I, timeoutMs=10)
        self.drive_motor.config_kD(0, self.drive_PID.D, timeoutMs=10)
        self.drive_motor.config_kF(0, self.drive_PID.F, timeoutMs=10)

    def on_disable(self):
        self.stop_lift()
        self.stop_wheels()

    def set_pid(self, pid):
        self.lift_pid_controller.setP(pid.P)
        self.lift_pid_controller.setI(pid.I)
        self.lift_pid_controller.setD(pid.D)
        self.lift_pid_controller.setFF(pid.F)

    def set_lift_height(self, lift, set_point_metres):
        if set_point_metres - self.get_lift_height(lift) > 0:
            self.set_pid(lift, self.up_PID)
        else:
            self.set_pid(lift, self.down_PID)

        self.lift_set_point = (
            set_point_metres / self.LIFT_METRES_PER_REV + self.GROUND_OFFSET
        )
        self.lift_motor.lift_pid_controller.setReference(
            self.lift_set_point, rev.ControlType.kPosition
        )

    def get_lift_height(self):
        pos = self.lift_encoder.getPosition()
        return (pos - self.GROUND_OFFSET) * self.LIFT_METRES_PER_REV

    def stop_lift(self):
        self.lift_set_point = None
        self.lift_motor.lift_motor.stopMotor()

    def get_lift_status(self):
        lift_pos = self.get_lift_height()
        return self.is_within_threshold(lift_pos, self.lift_set_point)

    def is_within_threshold(self, pos, goal):
        return (goal + self.THRESHOLD) >= pos >= (goal - self.THRESHOLD)

    def move_wheels_forward(self):
        self.drive_motor.set(ctre.ControlMode.PercentOutput, 0.5)

    def stop_wheels(self):
        self.drive_motor.set(ctre.ControlMode.PercentOutput, 0)

    def is_touching_podium(self, lift):
        return all([switch.get() for switch in self.limit_switches])

    def execute(self):
        pass
