import os

from conans import ConanFile, CMake, tools


class ppConsulTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        # Current dir is "test_package/build/<build_id>" and CMakeLists.txt is
        # in "test_package"
        cmake.configure()
        cmake.build()

    # def imports(self):
    #     self.copy("*.dll", dst="bin", src="bin")
    #     self.copy("*.dylib*", dst="bin", src="lib")
    #     self.copy('*.so*', dst='bin', src='lib')

    def test(self):
        bin_path = os.path.join("bin", "example")
        self.run(bin_path, run_environment=True)
