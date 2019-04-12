import unittest
from src.validpanda.block import Block
from collections import OrderedDict
import pandas as pd


class TestBlock(unittest.TestCase):
    """
    Tests Block class
    """
    def setUp(self):

        # Blocks definitions
        self.valid_block = Block()
        self.valid_block.columns_names = OrderedDict([("col1", (None, 'int64')),
                                                      ("col2", (None, 'int64')),
                                                      ])
        self.invalid_block = Block()
        self.invalid_block.columns_names = {"col1": (None, 'int64'),
                                            "col2": (None, 'int64')
                                            }

        self.test_data = pd.DataFrame([["col1", "col2"],
                                       [3, 3],
                                       [2, 4],
                                       [4, 5],
                                       [5, 6]
                                       ])

    def test_columns(self):
        self.assertEqual(self.valid_block.columns, {"col1", "col2"})

    def test_invalidity(self):
        """
        test invalid definition of column_names

        :return:
        """
        self.assertRaises(AssertionError, self.invalid_block.is_valid, self.test_data)

    def test_validity(self):
        self.assertTrue(self.valid_block.is_valid(self.test_data))


if __name__ == '__main__':
    unittest.main()
