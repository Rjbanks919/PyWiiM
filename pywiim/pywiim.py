"""Python library to control WiiM devices.

This module provides a class to allow a user to control a specified WiiM device
using the WiiM API.

The class is designed to be used asynchronously for Home Assistant, so
"""

import json

import asyncio
import aiohttp

from .const import *

class PyWiim:
    """Represents a WiiM device to be controlled."""

    def __init__(self, host, session=None):
        """Initialize the object.

        Args:
            host (str): The IP my guy
            session (:obj:`ClientSession`): yeah...

        """
        self._host = host
        self._aiohttp_session = session

        # Tracked for later :)
        self._created_session = False


    async def close(self):
        """Close the aiohttp connection."""
        if self._created_session and self._aiohttp_session is not None:
            await self._aiohttp_session.close()
            self._aiohttp_session = None
            self._created_session = False


    def _init_aiohttp_session(self):
        """Initialize an aiohttp session if one does not exist."""
        if self._aiohttp_session is None:
            self._aiohttp_session = aiohttp.ClientSession()
            self._created_session = True


    async def _get(self, request: str):
        """Send a GET request to the WiiM API.

        Note:
            SSL is not verified as this will cause failures.

        Args:
            request (str): GET request to send.

        Returns:
            str: The text response from the WiiM device.

        """
        url = PYWIIM_API_URL_HTTPS + self._host + PYWIIM_API_URL_BODY + request

        try:
            self._init_aiohttp_session()
            response = await self._aiohttp_session.get(url, verify_ssl=False)
            if response.status == STATUS_OK:
                # TODO: Should this just pull the text?
                return await response.text()
            else:
                raise CannotConnectError(response)
        except (asyncio.TimeoutError, aiohttp.clientError) as error:
            raise CannotConnectError() from error


    # Begin information-getter commands

    async def get_device_information(self):
        """Get the WiiM device information.

        Returns:
            {str: str}: Dictionary of device keys and values.

        """
        response = json.loads(await self._get(PYWIIM_CMD_GET_DEVICE_INFO))
        return response.copy()


    async def get_connection_status(self):
        """Get the WiiM device WiFi connection status.

        Note:
            Possible returned statuses are:
                1. "PROCESS"  -> In progress
                2. "PAIRFAIL" -> Wrong password
                3. "FAIL"     -> Connect fail
                4. "OK"       -> Connected

        Returns:
            str: Current connection status

        """
        response = await self._get(PYWIIM_CMD_GET_WIFI_INFO)
        return response


    async def get_playback_status(self):
        """Get the WiiM device playback status.

        Returns:
            {str: str}: Dictionary of the playback keys and values.
        """
        response = json.loads(await self._get(PYWIIM_CMD_GET_PLAY_INFO))
        return response.copy()


    async def get_eq_status(self):
        """Get the WiiM Equalization status.

        Note:
            This seems to be broken currently on WiiM's side.

        """
        response = json.loads(await self._get(PYWIIM_CMD_GET_EQ_STATUS))
        return response.copy()


    async def get_eq_presets(self):
        """Get a list of WiiM Equalization preset names."""
        response = await self._get(PYWIIM_CMD_GET_EQ_LIST)
        return response


    async def get_shutdown_timer(self):
        """Gets the current shutdown timer.

        Returns:
            int: Seconds left before shutdown occurs.

        """
        return int(await self._get(PYWIIM_CMD_GET_SHUTDOWN))


    # Begin playback commands

    async def pause(self):
        """Send 'pause' command to wiim."""
        await self._get(PYWIIM_CMD_PAUSE)


    async def play(self):
        """Send 'play' command to wiim."""
        await self._get(PYWIIM_CMD_PLAY)


    async def toggle(self):
        """Send 'toggle pause/play' command to wiim."""
        await self._get(PYWIIM_CMD_TOGGLE)


    async def previous(self):
        """Send 'previous' command to wiim."""
        await self._get(PYWIIM_CMD_PREVIOUS)


    async def next(self):
        """Send 'next' command to wiim."""
        await self._get(PYWIIM_CMD_NEXT)


    async def seek(self, duration: int):
        """Send 'seek <DURATION>' command to wiim (0 -> duration in sec).

        Args:
            duration (int): Duration (in seconds) to seek.
        """
        await self._get(PYWIIM_CMD_SEEK + str(duration))


    async def stop(self):
        """Send 'stop' command to wiim."""
        await self._get(PYWIIM_CMD_STOP)


    async def set_volume(self, volume: int):
        """Send volume level to wiim (0 -> 100).

        Args:
            volume (int): Volume level to set [0, 100].
        """
        await self._get(PYWIIM_CMD_VOLUME_SET + str(volume))


    async def mute(self):
        """Send 'mute' command to wiim."""
        await self._get(PYWIIM_CMD_MUTE_SET + PYWIIM_MUTE)


    async def unmute(self):
        """Send 'unmute' command to wiim."""
        await self._get(PYWIIM_CMD_MUTE_SET + PYWIIM_UNMUTE)


    async def set_loopmode(self, loopmode: str):
        """Enable/disable shuffle mode.

        Args:
            loopmode (str): Loopmode to set (see constants for values).
        """
        await self._get(PYWIIM_CMD_LOOPMODE_SET + loopmode)


    async def enable_eq(self):
        """Enable WiiM Equalization."""
        await self._get(PYWIIM_CMD_EQ_ON)


    async def disable_eq(self):
        """Disable WiiM Equalization."""
        await self._get(PYWIIM_CMD_EQ_OFF)


    async def load_eq(self, eq: str):
        """Load an EQ preset.

        Args:
            eq (str): EQ preset to load

        """
        await self._get(PYWIIM_CMD_EQ_LOAD + eq)


    async def reboot(self):
        """Reboot the WiiM device."""
        await self._get(PYWIIM_CMD_REBOOT)


    async def schedule_shutdown(self, delay: int):
        """Schedule a shutdown for the WiiM device.

        Args:
            delay (int): How long to wait (in seconds) before shutting down.

        Notes:
            A delay of 0 causes an instant shutdown, whereas -1 will cancel a
            previous shutdown timer.

        """
        await self._get(PYWIIM_CMD_SET_SHUTDOWN + str(delay))


    async def set_source(self, source: str):
        """Set the source for WiiM.

        Args:
            source (str): Source to set (see constants for values).

        """
        await self._get(PYWIIM_CMD_SOURCE + source)


    async def play_audio_url(self, url: str):
        """Plays the Audio URL.

        Notes:
            Try with url=https://hd1.wamu.org/wamu-1

        Args:
            url (str): Audio URL to play.

        """
        await self._get(PYWIIM_CMD_PLAY_AUDIO_URL + url)


    # Begin advanced commands

    async def set_volume_relative(self, offset: int):
        """Offsets the volume level by a given amount (+/-).

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


class CannotConnectError(Exception):
    """Exception to indicate an error in connection."""

