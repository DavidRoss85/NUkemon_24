import math
from random import randint

from src.globals.special_effects import SpecialEffects
from src.globals.UC import UC



class BattleAnimator:
    """
    Object that handles all the animation of effects in the Battle
    Items in the queue are handled one at a time, and player and
    enemy actions are halted while animations are ensue.
    """

    #Constants for tweaking animation timing
    SHAKE_AMT=10
    EXIT_AMT=30
    ATK_AMT=10
    DFND_AMT=20
    DTH_AMT=10
    # SWTCH_STP=20    #Constant for how much out of the screen the __player moves
    INTRO_MOVE_AMT=4

    ATTACK_LENGTH=15
    DEFEND_LENGTH=6
    RECEIVE_DMG_LENGTH=13
    DISCREET_M_LENGTH=20
    SWITCH_LENGTH=20
    KO_LENGTH=20
    PAUSE_LENGTH=30
    SCREEN_TRANSITION_LENGTH=90

    def __init__(self,mixer=None):
        self.__queue=[] #List of all animations to carry out
        self.__object_dictionary=dict()   #Store game objects here to be used in animations
        self.__sounds_dict=dict()   #Dictionary of sounds to play during animations
        self.__animating=False  #Animation status
        self.__tick=0   #Timing variable
        self.__volume=0.7   #Volume of sound

        self.__middle_x=UC.screen_width/2   #Middle of screen x
        self.__middle_y=UC.screen_height/2  #Middle of screen y

        #Stores the original coords of objects that were moved around:
        self.__org_x=0
        self.__org_x2=0
        self.__org_x3=0
        self.__org_y=0
        self.__done_bool=False

        #Dictionaries that tell the object which animation to perform
        self.subject_animation_dictionary=dict()
        self.object_animation_dictionary=dict()
        #Initialize the dictionaries:
        self.initialize_animation_dictionary()

        #initialize sounds
        self.set_sounds_dictionary(UC.animator_sound_dictionary)
        #Sound mixer:
        self.__mixer=mixer

    def set_sounds_dictionary(self,sounds_dict):
        """
        Change sounds
        :param sounds_dict: New dictionary of sounds
        """
        self.__sounds_dict=sounds_dict
    #======================================================================================================
    def initialize_animation_dictionary(self):
        """
        Initialize the animation dictionaries with their related function
        """
        self.subject_animation_dictionary={
            "Attack": self.animate_attack,
            "Defend": self.animate_defend,
            "Switch": self.animate_switch_out,
            "eSwitch": self.animate_switch_in,
            "Discreet Math": self.animate_discreet_math,
            "Growl":self.animate_defend,
            "Algorithms": self.animate_algorithms,
            "KO": self.animate_ko,
            "eKO": self.animate_eko,
            "Die": self.animate_death_1,
            "Intro": self.show_intro,
            "Other":self.animate_defend,
            "Screen_Transition": self.animate_screen_transition
        }

        self.object_animation_dictionary = {
            "Attack": self.animate_receive_damage,
            "Defend": self.animate_defend,
            "Switch": self.animate_switch_in,
            "eSwitch": self.animate_switch_out,
            "Discreet Math": self.animate_confusion,
            "Growl": self.animate_nothing,
            "Algorithms": self.animate_defend,
            "KO": self.animate_switch_in,
            "eKO": self.animate_switch_out,
            "Die": self.animate_death_1,
            "Other": self.animate_defend
        }
    #======================================================================================================
    def set_mixer(self,mixer):
        """
        Changes the sound mixer
        :param mixer: Sound Object
        """
        self.__mixer=mixer
    #======================================================================================================
    def update_object_dictionary(self,item:dict):
        """
        Updates the objects in the dictionary for animations
        :params item: Dictionary with game objects
        """
        self.__object_dictionary.update(item)
    #======================================================================================================
    def get_object_dictionary(self):
        """
        return: Object Dictionary
        """
        return self.__object_dictionary
    #======================================================================================================
    def get_animating_status(self):
        """
        :return: Animating status (True/False)
        """
        return self.__animating
    #======================================================================================================
    def set_animating_status(self,value):
        """
        Set animating status
        """
        self.__animating=value
    #======================================================================================================
    def pause_and_animate(self,animation):
        """
        Adds an animation to the queue and changes animation status
        """
        self.__queue.append(animation)
        self.__animating=True
    #======================================================================================================
    def animate_list(self):
        """
        For each item in the animation queue carry out all actions then remove it from queue
        """

        #If items are in the queue:
        if len(self.__queue)>0:

            #Get the action that is being done:
            action= self.__queue[0]["action"]
            #If the action isn't in the directory, use default action instead:
            if (self.__queue[0]["action"] not in self.subject_animation_dictionary and
                self.__queue[0]["action"] not in self.object_animation_dictionary):
                action="Other"

            #Is subject or object animation?
            #Every action has a reaction. Depending on if it's the subject or the object,
            #the animation will change.
            if "subject" in self.__queue[0]:
                subject=self.__queue[0]["subject"]
                if self.subject_animation_dictionary[action](subject):
                    self.__queue.pop(0)
                    # self.__animating_hp=False

            elif "object" in self.__queue[0]:
                subject=self.__queue[0]["object"]
                if self.object_animation_dictionary[action](subject):
                    self.__queue.pop(0)
                    self.__animating=False
    #======================================================================================================

    #All animations use the 'tick' variable to increment
    def animate_attack(self,subject):
        """
        Animation for attack
        :param subject: The object to perform animation on
        :return: True if animation complete, False if not complete
        """
        self.__animating=True
        if self.__tick<1:
            self.__org_y = subject.get_y()
            self.__mixer.play("swish")

        self.__tick+=1

        if self.__tick<self.ATTACK_LENGTH:
            subject.set_y(subject.get_y() + (math.sin(self.__tick)) * self.ATK_AMT)



        if self.__tick>self.ATTACK_LENGTH+self.PAUSE_LENGTH:
            self.__tick=0
            subject.set_y(self.__org_y)
            return True
        else:
            return False
    #======================================================================================================
    def animate_defend(self, subject):
        """
        Animation for defend
        :param subject: The object to perform animation on
        :return: True if animation complete, False if not complete
        """

        self.__animating = True
        self.__tick += 1
        if self.__tick<self.DEFEND_LENGTH:
            subject.get_sprite().blend_color((self.__tick * self.DFND_AMT, self.__tick * self.DFND_AMT, self.__tick * self.DFND_AMT))
        else:
            subject.get_sprite().restore()

        if self.__tick > self.DEFEND_LENGTH+self.PAUSE_LENGTH:
            self.__tick = 0
            return True
        else:
            return False
    #======================================================================================================
    def animate_receive_damage(self, subject):
        """
        Animation for receiving damage
        :param subject: The object to perform animation on
        :return: True if animation complete, False if not complete
        """

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

        if self.__tick<=self.RECEIVE_DMG_LENGTH:   #Do animation for designated ticks
            if self.__tick % 7 == 0:
                self.__mixer.play("punch")
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


        if self.__tick > self.RECEIVE_DMG_LENGTH+self.PAUSE_LENGTH: #Pause a bit before releasing animation
            self.__tick = 0
            return True
        else:
            return False
    #======================================================================================================
    def animate_switch_out(self,subject):
        """
        Animation for swapping characters
        :param subject: The object to perform animation on
        :return: True if animation complete, False if not complete
        """

        self.__animating = True
        subject.set_visible(True)

        self.__tick += 1
        if self.__tick<=self.SWITCH_LENGTH:
            subject.set_x(subject.get_x() - self.EXIT_AMT)

        if self.__tick > self.SWITCH_LENGTH+self.PAUSE_LENGTH: #Pause a bit before releasing animation
            self.__tick = 0
            subject.unfreeze_frame()
            return True
        else:
            return False
    #======================================================================================================
    def animate_switch_in(self,subject):
        """
        Animation for character switch in
        :param subject: The object to perform animation on
        :return: True if animation complete, False if not complete
        """

        self.__animating = True
        subject.set_visible(True)
        self.__tick += 1
        if self.__tick <= self.SWITCH_LENGTH:
            subject.set_x(subject.get_x() + self.EXIT_AMT)

        if self.__tick > self.SWITCH_LENGTH+self.PAUSE_LENGTH:
            self.__tick = 0
            subject.unfreeze_frame()
            return True
        else:
            return False
    #======================================================================================================
    def animate_death_1(self,subject):
        """
        Animation for death
        :param subject: The object to perform animation on
        :return: True if animation complete, False if not complete
        """

        self.__animating = True
        if self.__tick<1:
            self.__mixer.play("base_boom")

        self.__tick += 1
        if self.__tick < self.KO_LENGTH:
            subject.get_sprite().blend_color(
                (self.__tick * self.DTH_AMT, 0, 0)
            )
        else:
            subject.set_visible(False)

        if self.__tick > self.KO_LENGTH+self.PAUSE_LENGTH:
            self.__tick = 0
            subject.unfreeze_frame()
            return True
        else:
            return False
    #======================================================================================================
    def animate_eko(self,subject):
        """
        Animation for enemy Knock out (Differs from KO since characters slide in from different direction)
        :param subject: The object to perform animation on
        :return: True if animation complete, False if not complete
        """

        self.__animating = True
        if self.__tick<1:
            self.__mixer.play("base_boom")

        self.__tick += 1
        if self.__tick < self.KO_LENGTH:
            self.__object_dictionary["enemy_stat_box"].set_visible(False)
            subject.get_sprite().blend_color(
                (self.__tick * self.DTH_AMT, 0, 0)
            )
        elif self.__tick <= self.KO_LENGTH + self.PAUSE_LENGTH:
            subject.set_visible(False)

        elif self.__tick <= self.KO_LENGTH+ self.PAUSE_LENGTH+self.SWITCH_LENGTH:
            subject.set_x(subject.get_x() + self.EXIT_AMT)

        if self.__tick > self.KO_LENGTH+self.PAUSE_LENGTH+self.SWITCH_LENGTH+self.PAUSE_LENGTH:
            self.__tick = 0
            self.__object_dictionary["enemy_stat_box"].set_visible(True)
            subject.unfreeze_frame()
            return True
        else:
            return False
    #======================================================================================================
    def animate_ko(self, subject):
        """
        Animation for Knock out (Differs from eKO since characters slide in from different direction)
        :param subject: The object to perform animation on
        :return: True if animation complete, False if not complete
        """

        self.__animating = True
        if self.__tick<1:
            self.__mixer.play("base_boom")

        self.__tick += 1
        if self.__tick < self.KO_LENGTH:
            subject.get_sprite().blend_color(
                (self.__tick * self.DTH_AMT, 0, 0)
            )
        elif self.__tick <= self.KO_LENGTH + self.PAUSE_LENGTH:
            subject.set_visible(False)
        elif self.__tick <= self.KO_LENGTH+self.PAUSE_LENGTH + self.SWITCH_LENGTH:
            subject.set_x(subject.get_x() - self.EXIT_AMT)

        if self.__tick > self.KO_LENGTH+self.PAUSE_LENGTH+self.SWITCH_LENGTH+self.PAUSE_LENGTH:
            self.__tick = 0
            subject.unfreeze_frame()
            return True
        else:
            return False
    #======================================================================================================
    def animate_screen_transition(self,subject):
        """
        Animation for the screen transition in the beginning of the battle.
        :param subject: The object to perform animation on
        :return: True if animation complete, False if not complete
        """

        self.__animating=True
        player = self.__object_dictionary["player"]
        enemy = self.__object_dictionary["enemy"]
        background = self.__object_dictionary["background"]
        stats1 = self.__object_dictionary["player_stat_box"]
        stats2 = self.__object_dictionary["enemy_stat_box"]
        h_box = self.__object_dictionary["help_box"]
        a_layer=self.__object_dictionary["animation_layer"]
        effect=subject
        ani_ref="Transition_effect"

        if self.__tick < 1:
            background.set_x(background.get_x()-500)
            player.set_visible(False)
            enemy.set_visible(False)
            stats1.set_visible(False)
            stats2.set_visible(False)
            h_box.set_visible(False)
            a_layer.add_to_queue(ani_ref, effect, 0, 0)

        self.__tick+=1
        effect.set_frame_index((min(self.__tick , effect.get_max_frames()-1)))

        if self.__tick>self.SCREEN_TRANSITION_LENGTH:
            a_layer.remove_from_queue(ani_ref)

        if self.__tick>self.SCREEN_TRANSITION_LENGTH:
            self.__tick=0
            return True
        else:
            return False
    #======================================================================================================
    def show_intro(self,args):
        """
        Animation for characters sliding in the beginning
        :param args: Not used
        :return: True if animation complete, False if not complete
        """

        self.__animating=True
        player=self.__object_dictionary["player"]
        enemy=self.__object_dictionary["enemy"]
        background=self.__object_dictionary["background"]
        stats1=self.__object_dictionary["player_stat_box"]
        stats2=self.__object_dictionary["enemy_stat_box"]
        m_box=self.__object_dictionary["messenger"]
        h_box=self.__object_dictionary["help_box"]

        if self.__tick<1:
            self.__org_x=player.get_x()
            self.__org_x2=enemy.get_x()
            self.__org_x3=background.get_x()
            # background.set_x(background.get_x()-500)
            stats1.set_visible(False)
            stats2.set_visible(False)
            h_box.set_visible(False)
            player.set_x(player.get_x()+500)
            enemy.set_x(enemy.get_x()-500)
            player.set_visible(True)
            enemy.set_visible(True)

        self.__tick+=1

        if self.__tick<125 and player.get_x()>self.__org_x:
            player.set_x(player.get_x()-self.INTRO_MOVE_AMT)
            enemy.set_x(enemy.get_x() + self.INTRO_MOVE_AMT)
            background.set_x(background.get_x()+self.INTRO_MOVE_AMT)
        else:
            if not self.__done_bool:
                m_box.process_message(f"A wild {enemy.get_current_character().get_profession()} appears!\n ")
                self.__done_bool = True

        if self.__tick>175:
            self.__tick=0
            self.__animating=False
            player.set_x(self.__org_x)
            enemy.set_x(self.__org_x2)
            # background.set_x(self.__org_x3)
            stats1.set_visible(True)
            stats2.set_visible(True)
            # h_box.set_visible(True)
            self.__done_bool=False
            return True
        else:
            return False
    #======================================================================================================
    def animate_discreet_math(self,subject):
        """
        Animation for discreet math
        :param subject: The object to perform animation on
        :return: True if animation complete, False if not complete
        """

        self.__animating=True

        a_layer = self.__object_dictionary["animation_layer"]
        effect = SpecialEffects.discreet_math
        ani_ref = f"{subject.get_name()}discreet_math"

        if self.__tick < 1:
            self.__org_x = self.__middle_x-250
            self.__org_y = self.__middle_y-450
            a_layer.add_to_queue(ani_ref, effect, self.__org_x, self.__org_y)

        self.__tick += 1

        effect.set_frame_index(((self.__tick // 5) % effect.get_max_frames()))

        if self.__tick>60:
            a_layer.remove_from_queue(ani_ref)

        if self.__tick>70:
            self.__tick=0
            return True
        else:
            return False

    # ======================================================================================================
    def animate_algorithms(self, subject):
        """
        Animation for discreet math
        :param subject: The object to perform animation on
        :return: True if animation complete, False if not complete
        """

        self.__animating = True

        a_layer = self.__object_dictionary["animation_layer"]
        effect = SpecialEffects.algorithms
        ani_ref = f"{subject.get_name()}discreet_math"

        if self.__tick < 1:
            self.__org_x = self.__middle_x - 250
            self.__org_y = self.__middle_y - 450
            a_layer.add_to_queue(ani_ref, effect, self.__org_x, self.__org_y)

        self.__tick += 1

        effect.set_frame_index(((self.__tick // 5) % effect.get_max_frames()))

        if self.__tick < self.DEFEND_LENGTH:
            subject.get_sprite().blend_color(
                (self.__tick * self.DFND_AMT, self.__tick * self.DFND_AMT, self.__tick * self.DFND_AMT))
        else:
            subject.get_sprite().restore()

        if self.__tick > 60:
            a_layer.remove_from_queue(ani_ref)

        if self.__tick > 70:
            self.__tick = 0
            return True
        else:
            return False

    # ======================================================================================================
    def animate_confusion(self,subject):
        """
        Animation for confusion
        :param subject: The object to perform animation on
        :return: True if animation complete, False if not complete
        """
        #Stub
        return True
    #======================================================================================================

    def animate_nothing(self,subject):
        """
        Just a blank function to do nothing
        :param subject: The object to perform animation on
        :return: True if animation complete, False if not complete
        """

        return True