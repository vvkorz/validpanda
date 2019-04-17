# validpanda

A python package that helps to validate pandas dataframes.

In general the idea is that every file is a collection of spreadsheets, each of which can be a collection of basic blocks
that in their turn have headers and content under header. We can than construct spreadsheets from this blocks and entire files from spreadsheets.

## Usage

The project is work in progress, so please clone this repository, cd to the root directory and install with 

```
pip install .
```

For more detailed documentation, please see [here](https://validpanda.readthedocs.io/en/latest/)

## Development

### Prerequisites

All dependencies are specified in requirements.txt file.

```
pip install -r requirements.txt
```

### Installing

```
pip install -e.
```

## Running tests

To run tests from the root folder do

```
python -m unittest discover -s src/tests
```

## Versioning

I use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/vvkorz/validpanda/tags).

## Authors

* **Vladimir Korzinov** - *Initial work* - [vvkorz](https://github.com/vvkorz)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
