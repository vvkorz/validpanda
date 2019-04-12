"""
Block
-----

Defines *Block* class of the validpanda package
"""
import collections
import re
from .helpers import Helper


class Block:
    """
    basic building block of a file format. It consists of the HEADER and CONTENT.
    The HEADER specifies columns and their datatypes. Each column can be specified by a few rows

    The CONTENT just contains the actual values.

    An example of a **Block**

    >>>  --> direction of the header_pattern
    >>>  ___________________________________
    >>> |  column_1 |  column_2 |   ...     | HEADER
    >>> |   dtype_1 |   dtype_2 |   ...     |
    >>> |-----------------------------------|
    >>> |           |           |           | CONTENT
    >>> |           |           |           |
    >>> |           |           |           |
    >>> |           |           |           |
    >>> |___________|___________|___________|

    A HEADER can be specified in a dict like so

    >>> from collections import OrderedDict
    >>> block = Block()
    >>> preprocess_function = lambda x: x + 1
    >>> block.columns_names =  OrderedDict([("first_column_name", (preprocess_function, "int64")),
    ...                                     ("second_column_name", (None, "category"))])
    >>> block.content_length = 100

    where integer keys in the first dict specify row number from the top, and dict inside column names and datatype.

    .. note::
       note that a multiple-row header is just a collection of Blocks with no content

    .. note::
       one can define dynamic headers by specifying *header_pattern* variable. A repeating pattern will be then searched
       in horizontal direction from left to right starting from the first column.

    *zero*, *calculated_row_length*, *calculated_col_length* are variables that initially are None, and should be calculated
    for a particular spreadsheet. Zero indicates the exact row and column number where this block starts,
    """

    def __init__(self, columns_names=collections.OrderedDict(), content_length=None):
        self.name = "dummy_block"
        """simple name of this block"""
        self.columns_names = columns_names
        """a dict defining names of columns and their datatype. see a docstring"""
        self.content_length = content_length
        """maximum number of rows (length of the content) if ==0 than there is no length"""
        self.header = True
        """whether keys of the self.columns_names dict should be used or not"""
        self.header_pattern = False
        """specifies whether a header should repeat itself in horizontal direction"""
        self.zero = None
        """very first row, col of this block"""
        self.calculated_row_length = None
        """calculated amount of rows in particular dataframe for this Block instance"""
        self.calculated_col_length = None
        """calculated amount of columns in particular dataframe for this Block instance"""

    def __str__(self):
        return self.name

    @property
    def columns(self):
        """
        Returns the keys of the columns dictionary that corresponds to the
        name of the columns of the db for each header.

        >>> block = Block()
        >>> block.columns_names = collections.OrderedDict([('a', (None, 'A')), ('b', (None, 'B'))])
        >>> block.columns == {'a', 'b'}
        True

        :return: dict_keys
        """
        return self.columns_names.keys()

    def is_valid(self, dataframe):
        """
        core method to validate whether a given dataframe matches this block

        .. warning::
           Important the dataframe is expected with header being the first row

        :param dataframe: pandas dataframe to be validated.
        :return: Boolean
        """
        assert(isinstance(self.columns_names, collections.OrderedDict)), \
            "Block.columns_names must be {}, not {}".format(collections.OrderedDict, type(self.columns_names))
        # first check if there is a pattern in the header
        if self.header:
            # grab the first row for the header
            dataframe_header = tuple(map(lambda c: c.strip(), dataframe.iloc[0]))
            # new df without first row
            dataframe = dataframe.iloc[1:]
            # create dict to be able to look up things later
            dataframe_header_dict = dict(zip(dataframe.columns, dataframe_header))
            if self.header_pattern:
                pattern = tuple(self.columns)
                # look for pattern
                col_length = Helper.find_pattern(dataframe_header, pattern)
                assert(col_length == len(dataframe.columns)), "Block {}, pattern does not fit into the dataframe header".format(self.name)

            else:
                assert(dataframe_header == tuple(self.columns)), \
                    "Block {}. Header column names do not match or are in wrong order.\n\n dataframe header:\n {} \n\n columns:\n{}".format(self.name,
                                                                                                                                            "|".join(dataframe_header),
                                                                                                                                            "|".join(tuple(self.columns)))
        else:
            dataframe_header_dict = dict(zip(dataframe.columns, self.columns_names.keys()))  # map to itself

        for column_indx in dataframe.columns:
            function_to_apply, dtype = self.columns_names[dataframe_header_dict[column_indx]]

            if function_to_apply is not None:
                # TODO use proper indexing. Pandas raises a warning.
                dataframe[column_indx] = dataframe[column_indx].apply(function_to_apply)

            if isinstance(dtype, type(re.compile("([0-9])+"))):
                assert (set(dataframe[column_indx].str.match(dtype)) == {True}), \
                    "one of the values in column {}, does not match the regular expression {} in block {}".format(dataframe_header_dict[column_indx],
                                                                                                                  str(dtype),
                                                                                                                  self.name)
            else:
                try:
                    dataframe[column_indx].astype(dtype, copy=False)
                except ValueError:
                    raise AssertionError("column {} (index={}), can not be converted to type {} in block {}".format(dataframe_header_dict[column_indx],
                                                                                                                    str(column_indx),
                                                                                                                    str(dtype),
                                                                                                                    self.name)

                                         )
        return True


if __name__ == "__main__":
    print("import me")
