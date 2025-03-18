import os

from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.files import copy, get, rmdir

required_conan_version = ">=2"

class nsisConan(ConanFile):
    name = "nsis"
    description = "NSIS (Nullsoft Scriptable Install System) is a professional open source system to create Windows installers."
    license = "LicenseRef-NSIS"
    url = "https://github.com/ashley-b/conan-recipes"
    homepage = "https://sourceforge.net/projects/nsis/"
    topics = ("windows", "installer")

    package_type = "application"
    settings = "os", "arch", "compiler", "build_type"

    def package_id(self):
        del self.info.settings.compiler
        del self.info.settings.build_type

    def validate(self):
        if self.settings.arch not in ["x86", "x86_64"]:
            raise ConanInvalidConfiguration("Binaries are only provided for x86 or x86_64 architectures")

        if self.settings.os != "Windows":
            raise ConanInvalidConfiguration(f"Only supports Windows, not {self.settings.os}.")

    def build(self):
        get(self, **self.conan_data["sources"][self.version], filename='nsis.zip')

    def package(self):
        path = os.path.join(self.build_folder, f"nsis-{self.version}")
        self.output.info(f"path: {path}")
        copy(self, pattern="*",
            src=path,
            dst=os.path.join(self.package_folder, "bin"))
        copy(self, "COPYING",
            src=path,
            dst=os.path.join(self.package_folder, "licenses"))

        rmdir(self, os.path.join(self.package_folder, "bin", "Examples"))

    def package_info(self):
        self.cpp_info.includedirs = []
        self.cpp_info.libdirs = []
