from src.org.mugbook.firearm import Firearm, NullFirearm


class Mugbook:
    def __init__(self, initial_directory: str):
        self.initial_directory = initial_directory

    # method to rescan the directory
    def rescan(self):
        pass

    def path_to_firearm(self, path: str) -> Firearm:
        #return Firearm("", "", "", "", False, [], [])
        return NullFirearm()

