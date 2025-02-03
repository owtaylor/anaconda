#
# Payload module for preinstalling Flatpaks
#
# Copyright (C) 2024 Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.  You should have received a copy of the
# GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.  Any Red Hat trademarks that are incorporated in the
# source code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission of
# Red Hat, Inc.
#
from pyanaconda.anaconda_loggers import get_module_logger
from pyanaconda.modules.payloads.base.utils import calculate_required_space
from pyanaconda.modules.payloads.constants import PayloadType, SourceType
from pyanaconda.modules.payloads.payload.flatpak.flatpak_interface import FlatpakInterface
from pyanaconda.modules.payloads.payload.flatpak.flatpak_manager import FlatpakManager
from pyanaconda.modules.payloads.payload.flatpak.installation import (
    CalculateFlatpaksSizeTask,
    CleanUpDownloadLocationTask,
    DownloadFlatpaksTask,
    InstallFlatpaksTask,
    PrepareDownloadLocationTask,
)
from pyanaconda.modules.payloads.payload.payload_base import PayloadBase

log = get_module_logger(__name__)


class FlatpakModule(PayloadBase):
    """The Flatpak payload module."""

    def __init__(self):
        super().__init__()
        self._flatpak_manager = FlatpakManager()

    def for_publication(self):
        """Get the interface used to publish this source."""
        return FlatpakInterface(self)

    @property
    def type(self):
        """Type of this payload."""
        return PayloadType.FLATPAK

    @property
    def default_source_type(self):
        """Type of the default source."""
        return None

    @property
    def supported_source_types(self):
        """List of supported source types."""
        # Include all the types of SourceType.
        return list(SourceType)

    def set_sources(self, sources):
        """Set a new list of sources to this payload.

        This overrides the base implementation since the sources we set here
        are the sources from the main payload, and can already be initialized.

        :param sources: set a new sources
        :type sources: instance of pyanaconda.modules.payloads.source.source_base.PayloadSourceBase
        """
        self._sources = sources
        self._flatpak_manager.set_sources(sources)
        self.sources_changed.emit()

    def set_flatpak_refs(self, refs):
        """Set the flatpak refs.

        :param refs: a list of flatpak refs
        """
        self._flatpak_manager.set_flatpak_refs(refs)

    def calculate_required_space(self):
        """Calculate space required for the installation.

        :return: required size in bytes
        :rtype: int
        """
        return calculate_required_space(self._flatpak_manager.download_size,
                                        self._flatpak_manager.install_size)

    def install_with_tasks(self):
        """Install the payload with tasks."""

        tasks = [
            CalculateFlatpaksSizeTask(
                flatpak_manager=self._flatpak_manager,
            ),
            PrepareDownloadLocationTask(
                flatpak_manager=self._flatpak_manager,
            ),
            DownloadFlatpaksTask(
                flatpak_manager=self._flatpak_manager,
            ),
            InstallFlatpaksTask(
                flatpak_manager=self._flatpak_manager,
            ),
            CleanUpDownloadLocationTask(
                flatpak_manager=self._flatpak_manager,
            ),
        ]

        return tasks
