import unittest

from src.org.mugbook.firearm import NullFirearm
from src.org.mugbook.mugbook import Mugbook


class MugbookTest(unittest.TestCase):
    mugbook = Mugbook("/Users/paulslusarz/Documents/radoms/mugbook2024/__POLSKIE_VIS35")
    def test_null_for_anything_not_recognized(self):

        result = self.mugbook.path_to_firearm("some/path")
        self.assertEqual(NullFirearm(), result)  # add assertion here

    def test_prealfa(self):
        firearm = self.mugbook.path_to_firearm("/Users/paulslusarz/Documents/radoms/mugbook2024/__POLSKIE_VIS35/000_GER____5609/__pre-alpha____282/5_no legend_bbl white")
        # check all properties of the firearm
        self.assertEqual("/000_GER____5609/__pre-alpha____282/5_no legend_bbl white", firearm.directory)
        self.assertEqual("vis", firearm.type)
        self.assertEqual("5", firearm.serial_on_frame)
        self.assertEqual("prealfa 5", firearm.standardized_serial)
        self.assertEqual("0P00005", firearm.sorted_serial)
        self.assertEqual(False, firearm.prewar)
        self.assertEqual(["vis","german", "prealfa"], firearm.catalog_category_tree)
        self.assertEqual(["no legend", "bbl white"], firearm.features)

    def test_rescan_prealfas(self):
        self.mugbook.rescan()
        self.mugbook.pretty_print_firearms()
        # sort firearms on sorted_serial
        sorted_fireamrs = self.mugbook.firearms.sort(key=lambda x: x.sorted_serial)

        self.assertEqual(282, len(self.mugbook.firearms))
        # first should have serial on frame 5, last 11151
        self.assertEqual("5", sorted_fireamrs[0].serial_on_frame)
        self.assertEqual("11151", sorted_fireamrs[-1].serial_on_frame)



if __name__ == '__main__':
    unittest.main()
