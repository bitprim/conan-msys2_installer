from conans import ConanFile, tools
import os


class TestPackage(ConanFile):
        
    def test(self):
        new_path = os.environ['PATH'] + os.pathsep + self.deps_env_info['msys2_installer'].MSYS_BIN
        with tools.environment_append({'PATH': new_path}):
            self.run(os.path.join('%MSYS_BIN%\\bash -c "yasm --version"'))
            self.run(os.path.join('%MSYS_BIN%\\bash -c "make --version"'))
            self.run(os.path.join('%MSYS_BIN%\\bash -c "diff --help"'))
            self.run(os.path.join('%MSYS_BIN%\\bash -c "pkg-config --version"'))
            self.run(os.path.join('%MSYS_BIN%\\bash -c "autoconf --version"'))
            self.run(os.path.join('%MSYS_BIN%\\bash -c "autoreconf --version"'))
