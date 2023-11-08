# Conan rpi eepromutils

## Description

Simple Conan recipe for https://www.github.com/raspberrypi/hats

Which is a collection of tools for writing, reading and flashing raspberry pi HAT EEPROM's

* eepmake
* eepdump
* eepflash.sh

## Build and package

The following command will build and publish the Conan package to the local system cache:

```
conan create . 1.0-2022-11-11@
```

## Useage

### Standalone
```
conan install -g VirtualRunEnv rpi_eepromutils/1.0-2022-11-11@
```
**OR**
### Example conanfile.txt for consumers
```
[build_requires]
rpi_eepromutils/1.0-2022-11-11

[generators]
VirtualRunEnv
```
### Running commands directly
```sh
$ source conanrun.sh
$ sudo eepflash.sh -d=0 -t=24c256 -w -f=hat.eep
$ source deactivate_conanrun.sh
```
