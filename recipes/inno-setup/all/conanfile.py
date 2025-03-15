import os

from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.files import copy, download, rmdir

required_conan_version = ">=2"

class innosetupConan(ConanFile):
    name = "inno-setup"
    description = "Inno Setup is a free installer for Windows programs by Jordan Russell and Martijn Laan"
    license = "LicenseRef-InnoSetup"
    url = "https://github.com/ashley-b/conan-recipes"
    homepage = "https://jrsoftware.org/isinfo.php"
    topics = ("windows", "installer")

    package_type = "application"
    settings = "os", "arch", "compiler", "build_type"

    @property
    def _installer_file_name(self):
        return "is.exe"

    def package_id(self):
        del self.info.settings.compiler
        del self.info.settings.build_type

    def validate(self):
        if self.settings.arch not in ["x86", "x86_64"]:
            raise ConanInvalidConfiguration(f"{self.name} binaries are only provided for x86 or x86_64 architectures")

        if self.settings.os != "Windows":
            raise ConanInvalidConfiguration(f"{self.name} only supports Windows")

    def build(self):
        download(self, **self.conan_data["sources"][self.version], filename=self._installer_file_name)

        installer_path = os.path.join(self.build_folder, self._installer_file_name)
        self.run(f"{installer_path} /SP- /PORTABLE=1 /CURRENTUSER /NOICONS /VERYSILENT /SUPPRESSMSGBOXES /DIR={os.path.join(self.build_folder, "bin")}")

    def package(self):
        copy(self, pattern="*",
            src=os.path.join(self.build_folder, "bin"),
            dst=os.path.join(self.package_folder, "bin"))
        copy(self, "license.txt",
            src=os.path.join(self.build_folder, "bin"),
            dst=os.path.join(self.package_folder, "licenses"))

        rmdir(self, os.path.join(self.package_folder, "bin", "Examples"))

    def package_info(self):
        self.cpp_info.includedirs = []
        self.cpp_info.libdirs = []
