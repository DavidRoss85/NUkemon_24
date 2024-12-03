from src.units.Character import Character


class Husky(Character):
    def __init__(self,name,level,hp,mp,strength,intel,sprite,x=0,y=0):
        super().__init__(name,level,hp,mp,strength,intel,sprite,x,y)
        self.set_profession("Husky")
        self.get_condition().immunities={"confused":True}
        self.__husky_move_dict={
            "Skill":{
                "menu":{
                    "Growl": {
                        "name": "Growl", "target": "enemies", "function":self.stub_func
                    }
                }
            }
        }

        self.update_move_dictionary(self.__husky_move_dict)




    def stub_func(self):
        pass