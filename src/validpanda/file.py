"""
File
----

Defines *File* class of the validpanda package
"""
import pandas as pd


class File:
    """
    File is a collection of spreadsheets.

    Here is a bad attempt to visualise a **File** class

    >>>          ----------------------------------
    >>>        /                                   / |
    >>>       /                                   /  |
    >>>      /                                   /   |
    >>>     /                                   /    |
    >>>    /                                   /     |
    >>>   /                                   /      |
    >>>  ----------------------------------- /       |
    >>> |                                   |        |
    >>> |           Block_1                 |        |
    >>> |                                   |        |
    >>> |-----------------------------------|        |
    >>> |           |                       |        |
    >>> |           |                       |       /
    >>> |           |        Block_3        |      /
    >>> |           |                       |     / Spreadsheets
    >>> |  Block_2  |-----------------------|    /
    >>> |           |                       |   /
    >>> |           |        Block_3        |  /
    >>> |           |                       | /
    >>> |           |                       |/
    >>>  -----------------------------------


    Here is an example of the definition of all elements needed to create a File

    >>> from collections import OrderedDict
    >>> block = Block()
    >>> preprocess_function = lambda x: x + 1
    >>> block.columns_names =  OrderedDict([("first_column_name", (preprocess_function, "int64")),
    ...                                     ("second_column_name", (None, "category"))])
    >>> block.content_length = 100
    >>> second_block = Block()
    >>> block.columns_names =  OrderedDict([("first_column_name", (None, "datetime64")),
    ...                                     ("second_column_name", (None, "category"))])
    >>> second_block.content_length = None
    >>> third_block = Block()
    >>> block.columns_names =  OrderedDict([("first_column_name", (None, "datetime64")),
    ...                                     ("second_column_name", (None, "category")),
    ...                                     ("third_column_name", (None, "bool"))])
    >>> third_block.content_length = 100
    >>> spreadsheet = Spreadsheet()
    >>> spreadsheet.blocks_allocation = {0: {"coordinates": (None, None), "block": first_block},
    ...                                  1: {"coordinates": (0, None), "block": second_block},
    ...                                  2: {"coordinates": (0, 1), "block": third_block},
    ...                                  3: {"coordinates": (2, 1), "block": third_block},
    ...                                  }
    >>> second_spreadsheet = Spreadsheet()
    >>> second_spreadsheet.blocks_allocation = {0: {"coordinates": (None,None), "block": second_block},
    ...                                         1: {"coordinates": (0,None), "block": third_block},
    ...                                         2: {"coordinates": (0,1), "block": third_block},
    ...                                         3: {"coordinates": (2,1), "block": first_block},
    ...                                         }
    >>> file = File()
    >>> file.spreadsheets = {0: {"name": "Spreadsheet name", "spreadsheet": first_spreadsheet},
    ...                      1: {"name": "Spreadsheet name", "spreadsheet": second_spreadsheet}
    ...                      }
    >>>
    """

    def __init__(self, spreadsheets=None):
        if spreadsheets is None:
            self.spreadsheets = dict(dict())
        else:
            self.spreadsheets = spreadsheets
        """ids, names and classes of spreadsheets in this file"""

        self.data = tuple()
        """a list or tuple with dataframes to be validated"""

    def is_valid(self):
        """
        core method to validate whether a given file matches this class definition.

        :return: Boolean
        """
        assert(isinstance(self.data, tuple)), "File class only accepts tuples of dataframes, not {}".format(type(self.data))
        for indx, dataframe in enumerate(self.data):
            assert(isinstance(dataframe, pd.DataFrame)), "{} entry in data tuple is not a dataframe, but {}".format(indx, type(dataframe))
            if not self.spreadsheets[indx]["spreadsheet"].is_valid(dataframe):
                return False
        return True


if __name__ == "__main__":
    print("import me!")
