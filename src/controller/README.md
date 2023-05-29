# Controller

This is the code for sending commands to move the bot over a serial connection (via [pySerial](https://pyserial.readthedocs.io/en/latest/)). Calculates the moves using [BFS](https://en.wikipedia.org/wiki/Breadth-first_search) and a [trie](https://en.wikipedia.org/wiki/Trie) to validate the path.

This code should *theoretically* be ~~cross-platform~~ runnable on all Linux/Mac platforms. You may need to modify [this](https://github.com/ThatXliner/FADAIG/blob/2a3d672dbd43a54c94660e576eb2e343c46ba226/src/controller/controller/__init__.py#L8)

## Usage

Set up virtual environment with [Poetry](https://python-poetry.org/)

```
poetry install
```

Run code

```
poetry run python -m controller
```
