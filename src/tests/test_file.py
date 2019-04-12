"""
TODO
"""
import unittest
from src.validpanda.block import Block
from src.validpanda.spreadsheet import Spreadsheet
from src.validpanda.file import File
import re
import pandas as pd
from collections import OrderedDict


class TestFile(unittest.TestCase):
    def setUp(self):
        first_block = Block()
        first_block.columns_names = OrderedDict([("col1", (None, 'int64')),
                                                 ("col2", (None, 'int64'))
                                                 ])

        second_block = Block()
        second_block.columns_names = OrderedDict([("col3", (None, 'int64')),
                                                  ("col4", (None, 'int64')),
                                                  ("col5", (None, 'int64'))
                                                  ])
        second_block.content_length = 2

        third_block = Block()
        fapply = lambda x: x.strip("[].")
        third_block.columns_names = OrderedDict([("col6", (fapply, re.compile("([A-Z,0-9])+")))
                                                 ])
        third_block.content_length = 2
        third_block.header_pattern = True

        fourth_block = Block()
        fourth_block.columns_names = OrderedDict([("1", (None, 'int64')),
                                                  ("2", (None, 'int64')),
                                                  ("3", (None, 'int64')),
                                                  ("4", (None, 'int64'))
                                                  ])
        fourth_block.content_length = 2
        fourth_block.header = False

        fifth_block = Block()
        fifth_block.columns_names = OrderedDict([("1", (None, "category"))])

        fifth_block.header = False
        fifth_block.content_length = 2

        six_block = Block()
        six_block.columns_names = OrderedDict([("hed1", (None, "int64")),
                                               ("hed2", (None, "int64")),
                                               ("hed3", (None, "object"))
                                               ])
        six_block.header_pattern = True

        sevens_block = Block()
        sevens_block.columns_names = OrderedDict([("hed4", (None, "int64"))])

        spreadsheet = Spreadsheet()
        spreadsheet.blocks_allocation = {0: {"coordinates": (None, None), "block": first_block},
                                         1: {"coordinates": (None, 0), "block": second_block},
                                         2: {"coordinates": (None, 1), "block": third_block},
                                         3: {"coordinates": (1, 0), "block": fifth_block},
                                         4: {"coordinates": (1, 3), "block": fourth_block},
                                         5: {"coordinates": (0, None), "block": six_block},
                                         6: {"coordinates": (0, 5), "block": sevens_block},
                                         }

        test_data = [["col1", "col2", "col3", "col4", "col5", "col6", "col6"],
                     [3, 3, 5, 5, 6, "[].ERTZ6….", "ERTZ6"],
                     [2, 4, 6, 7, 6, "34RF", "34RF"],
                     [4, 5, "ERT3", 5, 6, 5, 5],
                     [5, 6, "TRZ7", 6, 54, 6, 6],
                     ["hed1", "hed2", "hed3", "hed1", "hed2", "hed3", "hed4"],
                     [5, 6, "TRZ7", 6, 54, 6, 6]
                     ]

        self.file_xlsx = File()
        self.file_xlsx.spreadsheets = {0: {"name": "Sheet1", "spreadsheet": spreadsheet},
                                       1: {"name": "Sheet2", "spreadsheet": spreadsheet}
                                       }
        self.file_xlsx.data = (pd.DataFrame(test_data),)

        self.invalid_file_xlsx = File()
        self.invalid_file_xlsx.spreadsheets = self.file_xlsx.spreadsheets
        self.invalid_file_xlsx.data = [pd.DataFrame(test_data)]

    def test_file_validity(self):
        self.assertTrue(self.file_xlsx.is_valid())

    def test_invalidity(self):
        """
        test invalid definition of data, when not a tuple passed as an object

        :return:
        """
        self.assertRaises(AssertionError, self.invalid_file_xlsx.is_valid)
