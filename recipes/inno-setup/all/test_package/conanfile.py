from conan import ConanFile
from conan.tools.files import chdir
from conan.tools.layout import basic_layout

class TestPackageConan(ConanFile):
    settings = "os", "arch", "compiler", "build_type"
    generators = "VirtualBuildEnv"
    test_type = "explicit"

    def layout(self):
        basic_layout(self)

    def build_requirements(self):
        self.tool_requires(self.tested_reference_str)

    def test(self):
        with chdir(self, self.source_folder):
            self.run(f"ISCC.exe /O{self.build_folder} test.iss")
