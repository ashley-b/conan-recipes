# Conan Recipes

A collection of Conan 2 recipes which are missing from [conan-center-index](https://github.com/conan-io/conan-center-index)

The structure of this repository is design to work with Conan [Local Recipes Index Repository](https://docs.conan.io/2/devops/devops_local_recipes_index.html) feature

## Usage

1. Git clone this repository
   ```
   git clone https://github.com/ashley-b/conan-recipes/
   ```
2. Add the repository to conan as a local recipes index with the following command. `name_of_remote` can be replaced with a name of your choosing
   ```
   conan remote add name_of_remote ./path/to/conan-recipes
   ```

## Recipes

Recipe | Project name | Description |
| --- | --- | --- |
| inno-setup      | Inno Setup      | A free installer for Windows programs. |
| irrlicht        | Irrlicht        | The Irrlicht Engine is an open source high performance realtime 3D engine written and usable in C++. It is completely cross-platform, using D3D, OpenGL and its own software renderers. |
| nsis            | Nullsoft Scriptable Install System | NSIS (Nullsoft Scriptable Install System) is a professional open source system to create Windows installers. |
| qmdnsengine | QMdnsEngine | Multicast DNS library for Qt applications
| rpi_eepromutils | Raspberry Pi eepromutils | Utilities to create, flash and dump HAT EEPROM images |

## License

All the Conan recipes in this repository are distributed under the MIT license. There are other files, like patches or examples used to test the packages, that could use different licenses, for those files specific license and credit must be checked in the file itself.
