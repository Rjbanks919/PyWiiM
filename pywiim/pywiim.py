"""
pywiim

This module provides a Python interface for the WiiM device API.

Classes:
    PyWiim:
    PyWiimCannotConnectError:

Usage:
    To use this module, get an instance of the PyWiim class and call methods!
"""

import json
import asyncio
import aiohttp

from .const import *

class PyWiim:
    """
    A class to represent a WiiM device.
    """

    def __init__(self, host: str, session: aiohttp.ClientSession | None =None):
        """
        Initializes a new instance of PyWiim .

        Args:
            host    (str): IP address of the WiiM device.
            session (aiohttp.ClientSession): Optional aiohttp client session.
        """
        self._host = host
        self._aiohttp_session = session

        # Tracked for later :)
        self._created_session = False


    async def close(self):
        """
        Closes out the WiiM device connection.
        """
        if self._created_session and self._aiohttp_session is not None:
            await self._aiohttp_session.close()
            self._aiohttp_session = None
            self._created_session = False


    async def _get(self, request: str) -> str:
        """
        Retrieves data from WiiM's API using a GET request.

        Args:
            request (str): API command to send.

        Returns:
            str: The text response from the WiiM device.

        Raises:
            PyWiimCannotConnectError: If the API request encounters an error.
        """
        url = PYWIIM_API_URL_HTTPS + self._host + PYWIIM_API_URL_BODY + request

        try:
            if self._aiohttp_session is None:
                # Setup aiohttp session if we don't have one
                self._aiohttp_session = aiohttp.ClientSession()
                self._created_session = True

            # Note no SSL, WiiM doesn't support it
            response = await self._aiohttp_session.get(url, verify_ssl=False)

            if response.status == STATUS_OK:
                # Success! Return the raw response text
                return await response.text()
            else:
                raise PyWiimCannotConnectError(response)

        except (asyncio.TimeoutError, aiohttp.clientError) as error:
            raise PyWiimCannotConnectError() from error


    async def get_device_information(self) -> dict[str, str]:
        """
        Retrieves WiiM device information.

        This includes firmware, network details, hardware details, and a ton of
        other goodies.

        Returns:
            dict[str, str]: Device information key/value pairs.
        """
        response = json.loads(await self._get(PYWIIM_CMD_GET_DEVICE_INFO))
        return response.copy()


    async def get_connection_status(self) -> str:
        """
        Retrieves the WiiM device WiFi connection status.

        Possible returned statuses are:
            1. "PROCESS"  -> In progress
            2. "PAIRFAIL" -> Wrong password
            3. "FAIL"     -> Connect fail
            4. "OK"       -> Connected

        Returns:
            str: Current connection status
        """
        return await self._get(PYWIIM_CMD_GET_WIFI_INFO)


    async def get_playback_status(self) -> dict[str, str]:
        """
        Retrieves the WiiM device playback status.

        This includes source, song title/album/artist, position, volume, and
        more.

        Returns:
            dict[str, str]: Playback status key/value pairs.
        """
        response = json.loads(await self._get(PYWIIM_CMD_GET_PLAY_INFO))
        return response.copy()


    async def get_eq_status(self) -> dict[str, str]:
        """
        Retrieves the WiiM Equalization status.

        Note:
            This seems to be broken currently on WiiM's side.

        Returns:
            dict[str, str]: Single key/value pair with EQ status.
        """
        response = json.loads(await self._get(PYWIIM_CMD_GET_EQ_STATUS))
        return response.copy()


    # TODO!!!! ----------------------------------------------------------- Parse list!
    async def get_eq_presets(self):
        """
        Get a list of WiiM Equalization preset names.
        """
        response = await self._get(PYWIIM_CMD_GET_EQ_LIST)
        return response


    async def get_shutdown_timer(self) -> int:
        """
        Retrieves the time left on the shutdown timer.

        Returns:
            int: Time left on the shutdown timer, in seconds.
        """
        return int(await self._get(PYWIIM_CMD_GET_SHUTDOWN))


    async def pause(self):
        """
        Sends the 'pause' command to the WiiM device.
        """
        await self._get(PYWIIM_CMD_PAUSE)


    async def play(self):
        """
        Sends the 'play' command to the WiiM device.
        """
        await self._get(PYWIIM_CMD_PLAY)


    async def toggle(self):
        """
        Sends the 'play/pause toggle' command to the WiiM device.
        """
        await self._get(PYWIIM_CMD_TOGGLE)


    async def previous(self):
        """
        Sends the 'previous track' command to the WiiM device.
        """
        await self._get(PYWIIM_CMD_PREVIOUS)


    async def next(self):
        """
        Sends the 'next track' command to the WiiM device.
        """
        await self._get(PYWIIM_CMD_NEXT)


    async def seek(self, duration: int):
        """
        Sends the 'seek <duration> seconds' command to the WiiM device.

        Args:
            duration (int): Duration to seek, in seconds.
        """
        await self._get(PYWIIM_CMD_SEEK + str(duration))


    async def stop(self):
        """
        Sends the 'stop' command to the WiiM device.
        """
        await self._get(PYWIIM_CMD_STOP)


    async def set_volume(self, volume: int):
        """
        Sends the 'set volume' command to the WiiM device.

        Args:
            volume (int): Volume level to set, from 0 to 100.
        """
        await self._get(PYWIIM_CMD_VOLUME_SET + str(volume))


    async def mute(self):
        """
        Sends the 'mute' command to the WiiM device.
        """
        await self._get(PYWIIM_CMD_MUTE_SET + PYWIIM_MUTE)


    async def unmute(self):
        """
        Sends the 'unmute' command to the WiiM device.
        """
        await self._get(PYWIIM_CMD_MUTE_SET + PYWIIM_UNMUTE)


    async def set_loopmode(self, loopmode: str):
        """
        Sends the 'set loopmode' command to the WiiM device.

        Args:
            loopmode (str): Loopmode to set (see constants for values).
        """
        await self._get(PYWIIM_CMD_LOOPMODE_SET + loopmode)


    async def enable_eq(self):
        """
        Sends the 'enable EQ' command to the WiiM device.
        """
        await self._get(PYWIIM_CMD_EQ_ON)


    async def disable_eq(self):
        """
        Sends the 'disable EQ' command to the WiiM device.
        """
        await self._get(PYWIIM_CMD_EQ_OFF)


    async def load_eq(self, eq: str):
        """
        Sends the 'load EQ' command to the WiiM device.

        Args:
            eq (str): EQ preset to load
        """
        await self._get(PYWIIM_CMD_EQ_LOAD + eq)


    async def reboot(self):
        """
        Sends the 'reboot' command to the WiiM device.
        """
        await self._get(PYWIIM_CMD_REBOOT)


    async def schedule_shutdown(self, delay: int):
        """
        Sends the 'schedule shutdown' command to the WiiM device.

        Args:
            delay (int): How long to wait before shutting down, in seconds.

        Notes:
            A delay of 0 causes an instant shutdown, whereas -1 will cancel a
            previous shutdown timer.
        """
        await self._get(PYWIIM_CMD_SET_SHUTDOWN + str(delay))


    async def set_source(self, source: str):
        """
        Sends the 'set source' command to the WiiM device.

        Args:
            source (str): Source to set (see constants for values).
        """
        await self._get(PYWIIM_CMD_SOURCE + source)


    async def play_audio_url(self, url: str):
        """
        Sends the 'play audio URL' command to the WiiM device.

        Args:
            url (str): Audio URL to play.

        Notes:
            Try with url=https://hd1.wamu.org/wamu-1
        """
        await self._get(PYWIIM_CMD_PLAY_AUDIO_URL + url)


    async def set_volume_relative(self, offset: int):
        """
        Offsets the volume level by a given amount (+/-).

        Args:
            offset (int): Amount to offset volume level.

        """
        status = await self.get_playback_status()
        new_vol = int(status["vol"]) + offset

        # Bound the new volume
        if new_vol > 100:
            new_vol = 100
        elif new_vol < 0:
            new_vol = 0

        await self.set_volume(new_vol)


    async def get_track(self) -> str:
        """
        Retrieves the track from the WiiM playback status and decodes it.

        Returns:
            str: Track name
        """
        status = await self.get_playback_status()
        return bytes.fromhex(status["Title"]).decode("utf-8")


    async def get_album(self) -> str:
        """
        Retrieves the album from the WiiM playback status and decodes it.

        Returns:
            str: Album name
        """
        status = await self.get_playback_status()
        return bytes.fromhex(status["Album"]).decode("utf-8")


    async def get_artist(self) -> str:
        """
        Retrieves the artist from the WiiM playback status and decodes it.

        Returns:
            str: Artist name
        """
        status = await self.get_playback_status()
        return bytes.fromhex(status["Artist"]).decode("utf-8")


class PyWiimCannotConnectError(Exception):
    """
    Exception to indicate an error in connection.
    """

