# Controller

This is the code for sending commands to move the bot over a serial connection (via [pySerial](https://pyserial.readthedocs.io/en/latest/)). Calculates the moves using [BFS](https://en.wikipedia.org/wiki/Breadth-first_search) and a [trie](https://en.wikipedia.org/wiki/Trie) to validate the path.

This code should *theoretically* be cross-platform.

## Usage

Set up vitusl environment with [Poetry](https://python-poetry.org/)

```
poetry install
```

Run code

```
poetry run python -m controller
```
