# Copyright 2017 Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from abc import ABCMeta, abstractmethod


class AudioBackend(metaclass=ABCMeta):
    """
        Base class for all audio backend implementations.

        Args:
            config: configuration dict for the instance
            bus:    Mycroft messagebus emitter
    """

    def __init__(self, config, bus):
        self._track_start_callback = None
        self.supports_mime_hints = False
        self.bus = bus
        self.config = config
        self.index = 0
        self.track_data = {}
        self.bus.on('play:status', self.handle_track_status)

    def uri2index(self, uri):
        for idx in self.track_data:
            if self.track_data[idx].get("uri", "") == uri:
                return idx
        return None

    def handle_track_status(self, message):
        index = message.data.get("playlist_position")
        uri = message.data.get("uri")
        if index is None and uri:
            index = self.uri2index(uri)
        if index is not None:
            # ignore disambiguation results
            for k in message.data:
                if message.data[k]:
                    self.track_data[index][k] = message.data[k]

    @abstractmethod
    def supported_uris(self):
        """
            Returns: list of supported uri types.
        """
        pass

    @abstractmethod
    def clear_list(self):
        """
            Clear playlist
        """
        pass

    @abstractmethod
    def add_list(self, tracks):
        """
            Add tracks to backend's playlist.

            Args:
                tracks: list of tracks.
        """
        pass

    @abstractmethod
    def play(self, repeat=False):
        """
            Start playback.

            Args:
                repeat: Repeat playlist, defaults to False
        """
        pass

    @abstractmethod
    def stop(self):
        """
            Stop playback.

            Returns: (bool) True if playback was stopped, otherwise False
        """
        pass

    def set_track_start_callback(self, callback_func):
        """
            Register callback on track start, should be called as each track
            in a playlist is started.
        """
        self._track_start_callback = callback_func

    def pause(self):
        """
            Pause playback.
        """
        pass

    def resume(self):
        """
            Resume paused playback.
        """
        pass

    def next(self):
        """
            Skip to next track in playlist.
        """
        # play index + 1
        self.play()

    def previous(self):
        """
            Skip to previous track in playlist.
        """
        # play index - 1
        self.play()

    def lower_volume(self):
        """
            Lower volume.
        """
        pass

    def restore_volume(self):
        """
            Restore normal volume.
        """
        pass

    def seek_forward(self, seconds=1):
        """
            Skip X seconds

            Args:
                seconds (int): number of seconds to seek, if negative rewind
        """
        pass

    def seek_backward(self, seconds=1):
        """
            Rewind X seconds

            Args:
                seconds (int): number of seconds to seek, if negative rewind
        """
        pass

    def track_info(self):
        """
            Fetch info about current playing track.

            Returns:
                Dict with track info.
        """
        if self.index not in self.track_data:
            return {"track_number": self.index}
        self.track_data[self.index]["track_number"] = self.index
        return self.track_data[self.index]

    def playlist_info(self):
        """
            Fetch info about current playing track.

            Returns:
                Dict with track info.
        """
        return self.track_data

    def shutdown(self):
        """ Perform clean shutdown """
        self.stop()


class RemoteAudioBackend(AudioBackend):
    """ Base class for remote audio backends.

        These may be things like Chromecasts, mopidy servers, etc.
    """
    pass
