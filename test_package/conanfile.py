from conans import ConanFile
import os


class TestPackage(ConanFile):
        
    def test(self):
        self.run(os.path.join('"msys2 --login -c pwd"'))