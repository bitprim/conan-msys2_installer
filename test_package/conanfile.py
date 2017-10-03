from conans import ConanFile


class TestPackage(ConanFile):
        
    def test(self):
        self.run("msys2 --login -c pwd")