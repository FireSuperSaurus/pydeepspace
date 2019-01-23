#from components.climb import Climb
from magicbot import StateMachine, state, timed_state

class ClimbAutomation(StateMachine):

    climb: Climb

    def start_match(self):
        self.engage()

#driving off lvl 1
    @timed_state(first=True, must_finish=True, duration=1.0, next_state="both_climbs_up")
    def drive_off(self):
        self.both_motors.move()

#The robot will do it's thing, so the climb module is not needed until...

#going up lvl 3
    @state(must_finish=True)
    def both_climbs_up(self, initial_call):
        if initial_call:
            self.both_climbs.move(self.climb.MAX_REST_H)
        if self.both_climbs.at_pos():
            self.next_state_now("drive_forward")
    
    @timed_state(must_finish=True, duration=0.5, next_state="front_climb_down")
    def drive_forward(self):
        self.both_motors.move()

    @state(must_finish=True)
    def front_climb_down(self, initial_call):
        if initial_call:
            self.both_motors.move()
            self.front_climb.move(self.climb.MIN_REST_H)
        if self.front_climb.at_pos():
            self.next_state_now("going_forward")

    @timed_state(must_finish=True, duration=0.5, next_state="back_climb_down")
    def going_forward(self):
        self.both_motors.move()

    @state(must_finish=True)
    def back_climb_down(self, initial_call):
        if initial_call:
            self.both_motors.move()
            self.back_climb.move(self.climb.MIN_REST_H)
        if self.back_climb.at_pos():
            self.next_state_now("finish_pos")

    @state(must_finish=True)
    def finish_pos(self):
        self.both_motors.move(0.2)
        self.done()