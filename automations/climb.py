#from components.climb import Climb
from magicbot import StateMachine, state, timed_state

class ClimbAutomation(StateMachine):

    #climb: Climb

    def start_match(self):
        self.engage()

#driving off lvl 1
    @timed_state(first=True, must_finish=True, duration=1.0, next_state="climbs_up")
    def drive_off(self):
        self.motor.move()

#The robot will do it's thing, so the climb module is not needed until...

#going up lvl 3
    @state(must_finish=True)
    def climbs_up(self, initial_call):
        if initial_call:
            self.climbs.move(self.climb.MAX_REST_H)
        if self.climbs.at_pos():
            self.done()

    @timed_state(must_finish=True, duration=0.5, next_state="climb1_down")
    def bit_forward(self):
        self.motor.move()

    @state(must_finish=True)
    def climb1_down(self, initial_call):
        if initial_call:
            self.motor.move()
            self.climb1.move(self.climb.MIN_REST_H)
        if self.climb1.at_pos():
            self.done()

    @timed_state(must_finish=True, duration=0.5, next_state="climb2_down")
    def bit_forward(self):
        self.motor.move()

    @state(must_finish=True)
    def climb2_down(self, initial_call):
        if initial_call:
            self.motor.move()
            self.climb2.move(self.climb.MIN_REST_H)
        if self.climb2.at_pos():
            self.done()

    @state(must_finish=True)
    def finishing_pos(self):
        self.motor.move()