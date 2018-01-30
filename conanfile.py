#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright (c) 2017 Bitprim developers (see AUTHORS)
#
# This file is part of Bitprim.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from conans import ConanFile, tools
from conans import __version__ as conan_version
from conans.model.version import Version
import os


class MSYS2InstallerConan(ConanFile):
    name = "msys2_installer"
    version = "20161025"
    description = "MSYS2 is a software distro and building platform for Windows"
    url = "https://github.com/bitprim/conan-msys2_installer"
    license = "MSYS license"
    exports = ["LICENSE.md"]
    build_requires = "7z_installer/1.0@conan/stable"

    settings = {"os_build": ["Windows"], "arch_build": ["x86", "x86_64"]}

    @property
    def os(self):
        return self.settings.get_safe("os_build") or self.settings.get_safe("os")

    @property
    def arch(self):
        return self.settings.get_safe("arch_build") or self.settings.get_safe("arch")

    def source(self):
        # build tools have to download files in build method when the
        # source files downloaded will be different based on architecture or OS
        pass
        
    def build(self):
        msys_arch = "x86_64" if self.arch == "x86_64" else "i686"
        archive_name = "msys2-base-{0}-{1}.tar.xz".format(msys_arch, self.version)
        url = "http://repo.msys2.org/distrib/{0}/{1}".format(msys_arch, archive_name)
        self.output.info("Download {0} into {1}".format(url, archive_name))
        tools.download(url, archive_name)
        tar_name = archive_name.replace(".xz", "")
        self.run("7z x {0}".format(archive_name))
        self.run("7z x {0}".format(tar_name))
        os.unlink(archive_name)
        os.unlink(tar_name)

        msys_dir = "msys64" if self.arch == "x86_64" else "msys32"
        
        with tools.chdir(os.path.join(msys_dir, "usr", "bin")):
            self.run('bash -l -c "pacman -S base-devel --noconfirm"')
        
        # create /tmp dir in order to avoid
        # bash.exe: warning: could not find /tmp, please create!
        tmp_dir = os.path.join(msys_dir, 'tmp')
        if not os.path.isdir(tmp_dir):
            os.makedirs(tmp_dir)
        tmp_name = os.path.join(tmp_dir, 'dummy')
        with open(tmp_name, 'a'):
            os.utime(tmp_name, None)


    def package(self):
        msys_dir = "msys64" if self.arch == "x86_64" else "msys32"
        self.copy("*", dst=".", src=msys_dir)
        

    def package_info(self):
        msys_root = self.package_folder
        msys_bin = os.path.join(msys_root, "usr", "bin")
        
        self.output.info("Creating MSYS_ROOT env var : %s" % msys_root)
        self.env_info.MSYS_ROOT = msys_root
        
        self.output.info("Creating MSYS_BIN env var : %s" % msys_bin)
        self.env_info.MSYS_BIN = msys_bin

        self.output.info("Appending PATH env var with : " + msys_bin)
        self.env_info.path.append(msys_bin)
