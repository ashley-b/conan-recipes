import os

from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.env import VirtualBuildEnv, VirtualRunEnv
from conan.tools.files import copy, chdir, get
from conan.tools.gnu import Autotools, AutotoolsToolchain, AutotoolsDeps, PkgConfigDeps
from conan.tools.layout import basic_layout
from conan.tools.system.package_manager import Apt, Dnf

class oclintConan(ConanFile):
    name = "oclint"
    version = "22.02"
    package_type = "application"

    # Optional metadata
    license = "BSD-2-Clause"
    author = "<Put your name here> <And your email here>"
    homepage = "http://oclint.org/"
    url = "https://github.com/ashley-b/conan-recipes"
    description = "A static source code analysis tool to improve quality and reduce defects for C, C++ and Objective-C"
    topics = ("c", "c++", "linter")

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def layout(self):
        basic_layout(self)

    def system_requirements(self):
        apt = Apt(self)
        apt.install(["curl", "git", "xz-utils"])

        dnf = Dnf(self)
        dnf.install(["curl", "git", "xz"])

    def build_requirements(self):
        self.tool_requires("ninja/1.11.1")

    def requirements(self):
        self.requires("zlib/1.3")

    def generate(self):
        with chdir(self, os.path.join(self.source_folder, "oclint-scripts")):
            VirtualBuildEnv(self).generate()
            VirtualRunEnv(self).generate(scope="build")
            tc = AutotoolsToolchain(self)
            tc.generate()

            AutotoolsDeps(self).generate()
            PkgConfigDeps(self).generate()

#            tc = CMakeDeps(self)
#            tc.generate()
#
#            tc = CMakeToolchain(self)
#            tc.generate()

    def build(self):
        with chdir(self, os.path.join(self.source_folder, "oclint-scripts")):
            self.run("./make")

    def package(self):
        build_folder = os.path.join(self.source_folder, "build", "oclint-release")
        copy(self, "LICENSE", build_folder, dst=os.path.join(self.package_folder, "licenses"))
        for path in [ "bin", "lib" ]:
            self.output.info("Package Path {}".format(os.path.join(build_folder, path)))
            copy(self, "*", src=os.path.join(build_folder, path), dst=os.path.join(self.package_folder, path))

    def package_info(self):
        self.cpp_info.includedirs = []
        # Needed for compatibility with v1.x - Remove when 2.0 becomes the default
        bindir = os.path.join(self.package_folder, "bin")
        self.output.info(f"Appending PATH environment variable: {bindir}")
        self.env_info.PATH.append(bindir)
