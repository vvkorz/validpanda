from validpanda.block import Block
from validpanda.spreadsheet import Spreadsheet
from validpanda.file import File


class BaseParser:
    """
    basic abstract file parser. The example below shows how such a parser can be used.

    The Blocks, Spreadsheets and Files for a specific parser can be defined as follows:

    >>> from collections import OrderedDict
    >>> from validpanda.parsers import BaseParser
    >>> class ExampleParser(BaseParser):
    >>>     blocks = {"block0": {"columns_names": OrderedDict([("1", (lambda x: x.strip(), 'category')),
    ...                                                        ("2", (None, 'category')),
    ...                                                        ]),
    ...                          "header": False,
    ...                          "content_length": 5,
    ...                          "header_pattern": False,
    ...                          },
    ...               "block1": {"columns_names": OrderedDict([("Overall Result", (None, re.compile("([A-Z,0-9])+"))),
    ...                                                        ("", 'category'),
    ...                                                        ]),
    ...                          "header": True,
    ...                          "content_length": None,
    ...                          "header_pattern": False,
    ...                          },
    ...               "block2": {"columns_names": OrderedDict([("Total LC", (None, 'category')),
    ...                                                        ("Total GC", (None, 'category')),
    ...                                                        ]),
    ...                          "header": True,
    ...                          "content_length": 2,
    ...                          "header_pattern": True,
    ...                          },
    ...               "block3": {"columns_names": OrderedDict([("Total LC", (None, 'category')),
    ...                                                        ("Total GC", (None, 'category')),
    ...                                                        ]),
    ...                          "header": True,
    ...                          "content_length": 1,
    ...                          "header_pattern": True,
    ...                          },
    ...               "block4": {"columns_names": OrderedDict([("Total LC", (None, 'int64')),
    ...                                                        ("Total GC", (None, 'int64')),
    ...                                                        ]),
    ...                          "header": True,
    ...                          "content_length": None,
    ...                          "header_pattern": True,
    ...                          },
    ...
    ...               }
    >>>     spreadsheets = {"spreadsheet0": {"blocks_allocation": {0: {"coordinates": (None, None), "block": "block0"},
    ...                                                            1: {"coordinates": (0, None), "block": "block1"},
    ...                                                            2: {"coordinates": (None, 0), "block": "block2"},
    ...                                                            3: {"coordinates": (2, 0), "block": "block3"},
    ...                                                            4: {"coordinates": (3, 0), "block": "block4"},
    ...                                                            },
    ...                                      "preprocess_func": lambda x: x.reset_index(drop=True)
    ...                                      },
    ...                     }
    >>>     file = {"spreadsheets": {0: {"name": "Sheet1", "spreadsheet": "spreadsheet0"},
    ...                              }
    ...             }
    >>>     def __init__(self, **kwargs):
    ...         super().__init__(**kwargs)
    ...         self.initialise(ExampleParser.blocks,
    ...                         ExampleParser.spreadsheets,
    ...                         ExampleParser.file)
    """

    def __init__(self, file_path=None, file_name=None):
        self.file_path = file_path
        """path to the file to parse"""
        self.file_name = file_name
        """default name of the file"""
        self.file = File()
        """file object that will be used for validation"""

    def initialise(self, blocks, spreadsheets, file):
        """
        use this method in your parser. It constructs Blocks, Spreadsheets and File objects from the predefined structure.

        Please see the documentation above how one could possibly define such a structure

        :return: None
        """
        spreadsheet_allocation = file["spreadsheet_allocation"]

        for spreadsheet, svalue in file["spreadsheet_allocation"].items():

            blocks_allocation = spreadsheets[svalue["spreadsheet"]]["blocks_allocation"]

            for block, bvalue in spreadsheets[svalue["spreadsheet"]]["blocks_allocation"].items():
                block_ = Block()
                block_.name = block
                block_.columns_names = blocks[bvalue["block"]]["columns_names"]
                block_.header = blocks[bvalue["block"]]["header"]
                block_.content_length = blocks[bvalue["block"]]["content_length"]
                block_.header_pattern = blocks[bvalue["block"]]["header_pattern"]

                blocks_allocation[block]["block"] = block_

            spreadsheet_ = Spreadsheet()
            spreadsheet_.blocks_allocation = blocks_allocation
            spreadsheet_.preprocess_func = spreadsheets[svalue["spreadsheet"]]["preprocess_func"]

            spreadsheet_allocation[spreadsheet]["spreadsheet"] = spreadsheet_

        self.file.spreadsheets = spreadsheet_allocation
        self.file.extension = file["extension"]
