import os

from src.org.mugbook.firearm import Firearm, NullFirearm


class Mugbook:
    def __init__(self, initial_directory: str):
        self.initial_directory = initial_directory
        self.firearms = []

    # method to rescan the directory
    def rescan(self):
        self.firearms.clear()
        for root, dirs, files in os.walk(self.initial_directory):
            for dir in dirs:
                path = os.path.join(root, dir)
                firearm = self.path_to_firearm(path)
                if not isinstance(firearm, NullFirearm):
                    self.firearms.append(firearm)



    def path_to_firearm(self, path: str) -> Firearm:
        path = path.replace(self.initial_directory, '') if self.initial_directory else path

        if ("GER" not in path) or ("PK" in path):
            return NullFirearm()

        segments = path.split('/') if path else []

        last_segment = segments[-1].split('_') if segments else ["", ""]
        serial_on_frame = last_segment[0]
        features = last_segment[1:]

        prewar = "_GER_" not in segments[-3] and "_GER_" not in segments[-4] if len(segments) >= 4 else True

        categories = ["vis"]
        if not prewar:
            categories.append("german")

        alphabet_prefix = None
        if len(segments) >= 3:
            if "__pre-alpha" in segments[-2]:
                alphabet_prefix = "prealfa"
            elif "_1 st alpha_" in segments[-3]:
                alphabet_prefix = "first alfa"
            elif "_2nd alpha_" in segments[-3]:
                alphabet_prefix = "second alfa"

        if ((alphabet_prefix == "prealfa") or (alphabet_prefix == "first alfa") or (alphabet_prefix == "second alfa")) and not serial_on_frame[0].isdigit():
            return NullFirearm()

        if not alphabet_prefix:
            return NullFirearm()

        categories.append(alphabet_prefix)

        standardized_serial = f"{alphabet_prefix} {serial_on_frame}"
        if alphabet_prefix == "prealfa":
            sorted_serial = f"0P{serial_on_frame.zfill(5)}"
        elif alphabet_prefix == "first alfa":
            sorted_serial = f"1A{serial_on_frame.zfill(5)}"
        elif alphabet_prefix == "second alfa":
            # if serial on frame starts with 2k, padd the following digits with up to 4 zeroes
            if serial_on_frame[0] == '2' and serial_on_frame[1] == 'K':
                sorted_serial = f"2A2K{serial_on_frame[2:].zfill(4)}"
            else:
                sorted_serial = f"2A{serial_on_frame.zfill(5)}"

        return Firearm(path, "vis", serial_on_frame, standardized_serial, sorted_serial, prewar, categories, features)

    def pretty_print_firearms(self):
        # Sort firearms by sorted_serial
        self.firearms.sort(key=lambda x: x.sorted_serial)

        # Create a dictionary where the keys are category trees and the values are lists of firearms
        firearms_by_category = {}
        for firearm in self.firearms:
            category_tree = tuple(firearm.catalog_category_tree)
            if category_tree not in firearms_by_category:
                firearms_by_category[category_tree] = []
            firearms_by_category[category_tree].append(firearm)

        # Iterate over the dictionary
        for category_tree, firearms in firearms_by_category.items():
            # Print category tree with indentation
            for i, category in enumerate(category_tree):
                print('  ' * i + category)

            # Print firearms within this category
            for firearm in firearms:
                # Print standardized serial
                print('  ' * len(category_tree) + firearm.standardized_serial + '\tFeatures: ' + ', '.join(firearm.features))