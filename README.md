# strpdatetime

A replacement for `datetime.datetime.strptime` with super powers. `strpdatetime` is a drop-in replacement for `datetime.datetime.strptime` that adds a simplified regex-like syntax for finding and extracting date and time information from strings.

## Why this package?

A common use case is parsing date/time information from strings, for example filenames with
the date and time embedded in them. The standard library's `datetime.datetime.strptime` works
well if the string perfectly matches the format string, but does not work if the string
contains additional characters. For example, `datetime.datetime.strptime("IMG_1234_2022_11_20.jpeg", "%Y_%m_%d")` will fail with `ValueError: time data 'IMG_1234_2022_11_20.jpeg' does not match format '%Y_%m_%d'`. To use `datetime.datetime.strptime` in this case, you would need to first parse the string to remove the extra characters.

Third-party packages such as [dateutil](https://github.com/dateutil/dateutil) and [datefinder](https://github.com/akoumjian/datefinder) are more flexible but still fail to find the date in the above example and other common filename date/time formats.

`strpdatetime` can find the date in the above example using `strpdatetime("IMG_1234_2022_11_20.jpeg", "^IMG_*_%Y_%m_%d")`

## Installation

`pip install strpdatetime`

To install from source, clone the repository, `pip install poetry`, and run `poetry install`.

## Source Code

The source code is available on [GitHub](https://github.com/RhetTbull/strpdatetime).

## Usage

```pycon
>>> import datetime
>>> from strpdatetime import strpdatetime
>>> dt = strpdatetime("IMG_1234_2022_11_20.jpeg","^IMG_*_%Y_%m_%d.*")
>>> assert dt == datetime.datetime(2022,11,20)
>>>
```

## Syntax

In addition to the standard `strptime` [format codes](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes), `strpdatetime` supports the following:

- *: Match any number of characters
- ^: Match the beginning of the string
- $: Match the end of the string
- {n}: Match exactly n characters
- {n,}: Match at least n characters
- {n,m}: Match at least n characters and at most m characters
- In addition to `%%` for a literal `%`, the following format codes are supported:
    `%^`, `%$`, `%*`, `%|`, `%{`, `%}` for `^`, `$`, `*`, `|`, `{`, `}` respectively
- |: join multiple format codes; each code is tried in order until one matches
- Unlike the standard library, the leading zero is not optional for %d, %m, %H, %I, %M, %S, %j, %U, %W, and %V
- For optional leading zero, use %-d, %-m, %-H, %-I, %-M, %-S, %-j, %-U, %-W, and %-V

## Examples

```pycon
>>> from strpdatetime import strpdatetime
>>> strpdatetime("IMG_1234_2022_11_20.jpg","^IMG_{4}_%Y_%m_%d")
datetime.datetime(2022, 11, 20, 0, 0)
>>> strpdatetime("IMG_1234_2022_11_20.jpg","IMG_*_%Y_%m_%d")
datetime.datetime(2022, 11, 20, 0, 0)
>>> strpdatetime("1234_05_06_2022_11_20","%Y_%m_%d$")
datetime.datetime(2022, 11, 20, 0, 0)
>>> strpdatetime("1234_05_06_2022_11_20","IMG_*_%Y_%m_%d|%Y_%m_%d$")
datetime.datetime(2022, 11, 20, 0, 0)
>>>
```

## Command Line

`strpdatetime` includes a very simple command line interface. It can be used to test the regex-like syntax.

```bash
$ python -m strpdatetime "IMG_*_%Y_%m_%d" *.jpg
IMG_2131_2022_11_20.jpg: 2022-11-20 00:00:00
IMG_2132.jpg: time data 'IMG_2132.jpg' does not match format 'IMG_*_%Y_%m_%d'
IMG_2134_2022_11_20.jpg: 2022-11-20 00:00:00
```

## License

To ensure backwards compatibility with the Python standard library, `strpdatetime` makes use of original code from the standard library and is thus licensed under the Python Software Foundation License, just as Python itself is.

## Contributing

Contributions of all kinds are welcome! Please open an issue or pull request on [GitHub](https://github.com/RhetTbull/strpdatetime).
