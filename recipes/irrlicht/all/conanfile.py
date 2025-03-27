import os

from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.files import copy, chdir, get
from conan.tools.gnu import Autotools, AutotoolsToolchain
from conan.tools.layout import basic_layout
from conan.tools.microsoft import is_msvc

required_conan_version = ">=2"

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
    implements = ["auto_shared_fpic"]

    def layout(self):
        basic_layout(self, src_folder="src")

    def validate(self):
        if is_msvc(self):
            raise ConanInvalidConfiguration("MSVC is not supported")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def requirements(self):
        self.requires('libjpeg/9e')
        self.requires('libpng/1.6.40')
        self.requires('opengl/system')
        if self.settings.os in ["Linux", "FreeBSD"]:
            self.requires('xorg/system')
        self.requires('zlib/1.3')

    def generate(self):
        tc = AutotoolsToolchain(self)
        tc.generate()

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
