from conans import ConanFile, CMake, tools
import os


class MSYS2Conan(ConanFile):
    name = "msys2_installer"
    version = "20161025"
    license = "MSYS license"
    description = "MSYS2 is a software distro and building platform for Windows"
    url = "https://github.com/bincrafters/conan-msys2_installer"
    no_copy_source = True
    settings = {"os": ["Windows"], "arch": ["x86", "x86_64"]}
    
    def source(self):
        if self.settings.arch == "x86_64":
            msys2_arch = "x86_64"
            checksum = "2c198787ea1c4be39ff80466c4d831f8c7f06bd56d6d190bf63ede35292e344c"
        elif self.settings.arch == "x86":
            msys2_arch = "i686"
            checksum = "4951a47177777a54c7ad4ac99755ba4bbdf1a0cb23a174a72d91f71dc25bcb15"
        else:
            raise Exception("unsupported architecture %s" % self.settings.arch)

        archive_name = "msys2-base-%s-%s.tar.xz" % (msys2_arch, self.version)
        url = "http://repo.msys2.org/distrib/%s/%s" % (msys2_arch, archive_name)
        self.output.warn("download %s into %s" % (url, archive_name))
        tools.download(url, archive_name, verify=True)
        tools.check_sha256(archive_name, checksum)
        tools.untargz(archive_name)
        os.unlink(archive_name)
        
    def build(source):
        pass

    def package(self):
        if self.settings.arch == "x86_64":
            self.copy(pattern="*", dst=".", src="msys64")
        elif self.settings.arch == "x86":
            self.copy(pattern="*", dst=".", src="msys32")
        else:
            raise Exception("unsupported architecture %s" % self.settings.arch)

    def package_info(self):
        self.env_info.path.append(os.path.join(self.package_folder, "usr", "bin"))