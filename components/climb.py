from dataclasses import dataclass
import rev


class Lifts:
    def __init__(self, front_motor: rev.CANSparkMax, back_motor: rev.CANSparkMax):
        self.front, self.back = [
            {
                "motor": motor,
                "encoder": motor.getEncoder(),
                "pid_controller": motor.getPIDController(),
            }
            for motor in [front_motor, back_motor]
        ]


@dataclass
class PID:
    P: float
    I: float
    D: float
    F: float


class Climber:
    front_lift: rev.CANSparkMax
    back_lift: rev.CANSparkMax

    GROUND_OFFSET = 5  # motor rotations

    # TODO get values
    # heights in metres
    METRES_PER_REV = 0.002

    UP_HEIGHT = 5
    DOWN_HEIGHT = 5

    THRESHOLD = 0.01

    def __init__(self):
        # TODO tune values
        self.up_PID = PID(0, 0, 0, 0)
        self.down_PID = PID(0, 0, 0, 0)

    def setup(self):
        self.lifts = Lifts(self.front_lift, self.back_lift)

    def on_disable(self):
        self.front_lift.stopMotor()
        self.back_lift.stopMotor()

    def set_pid(self, lift, pid):
        lift["pid_controller"].setP(pid.P)
        lift["pid_controller"].setI(pid.I)
        lift["pid_controller"].setD(pid.D)
        lift["pid_controller"].setFF(pid.F)

    def set_lift_height(self, lift, set_point_metres):
        if set_point_metres - self.get_lift_height(lift) > 0:
            self.set_pid(lift, self.up_PID)
        else:
            self.set_pid(lift, self.down_PID)

        set_point = set_point_metres / self.METRES_PER_REV + self.GROUND_OFFSET
        lift["pid_controller"].setReference(set_point, rev.ControlType.kPosition)

    def get_lift_height(self, lift):
        pos = lift["encoder"].getPosition()
        return (pos - self.GROUND_OFFSET) * self.METRES_PER_REV

    def get_lift_status(self, lift, goal):
        value = self.get_lift_height(lift)
        return (goal + self.THRESHOLD) >= value >= (goal - self.THRESHOLD)

    def execute(self):
        pass
