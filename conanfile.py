from conans import ConanFile, CMake
import os
import platform

class HelloConan(ConanFile):
    name = "Hello"
    version = "0.1"
    settings = "os", "compiler", "build_type", "arch"

    scm = {
        "type": "git",
        "url": "auto",
        "revision": "auto",
    }

    def build(self):
        cmake = CMake(self)
        gcc_dbg_src = '-DCMAKE_SH="CMAKE_SH-NOTFOUND"'
        if self.settings.compiler == "gcc" and self.settings.build_type == "Debug":
            gcc_dbg_src += ' -DCMAKE_CXX_FLAGS="-fdebug-prefix-map=%s/=src"' % os.getcwd()
        self.run('cmake . %s %s' % (cmake.command_line, gcc_dbg_src))
        self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include")
        if self.settings.compiler == "gcc" and self.settings.build_type == "Debug":
            self.copy("*.cpp", dst="src")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["hello"]

    def test(self):
        if platform.system() != self.settings.os:
            assert os.path.exists("bin/example")
        else:
            self.run(os.sep.join([".", "bin", "example"]))