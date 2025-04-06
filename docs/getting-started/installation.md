# Installation

vAccel provides prebuilt binaries for Ubuntu-based systems. If you want to use
it with other distributions or build it manually you can follow
[Building from source](#building-from-source).

## Binaries

You can get the latest vAccel binary release from the
[Releases](https://github.com/nubificus/vaccel/releases) page of the
[vAccel repository](https://github.com/nubificus/vaccel). Releases include DEB
packages and binaries for x86_64/aarch64/armv7l Ubuntu-based systems.

### Requirements

The prebuilt vAccel binaries depend on [libcurl](https://curl.se/libcurl/). You
can install it with:

```sh
sudo apt install libcurl4
```

### DEB

To install the DEB package of the latest vAccel release:

/// tab | x86

```sh
wget https://github.com/nubificus/vaccel/releases/download/v[[ versions.vaccel ]]/vaccel_[[ versions.vaccel ]]-1_amd64.deb
sudo dpkg -i vaccel_[[ versions.vaccel ]]-1_amd64.deb
```

///

/// tab | ARM (64-bit)

```sh
wget https://github.com/nubificus/vaccel/releases/download/v[[ versions.vaccel ]]/vaccel_[[ versions.vaccel ]]-1_arm64.deb
sudo dpkg -i vaccel_[[ versions.vaccel ]]-1_arm64.deb
```

///

/// tab | ARM (32-bit)

```sh
wget https://github.com/nubificus/vaccel/releases/download/v[[ versions.vaccel ]]/vaccel_[[ versions.vaccel ]]-1_armhf.deb
sudo dpkg -i vaccel_[[ versions.vaccel ]]-1_armhf.deb
```

///

### TAR

To install the TAR binary package of the latest vAccel release:

/// tab | x86

```sh
wget https://github.com/nubificus/vaccel/releases/download/v[[ versions.vaccel ]]/vaccel_[[ versions.vaccel ]]_amd64.tar.gz
# Replace '/usr/local' below with the desired installation prefix
tar xfv vaccel_[[ versions.vaccel ]]_amd64.tar.gz --strip-components=2 -C /usr/local
```

///

/// tab | ARM (64-bit)

```sh
wget https://github.com/nubificus/vaccel/releases/download/v[[ versions.vaccel ]]/vaccel_[[ versions.vaccel ]]_arm64.tar.gz
# Replace '/usr/local' below with the desired installation prefix
tar xfv vaccel_[[ versions.vaccel ]]_arm64.tar.gz --strip-components=2 -C /usr/local
```

///

/// tab | ARM (32-bit)

```sh
wget https://github.com/nubificus/vaccel/releases/download/v[[ versions.vaccel ]]/vaccel_[[ versions.vaccel ]]_armhf.tar.gz
# Replace '/usr/local' below with the desired installation prefix
tar xfv vaccel_[[ versions.vaccel ]]_armhf.tar.gz --strip-components=2 -C /usr/local
```

///

### Latest artifacts

You can also find prebuilt artifacts of the latest vAccel revision at:

/// tab | x86

```sh
# DEB
https://s3.nbfc.io/nbfc-assets/github/vaccel/rev/main/x86_64/debug/vaccel_latest_amd64.deb
# TAR
https://s3.nbfc.io/nbfc-assets/github/vaccel/rev/main/x86_64/debug/vaccel-latest-bin.tar.gz
```

///

/// tab | ARM (64-bit)

```sh
# DEB
https://s3.nbfc.io/nbfc-assets/github/vaccel/rev/main/aarch64/debug/vaccel_latest_arm64.deb
# TAR
https://s3.nbfc.io/nbfc-assets/github/vaccel/rev/main/aarch64/debug/vaccel-latest-bin.tar.gz
```

///

/// tab | ARM (32-bit)

```sh
# DEB
https://s3.nbfc.io/nbfc-assets/github/vaccel/rev/main/armv7l/debug/vaccel_latest_armhf.deb
# TAR
https://s3.nbfc.io/nbfc-assets/github/vaccel/rev/main/armv7l/debug/vaccel-latest-bin.tar.gz
```

///

## Building from source

### Requirements

vAccel uses the [Meson](https://mesonbuild.com/) build system and this is the
main required dependency to build it. In Debian-based systems, you can install
the required build tools with:

```sh
sudo apt install build-essential ninja-build pkg-config python3-pip
pip install meson
```

Optionally, to support file downloading you need the
[libcurl](https://curl.se/libcurl/) development files:

```sh
sudo apt install libcurl4-openssl-dev
```

To get working image inference examples you also need the
[stb](https://github.com/nothings/stb) header library:

```sh
sudo apt install libstb-dev
```

### Building the source code

Get the source code:

```sh
git clone https://github.com/nubificus/vaccel
cd vaccel
```

Build and install all vAccel components in the repository with:

```sh
# Configure the build directory.
# Enable all features and set build type to 'release'.
meson setup --buildtype=release -Dauto_features=enabled build

# Compile the project
meson compile -C build

# Install the project to the default directory (/usr/local)
meson install -C build
```

And you are set to go.

If you want to select which components to build instead, you can continue
reading below.

#### Building the core library

The core library is the only component built by default. To only build the core
library replace:

```sh
meson setup --buildtype=release -Dauto_features=enabled build
```

above, with:

```sh
meson setup --buildtype=release build
```

#### Building the plugins

Building of the included plugins is disabled, by default. You can enable
building one or more plugins at configuration time by setting the corresponding
options.

To build the core library and all of the included plugins, replace:

```sh
meson setup --buildtype=release -Dauto_features=enabled build
```

above, with:

```sh
meson setup --buildtype=release -Dplugins=enabled build
```

You can also select which plugins to use. For example:

```sh
meson setup --buildtype=release -Dplugin-noop=enabled build
```

will select the core library and the noop backend plugin.

#### Building the examples

As with the plugins, building the examples is disabled by default. To build the
core library and all of the examples, replace:

```sh
meson setup --buildtype=release -Dauto_features=enabled build
```

above, with:

```sh
meson setup --buildtype=release -Dexamples=enabled build
```

To view all the available options/values you can use:

```sh
meson setup --buildtype=release build
meson configure build
```

vAccel specific options can be found in the `Project Options` section.
