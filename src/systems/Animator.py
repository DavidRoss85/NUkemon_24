class Animator:
    SHAKE_AMT=10
    EXIT_AMT=30
    def __init__(self):
        self.queue=[]
        self.animating=False
        self.tick=0

        self.subject_animation_dictionary={
            "Attack": self.animate_attack,
            "Defend": self.animate_defend,
            "Switch": self.animate_switch_out
        }

        self.object_animation_dictionary = {
            "Attack": self.animate_receive_damage,
            "Defend": self.animate_defend,
            "Switch": self.animate_switch_in,
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
                    self.animating=False

            elif "object" in self.queue[0]:
                subject=self.queue[0]["object"]
                if self.object_animation_dictionary[action](subject):
                    self.queue.pop(0)
                    self.animating=False

    def animate_attack(self,subject):
        self.animating=True
        self.tick+=1
        if self.tick%2==0:
            subject.set_x(subject.get_x()-self.SHAKE_AMT)
        else:
            subject.set_x(subject.get_x() + self.SHAKE_AMT)

        if self.tick>20:
            self.tick=0
            return True
        else:
            return False

    def animate_defend(self, subject):
        self.animating = True
        self.tick += 1
        if self.tick % 2 == 0:
            subject.set_x(subject.get_x() - self.SHAKE_AMT)
        else:
            subject.set_x(subject.get_x() + self.SHAKE_AMT)

        if self.tick > 20:
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
        subject.freeze_frame=True
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
        self.tick += 1
        if self.tick <= 20:
            subject.set_x(subject.get_x() + self.EXIT_AMT)

        if self.tick > 50:
            self.tick = 0
            return True
        else:
            return False