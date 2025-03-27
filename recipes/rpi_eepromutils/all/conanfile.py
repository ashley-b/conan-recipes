import os

from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.files import copy, chdir, get
from conan.tools.gnu import Autotools, AutotoolsToolchain
from conan.tools.layout import basic_layout

required_conan_version = ">=2.4"

class RpiEepromutilsConan(ConanFile):
    name = "rpi_eepromutils"
    license = "BSD-3-Clause"
    homepage = "https://github.com/raspberrypi/hats"
    url = "https://github.com/ashley-b/conan-recipes"
    description = "Utilities to create, flash and dump HAT EEPROM images"
    topics = ("eeprom", "rpi")
    package_type = "application"
    settings = "os", "compiler", "build_type", "arch"
    languages = "C"
    deprecated = True

    @property
    def _app_root_dir(self):
        return os.path.join(self.source_folder, 'eepromutils')

    def validate(self):
        if self.info.settings.os != "Linux":
            raise ConanInvalidConfiguration("Only Linux supported")

    def layout(self):
        basic_layout(self, src_folder="src")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        tc = AutotoolsToolchain(self)
        tc.generate()

    def build(self):
        with chdir(self, self._app_root_dir):
            autotools = Autotools(self)
            autotools.make()

    def package(self):
        copy(self, "LICENCE", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses"), keep_path=False)
        bin_dir = os.path.join(self.package_folder, "bin")
        copy(self, "eepmake", src=self._app_root_dir, dst=bin_dir)
        copy(self, "eepdump", src=self._app_root_dir, dst=bin_dir)
        copy(self, "eepflash.sh", src=self._app_root_dir, dst=bin_dir)

    def package_info(self):
        self.cpp_info.includedirs = []
        self.cpp_info.libdirs = []
