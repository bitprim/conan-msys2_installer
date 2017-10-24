from conans import ConanFile, tools
import os


class MSYS2InstallerConan(ConanFile):
    name = "msys2_installer"
    version = "20161025"
    license = "MSYS license"
    description = "MSYS2 is a software distro and building platform for Windows"
    url = "https://github.com/bincrafters/conan-msys2_installer"
    settings = {"os": ["Windows"], "arch": ["x86", "x86_64"]}
    build_requires = "7z_installer/1.0@conan/stable"

    def source(self):
        msys_arch = "x86_64" if self.settings.arch == "x86_64" else "i686"
        archive_name = "msys2-base-%s-%s.tar.xz" % (msys_arch, self.version)
        url = "http://repo.msys2.org/distrib/%s/%s" % (msys_arch, archive_name)
        self.output.info("download %s into %s" % (url, archive_name))
        tools.download(url, archive_name)
        tar_name = archive_name.replace(".xz","")
        self.run("7z x {0}".format(archive_name))
        self.run("7z x {0}".format(tar_name))
        os.unlink(archive_name)
        os.unlink(tar_name)
        
    def build(self):
        msys_dir = "msys64" if self.settings.arch == "x86_64" else "msys32"
        with tools.chdir(os.path.join(msys_dir, "usr", "bin")):
            self.run('bash -l -c "pacman -S pkgconfig yasm diffutils make --noconfirm')

    def package(self):
        msys_dir = "msys64" if self.settings.arch == "x86_64" else "msys32"
        self.copy("*", dst=".", src=msys_dir)
        
    def package_info(self):
        self.output.info("Creating MSYS_ROOT environment variable with : {0}".format(self.package_folder))
        self.env_info.MSYS_ROOT = self.package_folder
        
        self.output.info("Appending PATH environment variable with : {0}".format(self.package_folder))
        self.env_info.path.append(self.package_folder)
        
        bin_path = os.path.join(self.package_folder, "usr", "bin")
        
        self.output.info("Appending PATH environment variable with : {0}".format(bin_path))
        self.env_info.path.append(bin_path)
