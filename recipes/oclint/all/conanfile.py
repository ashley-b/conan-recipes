import os

from conan import ConanFile
from conan.tools.layout import basic_layout
from conan.tools.files import copy, chdir, get


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

    def generate(self):
        pass

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
