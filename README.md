# PyWiiM

A python interface to control [WiiM](https://www.wiimhome.com/) devices.

## Installation

You can install `pywiim` from [PyPI](https://pypi.org/).

```bash
$ python3 -m pip install pywiim
```

## How to Use

```python
from pywiim import PyWiiM
from pywiim.const import *

host = "192.168.1.123"

pw = PyWiim(host) # Optionally pass an aiohttp session!

pw.close()

```
