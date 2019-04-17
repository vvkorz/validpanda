About
=====

.. warning::
   The following documentation is work in progress.

**validpanda** helps to validate pandas dataframes.

github link is `here <https://github.com/vvkorz/validpanda>`_

In general the idea is that every file is a collection of spreadsheets, each of which can be a collection of basic blocks
that in their turn have headers and content under header. We can than construct spreadsheets from this blocks and entire files from spreadsheets.

The package takes as input a list of pandas dataframes with column dtypes being 'object'. It then splits those dataframes
according to the schema specified in your parser and validates each block. If all blocks and spreadsheets of your file are valid
it returns True.

:Authors:
    Vladimir Korzinov

:Version: |version|

Last updated: |today|