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
from mycroft.audio.services import AudioBackend
from mycroft.util.log import LOG
try:
    from py_mplayer import MplayerCtrl
except ImportError:
    LOG.error("install py_mplayer with "
              "pip install git+https://github.com/JarbasAl/py_mplayer")
    raise


class MPlayerService(AudioBackend):
    """
        Audio backend for mplayer.
    """

    def __init__(self, config, bus, name='mplayer'):
        super(MPlayerService, self).__init__(config, bus)
        self.name = name
        self.index = 0
        self.normal_volume = None
        self.tracks = []
        self.mpc = MplayerCtrl()

    def supported_uris(self):
        return ['file', 'http', 'https']

    def clear_list(self):
        self.tracks = []

    def add_list(self, tracks):
        self.tracks += tracks
        LOG.info("Track list is " + str(tracks))

    def play(self, repeat=False):
        """ Start playback of playlist.

        TODO: Add support for repeat
        """
        self.stop()
        if len(self.tracks):
            # play self.index track
            self.mpc.loadfile(self.tracks[self.index])

    def stop(self):
        self.mpc.stop()
        return True  # TODO: Return False if not playing

    def pause(self):
        if not self.mpc.paused:
            self.mpc.pause()

    def resume(self):
        if self.mpc.paused:
            self.mpc.pause()

    def lower_volume(self):
        if self.normal_volume is None:
            self.normal_volume = self.mpc.volume
            self.mpc.volume = self.mpc.volume / 3

    def restore_volume(self):
        if self.normal_volume:
            self.mpc.volume = self.normal_volume
        else:
            self.mpc.volume = 50
        self.normal_volume = None

    def track_info(self):
        """
            Fetch info about current playing track.

            Returns:
                Dict with track info.
        """
        ret = {}
        if self.index in self.track_data:
            ret = self.track_data[self.index]
        if "title" not in ret:
            ret['title'] = self.mpc.get_meta_title()
        if "artist" not in ret:
            ret['artist'] = self.mpc.get_meta_artist()
        if "album" not in ret:
            ret['album'] = self.mpc.get_meta_album()
        if "genre" not in ret:
            ret['genre'] = self.mpc.get_meta_genre()
        if "year" not in ret:
            ret['year'] = self.mpc.get_meta_year()
        if "track" not in ret:
            ret['track'] = self.mpc.get_meta_track()
        if "comment" not in ret:
            ret['comment'] = self.mpc.get_meta_comment()
        return ret

    def shutdown(self):
        """
            Shutdown mplayer

        """
        self.mpc.destroy()


def load_service(base_config, emitter):
    backends = base_config.get('backends', [])
    services = [(b, backends[b]) for b in backends
                if backends[b]['type'] == 'mplayer' and
                backends[b].get("active", True)]
    instances = [MPlayerService(s[1], emitter, s[0]) for s in services]
    return instances
