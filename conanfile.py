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
        if self.settings.arch == "x86_64":
            msys2_arch = "x86_64"
        elif self.settings.arch == "x86":
            msys2_arch = "i686"
        else:
            raise Exception("unsupported architecture %s" % self.settings.arch)

        archive_name = "msys2-base-%s-%s.tar.xz" % (msys2_arch, self.version)
        url = "http://repo.msys2.org/distrib/%s/%s" % (msys2_arch, archive_name)
        self.output.info("download %s into %s" % (url, archive_name))
        tools.download(url, archive_name)
        tar_name = archive_name.replace(".xz","")
        self.run("7z e {0}".format(archive_name))
        self.run("7z e {0} -aoa".format(tar_name))
        os.unlink(archive_name)
        os.unlink(tar_name)
        
    def package(self):
        if self.settings.arch == "x86_64":
            self.copy(pattern="*", dst=".", src="msys64")
        elif self.settings.arch == "x86":
            self.copy(pattern="*", dst=".", src="msys32")
        else:
            raise Exception("unsupported architecture %s" % self.settings.arch)

    def package_info(self):
        bin_path = os.path.join(self.package_folder, "usr", "bin")
        self.output.info("Appending PATH environment variable with : {0}".format(bin_path))
        self.env_info.path.append(bin_path)
        
        self.output.info("Creating MSYS_ROOT environment variable with : {0}".format(self.package_folder))
        self.env_info.MSYS_ROOT = self.package_folder