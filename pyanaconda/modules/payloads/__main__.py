#
# Payloads DBus service launcher.
#
# Copyright (C) 2020 Red Hat, Inc.
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
from pyanaconda.modules.common import init
init("/tmp/packaging.log")

import os
if "LD_PRELOAD" in os.environ:
    del os.environ["LD_PRELOAD"]  # pylint: disable=environment-modify

# We need Flatpak to read configuration files from the target and write
# to the target system installation. Since we use the Flatpak API
# in process, we need to do this by modifying the environment before
# we start any threads. Setting these variables will be harmless if
# we aren't actually using Flatpak.

from pyanaconda.core.configuration.anaconda import conf
os.environ["FLATPAK_DOWNLOAD_TMPDIR"] = os.path.join(conf.target.system_root, "var/tmp")  # pylint: disable=environment-modify
os.environ["FLATPAK_CONFIG_DIR"] = os.path.join(conf.target.system_root, "etc/flatpak")  # pylint: disable=environment-modify
os.environ["FLATPAK_OS_CONFIG_DIR"] = os.path.join(conf.target.system_root, "usr/share/flatpak")  # pylint: disable=environment-modify
os.environ["FLATPAK_SYSTEM_DIR"] = os.path.join(conf.target.system_root, "var/lib/flatpak")  # pylint: disable=environment-modify

from pyanaconda.modules.payloads.payloads import PayloadsService
service = PayloadsService()
service.run()
