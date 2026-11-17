# Copyright 2023-2026 Michael Beckh (mbeckh)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Remove padding in ID3 tag."""

from __future__ import annotations

from functools import partial
import os
from pathlib import Path
from typing import override

from mutagen.id3 import ID3

from picard.file import FileIdentity
from picard.plugin3.api import (
    BaseAction,
    DebugOpt,
    File,
    PluginApi,
    t_,
)
from picard.util import (
    iter_files_from_objects,
    thread,
)


def remove_padding(api: PluginApi, file: File) -> None:
    """Run optimization on save."""

    def no_padding(_info) -> int:
        return 0

    filepath = Path(file.filename)
    setting = api.global_config.setting

    api.logger.debug_if(DebugOpt.PLUGIN_DEVELOPMENT, "Removing padding for file: %r", filepath)
    st = filepath.stat()

    # actual optimization, i.e. remove padding
    id3 = ID3(filepath)

    if setting['write_id3v1']:
        v1 = 2
    else:
        v1 = 0

    if setting['write_id3v23']:
        separator = setting['id3v23_join_with']
        id3.save(v1=v1, v2_version=3, v23_sep=separator, padding=no_padding)
    else:
        id3.save(v1=v1, v2_version=4, padding=no_padding)

    # preserve timestamps if requested
    preserve_timestamps = setting['preserve_timestamps']

    if preserve_timestamps:
        os.utime(filepath, ns=(st.st_atime_ns, st.st_mtime_ns))

    st_after = filepath.stat()

    file._file_identity = FileIdentity(filepath)
    file._update_filesystem_metadata(file.orig_metadata)

    if st_after.st_size > st.st_size:
        api.logger.error(
            "Something went wrong. File grew from %d bytes to %d bytes: %r", st.st_size, st_after.st_size, filepath
        )
    elif st_after.st_size == st.st_size:
        api.logger.debug("File already had no padding at size of %d bytes: %r", st.st_size, filepath)
    else:
        api.logger.debug(
            "File padding removed, %d bytes stripped to size of %d bytes: %r",
            st.st_size - st_after.st_size,
            st_after.st_size,
            filepath,
        )


class RemovePaddingAction(BaseAction):
    """Context menu action."""

    TITLE = t_('ui.action.title', "Remove Padding")

    @override
    def callback(self, objs: list) -> None:
        for file in iter_files_from_objects(objs, save=True):
            file.set_pending()
            thread.run_task(partial(self._run, file), priority=2, thread_pool=file.tagger.save_thread_pool)

    def _run(self, file: File) -> None:
        remove_padding(self.api, file)
        file.clear_pending(signal=True)


def enable(api: PluginApi) -> None:
    """Enable plugin."""
    api.register_file_post_save_processor(remove_padding)

    api.register_clusterlist_action(RemovePaddingAction)
    api.register_cluster_action(RemovePaddingAction)
    api.register_album_action(RemovePaddingAction)
    api.register_track_action(RemovePaddingAction)
    api.register_file_action(RemovePaddingAction)


def disable() -> None:
    """Disable plugin."""
