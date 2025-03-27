import os
from conan import ConanFile
from conan.tools.layout import basic_layout
from conan.tools.build import can_run


class TestPackageConan(ConanFile):
    settings = "os", "arch"
    generators = "VirtualRunEnv"
    test_type = "explicit"

    def layout(self):
        basic_layout(self)

    def requirements(self):
        self.requires(self.tested_reference_str)

    def test(self):
        if can_run(self):
            src_file = os.path.join(self.source_folder, 'eeprom_settings.txt')
            bin_file = os.path.join(self.build_folder, 'eeprom_settings.bin')
            dump_file = os.path.join(self.build_folder, 'eeprom_settings.dump')
            self.run(f'eepmake {src_file} {bin_file}', env="conanrun")
            self.run(f'eepdump {bin_file} {dump_file}', env="conanrun")
