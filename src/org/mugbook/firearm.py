class Firearm:
    def __init__(self, directory, type, serial_on_frame, standardized_serial, sorted_serial, prewar, catalog_category_tree, features):
        self.directory = directory
        self.type = type
        self.serial_on_frame = serial_on_frame
        self.standardized_serial = standardized_serial
        self.sorted_serial = sorted_serial
        self.prewar = prewar
        self.catalog_category_tree = catalog_category_tree
        self.features = features

    def __eq__(self, other):
        if isinstance(other, NullFirearm):
            return True
        else:
            return (self.directory, self.type, self.serial_on_frame, self.standardized_serial, self.sorted_serial, self.prewar, self.catalog_category_tree, self.features) == (other.directory, other.type, other.serial_on_frame, other.standardized_serial, other.sorted_serial, other.prewar, other.catalog_category_tree, other.features)

class NullFirearm(Firearm):
    def __init__(self):
        super().__init__("", "", "", "", "", False, [], [])