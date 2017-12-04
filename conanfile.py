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
    build_requires = "7z_installer/1.0@conan/stable"
    
    settings = {
        "os": ["Windows"], "arch": ["x86", "x86_64"]
    }

    def source(self):
        # build tools have to download files in build method when the
        # source files downloaded will be different based on architecture or OS
        pass
        
    def build(self):
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

        msys_dir = "msys64" if self.settings.arch == "x86_64" else "msys32"
        
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
        msys_dir = "msys64" if self.settings.arch == "x86_64" else "msys32"
        self.copy("*", dst=".", src=msys_dir)
        

    def package_info(self):
        msys_root = self.package_folder
        msys_bin = os.path.join(msys_root, "usr", "bin")
        
        self.output.info("Creating MSYS_ROOT env var : %s" % msys_root)
        self.env_info.MSYS_ROOT = msys_root
        
        self.output.info("Creating MSYS_ROOT env var : %s" % msys_bin)
        self.env_info.MSYS_BIN = msys_bin

        self.output.info("Appending PATH env var with : " + msys_bin)
        self.env_info.path.append(msys_bin)
              
        # self.process_path_options(msys_bin, "bash.exe")

    # Commenting out because a feature was removed from conan in 0.29
    # Defaulting to adding MSYS to path until we can give user the option
    # Todo: Revisit upon resolution of Conan issue 2096
    # 
    # options = {
        # 'modify_path': ['append', 'prepend', 'skip'],
        # 'if_path_conflict': ['replace', 'skip', 'add_anyway']
    # }
    # default_options = (
        # 'modify_path=append', 
        # 'if_path_conflict=add_anyway'
    # )
    
    # def package_id(self):
        # self.info.options.modify_path = "any"
        # self.info.options.if_path_conflict = "any"      
    


        
    # def process_path_options(self, value_to_add, conflict_search_string):
        # if self.options.if_path_conflict ==  'add_anyway':
            # self.modify_path(value_to_add)
        # else:
            # existing_path = tools.which(conflict_search_string)
            # if existing_path:
                # if self.options.if_path_conflict ==  'replace':
                    # self.output.info(conflict_search_string + " already exists in PATH at : " + existing_path)
                    # self.output.info("Replacing with path : " + value_to_add)
                    # self.output.warn("Replacement method not yet implemented.")
                    # # TODO: Actually implement/verify replacement behavior
                # else:
                    # self.modify_path(value_to_add)
            # else:
                # self.modify_path(value_to_add)
            
    # def modify_path(self, value_to_append):
        # if self.options.modify_path ==  'append':
            # # TODO: Actually implement/verify append behavior
            # self.output.info("Appending PATH env var with : " + value_to_append)
            # self.env_info.path.append(value_to_append)
        # elif self.options.modify_path == 'prepend':
            # # TODO: Actually implement/verify prepend behavior
            # self.output.info("Prepending PATH env var with MSYS_BIN")
            # self.env_info.path.append(value_to_append)
        # else:  # do nothing for skip
            # pass
             