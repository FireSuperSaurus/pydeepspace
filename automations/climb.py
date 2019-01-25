from components.climb import Lift
from magicbot import StateMachine, state, timed_state


class ClimbAutomation(StateMachine):

    front_lift: Lift
    back_lift: Lift

    def start_match(self):
        self.engage()

    # driving off lvl 1
    @timed_state(
        first=True, must_finish=True, duration=1.0, next_state="both_lifts_down"
    )
    def drive_off(self):
        self.move_wheels_forward()

    # The robot will do it's thing, so the climb module is not needed until...

    # going up lvl 3
    @state(must_finish=True)
    def both_lifts_down(self):
        self.front_lift.extend_lift()
        self.back_lift.extend_lift()
        if self.front_lift.get_lift_status() and self.back_lift.get_lift_status():
            self.next_state_now("drive_forward")

    @state(must_finish=True)
    def drive_forward(self):
        self.front_lift.get_lift_status()
        self.move_wheels_forward()
        if self.front_lift.is_touching_podium():
            self.next_state_now("front_lift_up")

    @state(must_finish=True)
    def front_lift_up(self):
        self.front_lift.retract_lift()
        if self.front_lift.get_lift_status():
            self.next_state_now("going_forward")

    @state(must_finish=True)
    def going_forward(self):
        self.back_lift.get_lift_status()
        self.move_wheels_forward()
        if self.back_lift.is_touching_podium():
            self.next_state_now("back_lift_up")

    @state(must_finish=True)
    def back_lift_up(self):
        self.back_lift.retract_lift()
        if self.back_lift.get_lift_status():
            self.next_state_now("finish_pos")

    @state(must_finish=True)
    def finish_pos(self):
        self.move_wheels_forward()
        self.stop_wheels()
        self.done()
