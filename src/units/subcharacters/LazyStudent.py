from src.units.Character import Character


class LazyStudent(Character):
    def __init__(self, name, level, hp, mp, strength, intel, sprite, x=0, y=0):
        super().__init__(name, level, hp, mp, strength, intel, sprite, x, y)
        self.set_profession("Lazy Student")
        self.get_condition().immunities = []
        self.__lazy_move_dict = {
            "Skill": {
                "menu": {
                    "Sleep in Class": {
                        "name": "Sleep in Class", "target": "self", "function": self.sleep_in_class
                    }
                }
            }
        }

        self.update_move_dictionary(self.__lazy_move_dict)

    def sleep_in_class(self,target):
        target.set_curr_hp(target.get_curr_hp()+0)
        return self