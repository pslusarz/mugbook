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
        # Strip the base directory of the mugbook from the path
        path = path.replace(self.initial_directory, '') if self.initial_directory else path

        # Return NullFirearm if "GER" is not in the path
        if "GER" not in path:
            return NullFirearm()

        # Split the remaining path into segments
        segments = path.split('/') if path else []

        # Extract the serial on frame and features from the last segment of the path
        last_segment = segments[-1].split('_') if segments else ["", ""]
        serial_on_frame = last_segment[0]
        features = last_segment[1:]

        # Determine if the firearm is prewar based on the third from last segment of the path
        prewar = "_GER_" not in segments[-3] if len(segments) >= 3 else True

        # Determine the categories based on the type, prewar status, and whether "prealfa" is identified
        categories = ["vis"]
        if not prewar:
            categories.append("german")

        # Identify the alphabet prefix
        alphabet_prefix = "prealfa" if len(segments) >= 2 and "pre-alpha" in segments[-2] else None
        if alphabet_prefix == "prealfa" and not serial_on_frame[0].isdigit():
            return NullFirearm()

        # Return NullFirearm if alphabet prefix cannot be identified
        if not alphabet_prefix:
            return NullFirearm()

        categories.append(alphabet_prefix)

        # Construct the standardized serial and sorted serial
        standardized_serial = f"{alphabet_prefix} {serial_on_frame}"
        sorted_serial = f"0P{serial_on_frame.zfill(5)}"

        # Return a Firearm object with the extracted and constructed properties
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