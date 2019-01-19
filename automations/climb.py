#from components.climb import Climb
from magicbot import StateMachine, state, timed_state

class ClimbAutomation(StateMachine):

    climb: Climb

    def start_match(self):
        self.engage()

#driving off lvl 1
    @timed_state(first=True, must_finish=True, duration=1.0, next_state="both_climbs_down")
    def drive_off(self):
        self.both_motors.move()

#The robot will do it's thing, so the climb module is not needed until...

#going up lvl 3
    @state(must_finish=True)
    def both_lifts_down(self, initial_call):
        if initial_call:
            self.climber.set_lift_height(lift, set_point_metres)
            self.get_lift_height(climber.lifts.front, climber.UP_HEIGHT)
            self.get_lift_height(climber.lifts.back, climber.UP_HEIGHT)
        if self.both_lifts.at_pos():
            self.next_state_now("drive_forward")
    
    @state(must_finish=True)
    def drive_forward(self):
        self.get_lift_status(climber.lifts.front)
        self.climber.move_forward()
        if self.is_touching_podium(climber.lifts.front):
            self.next_state_now("front_lift_up")

    @state(must_finish=True)
    def front_lift_up(self, initial_call):
        if initial_call:
            self.climber.set_lift_height(lift, set_point_metres)
            self.get_lift_height(climber.lifts.front, climber.DOWN_HEIGHT)
        if self.front_lift.at_pos():
            self.next_state_now("going_forward")

    @state(must_finish=True)
    def going_forward(self):
        self.get_lift_status(climber.lifts.back)
        self.climber.move_forward()
        if self.is_touching_podium(climber.lifts.back):
            self.next_state_now("back_lift_up")

    @state(must_finish=True)
    def back_lift_up(self, initial_call):
        if initial_call:
            self.climber.set_lift_height(lift, set_point_metres)
            self.get_lift_height(climber.lifts.back, climber.DOWN_HEIGHT)
        if self.back_lift.at_pos():
            self.next_state_now("finish_pos")

    @state(must_finish=True)
    def finish_pos(self):
        self.climber.move_forward()
        self.done()
