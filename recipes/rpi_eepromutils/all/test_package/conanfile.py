from six import StringIO
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
            apps = [
                (
                    "eepmake",
                    "Wrong input format.\n"
                    "Try 'eepmake input_file output_file [dt_file] [-c custom_file_1 ... custom_file_n]'"
                ),
                (
                    "eepdump",
                    "Wrong input format.\n"
                    "Try 'eepdump input_file output_file'"
                )
            ]
            for cmd in apps:
                output = StringIO()
                self.run(cmd[0], output, ignore_errors=True, env="conanrun")
                output_str = str(output.getvalue())
                self.output.info("Output:\n{}".format(output_str))
                assert(cmd[1] in output_str)
