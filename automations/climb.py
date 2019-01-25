from components.climb import Lift
from magicbot import StateMachine, state, timed_state


class ClimbAutomation(StateMachine):

    front_lift: Lift
    back_lift: Lift

    @state(must_finish=True)
    def both_lifts_down(self):
        self.front_lift.extend_lift()
        self.back_lift.extend_lift()
        if (
            self.front_lift.get_lift_at_set_pos()
            and self.back_lift.get_lift_at_set_pos()
        ):
            self.next_state_now("drive_forward")

    @state(must_finish=True)
    def drive_forward(self):
        self.front_lift.move_wheels_forward()
        self.back_lift.move_wheels_forward()

        if self.front_lift.is_touching_podium():
            self.next_state_now("front_lift_up")

    @state(must_finish=True)
    def front_lift_up(self):
        self.front_lift.retract_lift()
        if self.front_lift.get_lift_at_set_pos():
            self.next_state_now("going_forward")

    @state(must_finish=True)
    def going_forward(self):
        self.back_lift.get_lift_at_set_pos()
        self.back_lift.move_wheels_forward()
        if self.back_lift.is_touching_podium():
            self.next_state_now("back_lift_up")

    @state(must_finish=True)
    def back_lift_up(self):
        self.back_lift.retract_lift()
        if self.back_lift.get_lift_at_set_pos():
            self.done()
