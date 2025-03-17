import os

from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.build import cross_building
from conan.tools.env import Environment, VirtualBuildEnv
from conan.tools.files import copy, chdir, get
from conan.tools.gnu import Autotools, AutotoolsToolchain
from conan.tools.layout import basic_layout
from conan.tools.microsoft import is_msvc, unix_path

required_conan_version = ">=1.50.0"

class IrrlichtConan(ConanFile):
    name = "irrlicht"
    license = "Irrlicht"
    homepage = "https://irrlicht.sourceforge.io/"
    url = "https://github.com/ashley-b/conan-recipes"
    description = "The Irrlicht Engine is an open source high performance realtime 3D engine written and usable in C++. It is completely cross-platform, using D3D, OpenGL and its own software renderers."
    topics = ("d3d", "opengl")
    package_type = "library"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
    }

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def layout(self):
        basic_layout(self, src_folder="src")

    def validate(self):
        if cross_building(self):
            raise ConanInvalidConfiguration(f"{self.name} Cross building is not yet supported. Contributions are welcome")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def build_requirements(self):
        if self.settings_build.os == "Windows":
            self.win_bash = True
            if not self.conf.get("tools.microsoft.bash:path", check_type=str):
                self.tool_requires("msys2/cci.latest")
        if is_msvc(self):
            self.tool_requires("automake/1.16.5")

    def requirements(self):
        self.requires('libjpeg/9e')
        self.requires('libpng/1.6.40')
        self.requires('opengl/system')
        if self.settings.os in ["Linux", "FreeBSD"]:
            self.requires('xorg/system')
        self.requires('zlib/1.3')

    def generate(self):
        venv = VirtualBuildEnv(self)
        venv.generate()
    
        tc = AutotoolsToolchain(self)
        if is_msvc(self):
            tc.extra_cflags.append("-FS")
            tc.extra_cxxflags.append("-FS")
        tc.generate()

        if is_msvc(self):
            env = Environment()
            automake_conf = self.dependencies.build["automake"].conf_info
            compile_wrapper = unix_path(self, automake_conf.get("user.automake:compile-wrapper", check_type=str))
            ar_wrapper = unix_path(self, automake_conf.get("user.automake:lib-wrapper", check_type=str))
            env.define("CC", f"{compile_wrapper} cl -nologo")
            env.define("CXX", f"{compile_wrapper} cl -nologo")
            env.define("LD", "link -nologo")
            env.define("AR", f"{ar_wrapper} lib")
            env.define("NM", "dumpbin -symbols")
            env.define("OBJDUMP", ":")
            env.define("RANLIB", ":")
            env.define("STRIP", ":")
            env.vars(self).save_script("conanbuild_msvc")

    def build(self):
        with chdir(self, os.path.join(self.source_folder, 'source', 'Irrlicht')):
            autotools = Autotools(self)
            target = 'sharedlib' if self.options.shared else ''
            args = ['NDEBUG=1' if not self.settings.build_type=='Debug' else '']
            autotools.make(target=target, args=args)

    def package(self):
        copy(self, "irrlicht-license.txt", src=os.path.join(self.source_folder, "doc"), dst=os.path.join(self.package_folder, "licenses"), keep_path=False)
        copy(self, "*", src=os.path.join(self.source_folder, 'include'), dst=os.path.join(self.package_folder, "include"))
        for pattern in ["*.so*", "*.dylib", "*.lib", "*.a"]:
            copy(self, pattern,
                 src=os.path.join(self.source_folder, 'source', 'Irrlicht'),
                 dst=os.path.join(self.package_folder, "lib"),
                 keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["Irrlicht"]
