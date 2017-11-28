from conans import ConanFile, tools
import os


class TestPackage(ConanFile):
        
    def test(self):
        new_path = os.environ['PATH'] + os.pathsep + self.deps_env_info['msys2_installer'].MSYS_BIN
        with tools.environment_append({'PATH': new_path}):
            self.run('%MSYS_BIN%\\bash -c ^"make --version^"')
