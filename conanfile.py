from conans import ConanFile, CMake, tools
import os


class MSYS2Conan(ConanFile):
    name = "msys2_installer"
    version = "2.0"
    license = "MSYS license"
    description = "MSYS2 is a software distro and building platform for Windows"
    url = "https://github.com/SSE4/conan-msys2-installer"
    settings = {"os": ["Windows"], "arch": ["x86", "x86_64"]}
    
    def build(self):
        tag = "20161025"
        if self.settings.arch == "x86_64":
            msys2_arch = 'x86_64'
        elif self.settings.arch == "x86":
            msys2_arch = 'i686'
        else:
            raise Exception("unsupported architecture %s" % self.settings.arch)

        archive_name = "msys2-base-%s-%s.tar.xz" % (msys2_arch, tag)
        url = "http://repo.msys2.org/distrib/%s/%s" % (msys2_arch, archive_name)
        self.output.warn("download %s into %s" % (url, archive_name))
        tools.download(url, archive_name, verify=True)
        tools.untargz(archive_name)
        os.unlink(archive_name)

    def package(self):
        if self.settings.arch == "x86_64":
            self.copy(pattern="*", dst=".", src="msys64")
        elif self.settings.arch == "x86":
            self.copy(pattern="*", dst=".", src="msys32")
        else:
            raise Exception("unsupported architecture %s" % self.settings.arch)

    def package_info(self):
        self.env_info.path.append(os.path.join(self.package_folder, "usr", "bin"))