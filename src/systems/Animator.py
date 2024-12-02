import math
from random import randint

from src.globals.special_effects import SpecialEffects
from src.graphics.Sprite import Sprite
from src.globals.UC import UC


class Animator:
    SHAKE_AMT=10
    EXIT_AMT=30
    ATK_AMT=10
    DFND_AMT=20
    DTH_AMT=10
    SWTCH_STP=20    #Constant for how much out of the screen the __player moves
    INTRO_MOVE_AMT=4

    def __init__(self):
        self.__queue=[]
        self.__object_dictionary=dict()   #Store game objects here to be used in animations
        self.__animating=False
        self.__tick=0

        self.__middle_x=UC.screen_width/2
        self.__middle_y=UC.screen_height/2

        #Stores the original coords of objects that were moved around:
        self.__org_x=0
        self.__org_x2=0
        self.__org_x3=0
        self.__org_y=0
        self.__done_bool=False


        self.subject_animation_dictionary={
            "Attack": self.animate_attack,
            "Defend": self.animate_defend,
            "Switch": self.animate_switch_out,
            "eSwitch": self.animate_switch_in,
            "Discreet Math": self.animate_discreet_math,
            "KO": self.animate_ko,
            "eKO": self.animate_eko,
            "Die": self.animate_death_1,
            "Intro": self.show_intro
        }

        self.object_animation_dictionary = {
            "Attack": self.animate_receive_damage,
            "Defend": self.animate_defend,
            "Switch": self.animate_switch_in,
            "eSwitch": self.animate_switch_out,
            "Discreet Math": self.animate_confusion,
            "KO": self.animate_switch_in,
            "eKO": self.animate_switch_out,
            "Die": self.animate_death_1
        }

    def update_object_dictionary(self,item:dict):
        self.__object_dictionary.update(item)

    def get_object_dictionary(self):
        return self.__object_dictionary

    def get_animating_status(self):
        return self.__animating

    def set_animating_status(self,value):
        self.__animating=value

    def pause_and_animate(self,animation):
        self.__queue.append(animation)
        self.__animating=True

    def animate_list(self):
        if len(self.__queue)>0:
            # print(self.__queue)
            action=self.__queue[0]["action"]
            if "subject" in self.__queue[0]:
                subject=self.__queue[0]["subject"]
                if self.subject_animation_dictionary[action](subject):
                    self.__queue.pop(0)
                    # self.__animating=False

            elif "object" in self.__queue[0]:
                subject=self.__queue[0]["object"]
                if self.object_animation_dictionary[action](subject):
                    self.__queue.pop(0)
                    self.__animating=False

    def animate_attack(self,subject):
        self.__animating=True
        if self.__tick<1:
            self.__org_y = subject.get_y()

        self.__tick+=1

        subject.set_y(subject.get_y() + (math.sin(self.__tick)) * self.ATK_AMT)


        if self.__tick>20:
            self.__tick=0
            subject.set_y(self.__org_y)
            return True
        else:
            return False

    def animate_defend(self, subject):
        self.__animating = True
        self.__tick += 1
        if self.__tick<6:
            subject.get_sprite().blend_color((self.__tick * self.DFND_AMT, self.__tick * self.DFND_AMT, self.__tick * self.DFND_AMT))
        else:
            subject.get_sprite().restore()

        if self.__tick > 10:
            self.__tick = 0
            return True
        else:
            return False

    def animate_receive_damage(self, subject):
        self.__animating = True
        a_layer = self.__object_dictionary["animation_layer"]
        punches = SpecialEffects.punches
        ani_ref=f"{subject.get_name()}punches"

        if self.__tick<1:
            self.__org_x=subject.get_x()
            self.__org_y=subject.get_y()
            a_layer.add_to_queue(ani_ref, punches,subject.get_x(),subject.get_y())

        self.__tick += 1

        punches.set_frame_index(((self.__tick // 5) % punches.get_max_frames()))

        if self.__tick<=50:   #Do animation for designated ticks
            y_bool=randint(0,1)
            if y_bool:
                subject.set_y(subject.get_y() - self.SHAKE_AMT)
            else:
                subject.set_y(subject.get_y() + self.SHAKE_AMT)

            if self.__tick % 2 == 0:
                subject.set_x(subject.get_x() - self.SHAKE_AMT)
                subject.get_sprite().blend_color((255,0,0))
            else:
                subject.set_x(subject.get_x() + self.SHAKE_AMT)
                subject.get_sprite().blend_color((0, 0, 0))
        else:
            subject.set_x(self.__org_x)
            subject.set_y(self.__org_y)
            subject.get_sprite().restore()
            a_layer.remove_from_queue(ani_ref)


        if self.__tick > 50: #Pause a bit before releasing animation
            self.__tick = 0
            return True
        else:
            return False

    def animate_switch_out(self,subject):
        self.__animating = True
        subject.set_visible(True)

        self.__tick += 1
        if self.__tick<=self.SWTCH_STP:
            subject.set_x(subject.get_x() - self.EXIT_AMT)

        if self.__tick > 20: #Pause a bit before releasing animation
            self.__tick = 0
            subject.unfreeze_frame()
            return True
        else:
            return False

    def animate_switch_in(self,subject):
        self.__animating = True
        subject.set_visible(True)
        self.__tick += 1
        if self.__tick <= self.SWTCH_STP:
            subject.set_x(subject.get_x() + self.EXIT_AMT)

        if self.__tick > 35:
            self.__tick = 0
            subject.unfreeze_frame()
            return True
        else:
            return False

    def animate_death_1(self,subject):
        self.__animating = True
        self.__tick += 1
        if self.__tick < 20:
            subject.get_sprite().blend_color(
                (self.__tick * self.DTH_AMT, 0, 0)
            )
        else:
            subject.set_visible(False)

        if self.__tick > 26:
            self.__tick = 0
            subject.unfreeze_frame()
            return True
        else:
            return False

    def animate_eko(self,subject):
        self.__animating = True
        self.__tick += 1
        if self.__tick < 20:
            self.__object_dictionary["enemy_stat_box"].set_visible(False)
            subject.get_sprite().blend_color(
                (self.__tick * self.DTH_AMT, 0, 0)
            )
        elif self.__tick <= 20 + self.SWTCH_STP:
            subject.set_visible(False)
            subject.set_x(subject.get_x() + self.EXIT_AMT)

        if self.__tick > 45:
            self.__tick = 0
            self.__object_dictionary["enemy_stat_box"].set_visible(True)
            subject.unfreeze_frame()
            return True
        else:
            return False

    def animate_ko(self, subject):
        self.__animating = True
        self.__tick += 1
        if self.__tick < 20:
            subject.get_sprite().blend_color(
                (self.__tick * self.DTH_AMT, 0, 0)
            )
        elif self.__tick <= 20 + self.SWTCH_STP:
            subject.set_visible(False)
            subject.set_x(subject.get_x() - self.EXIT_AMT)

        if self.__tick > 45:
            self.__tick = 0
            subject.unfreeze_frame()
            return True
        else:
            return False

    def show_intro(self,args):
        self.__animating=True
        player=self.__object_dictionary["player"]
        enemy=self.__object_dictionary["enemy"]
        background=self.__object_dictionary["background"]
        stats1=self.__object_dictionary["player_stat_box"]
        stats2=self.__object_dictionary["enemy_stat_box"]
        m_box=self.__object_dictionary["messenger"]

        if self.__tick<1:
            self.__org_x=player.get_x()
            self.__org_x2=enemy.get_x()
            self.__org_x3=background.get_x()
            player.set_x(player.get_x()+500)
            enemy.set_x(enemy.get_x()-500)
            background.set_x(background.get_x()-500)
            stats1.set_visible(False)
            stats2.set_visible(False)

        self.__tick+=1

        if self.__tick<125 and player.get_x()>self.__org_x:
            player.set_x(player.get_x()-self.INTRO_MOVE_AMT)
            enemy.set_x(enemy.get_x() + self.INTRO_MOVE_AMT)
            background.set_x(background.get_x()+self.INTRO_MOVE_AMT)
        else:
            if not self.__done_bool:
                m_box.process_message("A wild professor appears!\n ")
                self.__done_bool = True

        if self.__tick>175:
            self.__tick=0
            self.__animating=False
            player.set_x(self.__org_x)
            enemy.set_x(self.__org_x2)
            background.set_x(self.__org_x3)
            stats1.set_visible(True)
            stats2.set_visible(True)
            self.__done_bool=False
            return True
        else:
            return False

    def animate_discreet_math(self,subject):
        self.__animating=True

        a_layer = self.__object_dictionary["animation_layer"]
        effect = SpecialEffects.discreet_math
        ani_ref = f"{subject.get_name()}discreet_math"

        if self.__tick < 1:
            self.__org_x = self.__middle_x-300
            self.__org_y = self.__middle_y-300
            a_layer.add_to_queue(ani_ref, effect, self.__org_x, self.__org_y)

        self.__tick += 1

        effect.set_frame_index(((self.__tick // 5) % effect.get_max_frames()))

        if self.__tick>40:
            a_layer.remove_from_queue(ani_ref)

        if self.__tick>50:
            self.__tick=0
            return True
        else:
            return False

    def animate_confusion(self,subject):
        return True