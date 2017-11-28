#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, tools
import os


class MSYS2InstallerConan(ConanFile):
    name = "msys2_installer"
    version = "20161025"
    license = "MSYS license"
    description = "MSYS2 is a software distro and building platform for Windows"
    url = "https://github.com/bincrafters/conan-msys2_installer"
    settings = {"arch": ["x86", "x86_64"]}
    build_requires = "7z_installer/1.0@conan/stable"

    def source(self):
        msys_arch = "x86_64" if self.settings.arch == "x86_64" else "i686"
        archive_name = "msys2-base-{0}-{1}.tar.xz".format(msys_arch, self.version)
        url = "http://repo.msys2.org/distrib/{0}/{1}".format(msys_arch, archive_name)
        self.output.info("Download {0} into {1}".format(url, archive_name))
        tools.download(url, archive_name)
        tar_name = archive_name.replace(".xz", "")
        self.run("7z x {0}".format(archive_name))
        self.run("7z x {0}".format(tar_name))
        os.unlink(archive_name)
        os.unlink(tar_name)
        
    def build(self):
        msys_dir = "msys64" if self.settings.arch == "x86_64" else "msys32"
        
        # removed the following pacman installation because it caused 
        # binary to exceeded bintray max
        # Can remove if Bintray lifts the max for Conan packages. 
        with tools.chdir(os.path.join(msys_dir, "usr", "bin")):
            self.run('bash -l -c "pacman -S git curl zip unzip yasm base-devel --noconfirm"')
        
        # create /tmp dir in order to avoid
        # bash.exe: warning: could not find /tmp, please create!
        tmp_dir = os.path.join(msys_dir, 'tmp')
        if not os.path.isdir(tmp_dir):
            os.makedirs(tmp_dir)
        tmp_name = os.path.join(tmp_dir, 'dummy')
        with open(tmp_name, 'a'):
            os.utime(tmp_name, None)

    def package(self):
        msys_dir = "msys64" if self.settings.arch == "x86_64" else "msys32"
        self.copy("*", dst=".", src=msys_dir)
        
    def package_info(self):
        self.output.info("Creating MSYS_ROOT environment variable with : {0}".format(self.package_folder))
        self.env_info.MSYS_ROOT = self.package_folder
        self.env_info.MSYS_BIN = os.path.join(self.package_folder, "usr", "bin")
