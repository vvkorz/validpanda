"""
Spreadsheet
-----------

Defines *Spreadsheet* class of the validpanda package
"""
import pandas as pd
from .helpers import Helper


class Spreadsheet:
    """
    Spreadsheet is a collection of blocks arranged in a particular way. Each block then has *"coordinates"* defined in
    terms of which block precedes this block in direction of rows or columns (please see example below). The coordinates tell where in the spreadsheet a particular
    block is located. Additionally, each block will have an attribute *max_number_of_rows* that specifies its potential length.

    An example of a **Spreadsheet**

    >>>  -----------------------------------
    >>> |                                   |
    >>> |           Block_1                 |
    >>> |                                   |
    >>> |-----------------------------------|
    >>> |           |                       |
    >>> |           |                       |
    >>> |           |        Block_3        |
    >>> |           |                       |
    >>> |  Block_2  |-----------------------|
    >>> |           |                       |
    >>> |           |        Block_3        |
    >>> |           |                       |
    >>> |           |                       |
    >>>  -----------------------------------
    .. note::
       Note that one block can appear multiple times in the same spreadsheet.

    The specification of which block is located where is given by a dictionary of dictionaries.
    For example, for a scheme above the coordinates of block will look the following way:


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

    """

    def __init__(self, blocks_allocation=None):
        if blocks_allocation is None:
            self.name = "dummy_spreadsheet"
            """name of this spreadsheet"""
            self.blocks_allocation = {0: {"coordinates": (None, None), "block": None}}
            """blocks and their coordinates contained in this spreadsheet. see docstring"""
            self.preprocess_func = lambda x: x.reset_index(drop=True)
            """an arbitrary function that preprocesses a dataframe and returns a dataframe"""
        else:
            assert(isinstance(blocks_allocation, dict)), \
                "blocks_allocation must be a dict"
            assert(all(isinstance(n, int) for n in blocks_allocation.keys())), \
                "dict keys must be int"
            assert(all(isinstance(n, dict) for n in blocks_allocation.values())), \
                "dict values must be dictionaries"
            assert(all(set(n.keys()) == ("coordinates", "block") for n in blocks_allocation.values())), \
                "dict keys must be 'coordinates' and 'block'"
            self.blocks_allocation = blocks_allocation
            """blocks and their coordinates contained in this spreadsheet. see docstring"""

    def get_next_blocks(self, block_id):
        """
        get ids of the next blocks in row and col directions.

        :param block_id: id of a block of interest
        :return: next_row_block, next_col_block
        """

        smallest_rowr = 0  # keep in memory the smallest row number
        smallest_col = 0  # keep in memory the smallest column number
        next_col_block = None
        next_row_block = None
        for key, block_data in self.blocks_allocation.items():
            if block_data['coordinates'][0] == block_id:
                if not block_data['coordinates'][1]:
                    smallest_col = block_data['coordinates'][1]
                    next_row_block = block_data['block']
                else:
                    # in case the next row was found already
                    if smallest_col:
                        if block_data['coordinates'][1] <= smallest_col:
                            smallest_col = block_data['coordinates'][1]
                            next_row_block = block_data['block']

            if block_data['coordinates'][1] == block_id:
                if not block_data['coordinates'][0]:
                    smallest_rowr = block_data['coordinates'][0]
                    next_col_block = block_data['block']
                else:
                    # in case the next column was found already
                    if smallest_rowr:
                        if block_data['coordinates'][0] <= smallest_rowr:
                            smallest_rowr = block_data['coordinates'][0]
                            next_col_block = block_data['block']
        return next_row_block, next_col_block

    def get_block_size(self, block_id, dataframe):
        """
        returns the size of the current block in 4 numbers.

         * zero_row - row where the block starts
         * zero_col - column where the block starts
         * row_length - amount of rows
         * col_length - amount of columns

        :param self:
        :param block_id: id of the block
        :param dataframe: todo
        :return:
        """
        block_object = self.blocks_allocation[block_id]['block']
        block_coordinates = self.blocks_allocation[block_id]['coordinates']

        if block_coordinates[0] is not None:
            preceding_block_row = self.blocks_allocation[block_coordinates[0]]['block']
            if preceding_block_row.zero is not None:
                starting_row = preceding_block_row.zero[0] + preceding_block_row.calculated_row_length + 1
            else:
                (starting_row, zero_col), (preceding_row_length, preceding_col_length) = self.get_block_size(block_coordinates[0],
                                                                                         dataframe)
        else:
            starting_row = 0

        if block_coordinates[1] is not None:
            preceding_block_col = self.blocks_allocation[block_coordinates[1]]['block']
            # try to see if previous block in row direction has its size already.
            if preceding_block_col.zero is not None:
                starting_col = preceding_block_col.zero[1] + preceding_block_col.calculated_col_length + 1

            else:
                (zero_row, starting_col), (preceding_row_length, preceding_col_length) = self.get_block_size(block_coordinates[0],
                                                                                         dataframe)
        else:
            starting_col = 0

        # set the beginning of this block
        block_object.zero = tuple([starting_row, starting_col])
        # get the row and column length of this block
        df = dataframe.iloc[starting_row:, starting_col:].reset_index(drop=True)

        next_row_block, next_col_block = self.get_next_blocks(block_id)

        # find row_length
        row_length = 0
        if block_object.content_length:
            row_length = block_object.content_length
        else:
            if next_row_block is None:
                row_length = df.shape[0]
            else:
                if not next_row_block.header:
                    raise ValueError("next block in the row direction must have header")
                else:
                    next_block_header = tuple(next_row_block.columns)

                    for index, row in df.iterrows():
                        # cut the row to the length of the header
                        row = tuple(row[:len(next_block_header)])
                        if row == next_block_header:
                            # I found where next block starts
                            row_length = index - 1
                            break
        # find col_length
        if not block_object.header_pattern:
            # easy case
            col_length = len(block_object.columns) - 1
        else:
            # look where header pattern stops
            this_block_header = tuple(df.iloc[0])
            pattern = tuple(block_object.columns)

            col_length = Helper.find_pattern(this_block_header, pattern) - 1

        block_object.calculated_row_length = row_length
        block_object.calculated_col_length = col_length
        self.blocks_allocation[block_id]['block'] = block_object
        return tuple([tuple([starting_row, starting_col]), tuple([row_length, col_length])])

    def is_valid(self, dataframe):
        """
        core method to validate whether a given dataframe matches this Spreadsheet

        :param dataframe: pandas dataframe to be validated.
        :return: Boolean
        """
        # split the dataframe in blocks
        assert(self.blocks_allocation[0]["coordinates"] == (None, None)), \
            "Error in spreadsheet {}. block with id 0 must have coordinates (None, None)".format(self.name)

        if self.preprocess_func is not None:
            try:
                dataframe = self.preprocess_func(dataframe)
                assert(isinstance(dataframe, pd.DataFrame)), \
                    "The preprocessing function in {} returned {} not a dataframe".format(self.name, type(dataframe))
            except Exception as e:
                raise ValueError("Could not preprocess the dataframe, raised exception:\n {}".format(e))

        # get each block and validate it by
        # iterating over blocks here and recursively check if previous block in row and col direction
        # has its size already calculated or has None in its coordinates, which means first row or col.
        for block_id, block_data in self.blocks_allocation.items():
            (zero_row, zero_col), (row_length, col_length) = self.get_block_size(block_id, dataframe)
            if block_data['block'].header:
                row_correction = 0
            else:
                row_correction = 1
            block_df = dataframe.loc[zero_row: zero_row + row_length - row_correction, zero_col: zero_col + col_length].reset_index(
                drop=True)
            if not block_data['block'].is_valid(block_df):
                return False
        return True


if __name__ == "__main__":
    print("import me!")
