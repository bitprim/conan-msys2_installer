from conans import ConanFile
import os


class TestPackage(ConanFile):
    generators = "cmake"
        
    def test(self):
        self.run(os.path.join("msys2"))