VERSION 0.8

fedora:
    FROM registry.fedoraproject.org/fedora:39
    RUN dnf install --setopt=install_weak_deps=False --yes pipx cmake make gcc gcc-c++ 

debain:
    FROM docker.io/library/debian:bookworm
    RUN apt update && apt install --no-install-recommends and --no-install-suggests --yes cmake make pipx gcc g++

deps:
    ARG dist
    FROM +$dist
    ENV PATH="${PATH}:/root/.local/bin"
    RUN pwd
    RUN pipx install conan
    RUN conan profile detect

conan-setup:
    ARG dist
    FROM +deps --dist=$dist
    WORKDIR work
    RUN mkdir conan_local
    COPY recipes/ conan_local/recipes/
    RUN conan remote add local conan_local/

build-test:
    ARG dist
    ARG package
    FROM +conan-setup --dist=$dist
    RUN conan remote list
    RUN mkdir test && cd test && conan install --build missing -c tools.system.package_manager:mode=install --requires $package

build-test-all-dist:
    ARG package
    FROM +build-test --dist=fedora --dist=debain

build-test-all:
    FROM +build-test-all-dist --package=irrcht/1.8.5 --package=rpi_eepromutils/1.0-2022-11-11 --package=oclint/22.02
#    BUILD +build-test-all-dist --package=irrlicht/1.8.5
#    BUILD +build-test-all-dist --package=rpi_eepromutils/1.0-2022-11-11
#    BUILD +build-test-all-dist --package=oclint/22.02