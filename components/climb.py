import SparkMax
from dataclasses import dataclass


class Climber:
    @dataclass
    class Lifts:
        front: SparkMax
        back: SparkMax

    front_lift: SparkMax
    back_lift: SparkMax

    ENCODER_TYPE = SparkMax.ENCODER_TYPE
    COUNTS_PER_REV = int
    METRES_PER_REV = 0.005

    UP_HEIGHT = int
    DOWN_HEIGHT = int

    THRESHOLD = 0.01

    def __init__(self):
        self.lifts = self.lifts(self.front_lift, self.back_lift)

    def set_lift_height(self, lift, pos):
        set_point = pos / self.METRES_PER_REV * self.COUNTS_PER_REV
        lift.set(set_point)

    def get_lift_height(self, lift):
        pos = lift.get_pos()
        return pos / self.COUNTS_PER_REV * self.METRES_PER_REV

    def within_threshold(self, value, goal):
        return (goal + self.THRESHOLD) >= value >= (goal - self.THRESHOLD)

    def both_legs_down(self):
        self.set_lift_height(self.lifts.front, self.DOWN_HEIGHT)
        self.set_lift_height(self.lifts.back, self.DOWN_HEIGHT)

    def both_legs_down_status(self):
        front = self.within_threshold(
            self.get_lift_height(self.lifts.front), self.DOWN_HEIGHT
        )
        back = self.within_threshold(
            self.get_lift_height(self.lifts.back), self.DOWN_HEIGHT
        )

        return front and back
