# -*- coding: utf-8 -*-
"""Constants for PyWiiM."""
# General constants
STATUS_OK = 200


# WiiM API URL
PYWIIM_API_URL_HTTPS = "https://"              # HTTPS portion of URL
PYWIIM_API_URL_BODY  = "/httpapi.asp?command=" # Main body portion of URL


# WiiM API Commands
PYWIIM_CMD_GET_DEVICE_INFO = "getStatusEx"              # Get-Device-Info command
PYWIIM_CMD_GET_WIFI_INFO   = "wlanGetConnectState"      # Get-WiFi-Info command
PYWIIM_CMD_GET_PLAY_INFO   = "getPlayerStatus"          # Get-Player-Info command
PYWIIM_CMD_PAUSE           = "setPlayerCmd:pause"       # Pause command
PYWIIM_CMD_PLAY            = "setPlayerCmd:play"        # Play command
PYWIIM_CMD_TOGGLE          = "setPlayerCmd:onepause"    # Toggle play/pause command
PYWIIM_CMD_PREVIOUS        = "setPlayerCmd:prev"        # Previous-Track command
PYWIIM_CMD_NEXT            = "setPlayerCmd:next"        # Next-Track command
PYWIIM_CMD_SEEK            = "setPlayerCmd:seek:"       # Seek command
PYWIIM_CMD_STOP            = "setPlayerCmd:stop"        # Stop command
PYWIIM_CMD_VOLUME_SET      = "setPlayerCmd:vol:"        # Set-Volume command
PYWIIM_CMD_MUTE_SET        = "setPlayerCmd:mute:"       # Set-Mute command
PYWIIM_CMD_LOOPMODE_SET    = "setPlayerCmd:loopmode:"   # Set-LoopMode command
PYWIIM_CMD_EQ_ON           = "EQOn"                     # Enable EQ command
PYWIIM_CMD_EQ_OFF          = "EQOff"                    # Disable EQ command
PYWIIM_CMD_GET_EQ_STATUS   = "EQGetStat"                # Get EQ status
PYWIIM_CMD_GET_EQ_LIST     = "EQGetList"                # Get EQ preset names
PYWIIM_CMD_EQ_LOAD         = "EQLoad:"                  # Load EQ preset
PYWIIM_CMD_REBOOT          = "reboot"                   # Reboot command
PYWIIM_CMD_SET_SHUTDOWN    = "setShutdown:"             # Set-Shutdown command
PYWIIM_CMD_GET_SHUTDOWN    = "getShutdown"              # Get-Shutdown command
PYWIIM_CMD_SOURCE          = "setPlayerCmd:switchmode:" # Source command
PYWIIM_CMD_PLAY_AUDIO_URL  = "setPlayerCmd:play:"       # Play-Audio-URL command


# WiiM API Command Arguments
PYWIIM_MUTE             = "1"         # Mute enabled
PYWIIM_UNMUTE           = "0"         # Mute disabled
PYWIIM_SEQUENCE         = "4"         # Tracks playing in sequence
PYWIIM_LOOP_ALL         = "0"         # Loop-All enabled
PYWIIM_LOOP_ONE         = "1"         # Loop-One enabled
PYWIIM_LOOP_ALL_SHUFFLE = "2"         # Loop-All/Shuffle enabled
PYWIIM_LOOP_ONE_SHUFFLE = "5"         # Loop-One/Shuffle enabled
PYWIIM_SHUFFLE          = "3"         # Shuffle enabled
PYWIIM_SOURCE_LINE_IN   = "line-in"   # Line-In source
PYWIIM_SOURCE_BLUETOOTH = "bluetooth" # Bluetooth source
PYWIIM_SOURCE_OPTICAL   = "optical"   # Optical source
PYWIIM_SOURCE_UDISK     = "udisk"     # USB-Disk source (?)
PYWIIM_SOURCE_WIFI      = "wifi"      # WiFi source


# WiiM Playback Modes
PYWIIM_MODE_NONE           = "0"  # None (?)
PYWIIM_MODE_AIRPLAY        = "1"  # AirPlay or AirPlay 2
PYWIIM_MODE_DLNA           = "2"  # 3rd-Party DLNA
PYWIIM_MODE_DEFAULT        = "10" # Default WiiM
PYWIIM_MODE_UDISK_PLAYLIST = "11" # USB-Disk playlist
PYWIIM_MODE_TF_PLAYLIST    = "16" # TF-Card Playlist
PYWIIM_MODE_SPOTIFY        = "31" # Spotify-Connect
PYWIIM_MODE_TIDAL          = "32" # TIDAL-Connect
PYWIIM_MODE_LINE_IN        = "40" # Line-In
PYWIIM_MODE_BLUETOOTH      = "41" # Bluetooth
PYWIIM_MODE_EXT_STORAGE    = "42" # External Storage
PYWIIM_MODE_OPTICAL        = "43" # Optical-In
PYWIIM_MODE_MIRROR         = "50" # Mirror (?)
PYWIIM_MODE_VOICEMAIL      = "60" # Voicemail (?)
PYWIIM_MODE_SLAVE          = "99" # Slave

# TODO
# - Add EQ preset names
# - ...
