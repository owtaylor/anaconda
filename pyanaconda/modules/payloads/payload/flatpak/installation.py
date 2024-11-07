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

from pyanaconda.modules.common.task import Task
from pyanaconda.modules.payloads.payload.flatpak.flatpak_manager import FlatpakManager


class CalculateFlatpaksSizeTask(Task):
    """Task to determine space needed for Flatpaks"""

    def __init__(self, flatpak_manager: FlatpakManager):
        """Create a new task."""
        super().__init__()
        self._flatpak_manager = flatpak_manager

    @property
    def name(self):
        """Name of the task."""
        return "Calculate needed space for Flatpaks"

    def run(self):
        """Run the task."""
        self._flatpak_manager.calculate_size(self)


class DownloadFlatpaksTask(Task):
    """Task to download remote Flatpaks"""

    def __init__(self, flatpak_manager):
        """Create a new task."""
        super().__init__()
        self._flatpak_manager = flatpak_manager

    @property
    def name(self):
        """Name of the task."""
        return "Download remote Flatpaks"

    def run(self):
        """Run the task."""
        self._flatpak_manager.download(self)


class InstallFlatpaksTask(Task):
    """Task to install flatpaks"""

    def __init__(self, flatpak_manager):
        """Create a new task."""
        super().__init__()
        self._flatpak_manager = flatpak_manager

    @property
    def name(self):
        """Name of the task."""
        return "Install flatpaks"

    def run(self):
        """Run the task."""
        self._flatpak_manager.install(self)
