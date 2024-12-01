import math


class Animator:
    SHAKE_AMT=10
    EXIT_AMT=30
    ATK_AMT=10
    DFND_AMT=20
    DTH_AMT=10
    def __init__(self):
        self.queue=[]
        self.animating=False
        self.tick=0

        self.subject_animation_dictionary={
            "Attack": self.animate_attack,
            "Defend": self.animate_defend,
            "Switch": self.animate_switch_out,
            "eSwitch": self.animate_switch_in,
            "KO": self.animate_ko,
            "eKO": self.animate_eko,
            "Die": self.animate_death_1
        }

        self.object_animation_dictionary = {
            "Attack": self.animate_receive_damage,
            "Defend": self.animate_defend,
            "Switch": self.animate_switch_in,
            "eSwitch": self.animate_switch_out,
            "KO": self.animate_switch_in,
            "eKO": self.animate_switch_out,
            "Die": self.animate_death_1
        }


    def get_animating_status(self):
        return self.animating

    def set_animating_status(self,value):
        self.animating=value

    def pause_and_animate(self,animation):
        self.queue.append(animation)
        self.animating=True

    def animate_list(self):
        if len(self.queue)>0:
            # print(self.queue)
            action=self.queue[0]["action"]
            if "subject" in self.queue[0]:
                subject=self.queue[0]["subject"]
                if self.subject_animation_dictionary[action](subject):
                    self.queue.pop(0)
                    # self.animating=False

            elif "object" in self.queue[0]:
                subject=self.queue[0]["object"]
                if self.object_animation_dictionary[action](subject):
                    self.queue.pop(0)
                    self.animating=False

    def animate_attack(self,subject):
        self.animating=True
        self.tick+=1

        subject.set_y(subject.get_y()+(math.sin(self.tick))*self.ATK_AMT)
        # if self.tick%2==0:
        #     subject.set_x(subject.get_x()-self.SHAKE_AMT)
        # else:
        #     subject.set_x(subject.get_x() + self.SHAKE_AMT)

        if self.tick>20:
            self.tick=0
            return True
        else:
            return False

    def animate_defend(self, subject):
        self.animating = True
        self.tick += 1
        if self.tick<6:
            subject.get_sprite().blend_color((self.tick*self.DFND_AMT,self.tick*self.DFND_AMT,self.tick*self.DFND_AMT))
        else:
            subject.get_sprite().restore()

        if self.tick > 10:
            self.tick = 0
            return True
        else:
            return False

    def animate_receive_damage(self, subject):
        self.animating = True
        self.tick += 1
        if self.tick<=20:   #Do animation for designated ticks
            if self.tick % 2 == 0:
                subject.set_x(subject.get_x() - self.SHAKE_AMT)
            else:
                subject.set_x(subject.get_x() + self.SHAKE_AMT)

        if self.tick > 50: #Pause a bit before releasing animation
            self.tick = 0
            return True
        else:
            return False

    def animate_switch_out(self,subject):
        self.animating = True
        subject.set_visible(True)

        self.tick += 1
        if self.tick<=20:
            subject.set_x(subject.get_x() - self.EXIT_AMT)

        if self.tick > 20: #Pause a bit before releasing animation
            self.tick = 0
            subject.unfreeze_frame()
            return True
        else:
            return False

    def animate_switch_in(self,subject):
        self.animating = True
        subject.set_visible(True)
        self.tick += 1
        if self.tick <= 20:
            subject.set_x(subject.get_x() + self.EXIT_AMT)

        if self.tick > 35:
            self.tick = 0
            subject.unfreeze_frame()
            return True
        else:
            return False

    def animate_death_1(self,subject):
        self.animating = True
        self.tick += 1
        if self.tick < 20:
            subject.get_sprite().blend_color(
                (self.tick * self.DTH_AMT, 0, 0)
            )
        else:
            subject.set_visible(False)

        if self.tick > 26:
            self.tick = 0
            subject.unfreeze_frame()
            return True
        else:
            return False

    def animate_eko(self,subject):
        self.animating = True
        self.tick += 1
        if self.tick < 20:
            subject.get_sprite().blend_color(
                (self.tick * self.DTH_AMT, 0, 0)
            )
        elif self.tick < 40:
            subject.set_visible(False)
            subject.set_x(subject.get_x() + self.EXIT_AMT)

        if self.tick > 45:
            self.tick = 0
            subject.unfreeze_frame()
            return True
        else:
            return False

    def animate_ko(self, subject):
        self.animating = True
        self.tick += 1
        if self.tick < 20:
            subject.get_sprite().blend_color(
                (self.tick * self.DTH_AMT, 0, 0)
            )
        elif self.tick < 40:
            subject.set_visible(False)
            subject.set_x(subject.get_x() - self.EXIT_AMT)

        if self.tick > 45:
            self.tick = 0
            subject.unfreeze_frame()
            return True
        else:
            return False