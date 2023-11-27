# pywiim

Python interface for the [WiiM](https://www.wiimhome.com/) device API.

## Ruminations

This package was born out of a desire to integrate a WiiM Pro streamer with 
Home Assistant. Part of the integration required some sort of library to 
perform the API calls, which is where pywiim came in.

WiiM provides a fairly straightforward API for interacting with their 
streamers (as far as I know they all utilize the same API).

[You can find this API on WiiM's website.](https://www.wiimhome.com/pdf/HTTP%20API%20for%20WiiM%20Mini.pdf)

## Installation

(WIP) You can install `pywiim` from [PyPI](https://test.pypi.org/project/pywiim/).

```bash
$ python3 -m pip install pywiim
```

## Implementation Notes

As you will notice from using the `PyWiim` class, the main methods available are
designed to be used asynchronously. This was chosen to align best with Home 
Assistant's asynchronous functionality.

You also might notice that `verify_ssl` is set to `False` for the actual GET 
requests. This is required due to the API implementation from WiiM.

## Supported Commands

Below is a table of the currently supported commands in `pywiim`. Please read 
the method docstrings for expected arguments and nuances.

| Command | Description |
| --- | --- |
| `get_device_information` | Get the device information |
| `get_connection_status` | Get the Wi-Fi connection status |
| `get_playback_status` | Get the current playback status |
| `get_eq_presets` | Get a list of EQ presets available |
| `get_shutdown_timer` | Get time to shutdown (in seconds) |
| - | - |
| `pause` | Pause playback |
| `play` | Resume playback |
| `toggle` | Toggle playback state |
| `previous` | Skip to previous track |
| `next` | Skip to next track |
| `seek` | Seek a provided number of seconds |
| `stop` | Stop playback |
| `set_volume` | Set volume level |
| `mute` | Mute playback |
| `unmute` | Unmute playback |
| `set_loopmode` | Set looping mode (shuffle, loop once, loop all) |
| `enable_eq` | Enable equalizer |
| `disable_eq` | Disable equalizer |
| `load_eq` | Load an equalizer preset (`get_eq_presets` output) |
| `reboot` | Reboot device |
| `schedule_shutdown` | Schedule device shutdown |
| `set_source` | Set playback source (line-in, bluetooth, etc) |
| `play_audio_url` | Play an audio stream via URL |
| - | - |
| `set_volume_relative` | Set volume level relative to current level |

## Example Usage

```python
import asyncio
from pywiim import PyWiim
from pywiim.const import *

async def main():
    # Get an instance of the class (provide the WiiM IP address)
    p = PyWiim("192.168.1.123")

    # Doing some funky stuff to call async functions
    results = await asyncio.gather(
        p.get_device_information(),
        p.get_connection_status(),
        p.get_playback_status(),
        p.mute(),
        p.set_loopmode(PYWIIM_SHUFFLE),
        p.get_eq_presets(),
        p.load_eq("Jazz"),
        p.disable_eq(),
        p.get_shutdown_timer(),
        p.play_audio_url("https://hd1.wamu.org/wamu-1"),
        p.set_volume_relative(-10),
        p.get_playback_status(),
    )

    # Run all of the above commands, order not guaranteed
    for result in results:
        print(result)
        print('\n')

# Asyncio yadda-yadda
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
```
