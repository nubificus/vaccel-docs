# Build & Install from source using CMake (deprecated)

vAccel provides an alternate way of building from source using CMake. Do note
that this method is deprecared and these instructions may be out of date. It is
recommended to use Meson instead.

## Prerequisites

In Ubuntu-based systems, you need to have the following packages to build
`vaccel`:

- cmake
- build-essential

You can install them using the following command:

```bash
sudo apt-get install -y cmake build-essential
```

## Get the source code

Get the source code for **vaccel**:

```bash
git clone https://github.com/nubificus/vaccel --recursive
```

## Build and install the core runtime library

Build vaccel and install it in `/usr/local`:

```bash
cd vaccel
mkdir build
cd build
cmake ../ -DCMAKE_INSTALL_PREFIX=/usr/local -DCMAKE_BUILD_TYPE=Release
make
make install
```

## Build the plugins

Building the plugins is disabled by default. You can enable building one or more
plugins at configuration time of CMake by setting the corresponding variable of
the following table to `ON`

| Backend Plugin | Variable          | Default |
| -------------- | ----------------- | ------- |
| noop           | BUILD_PLUGIN_NOOP | `OFF`   |
| exec           | BUILD_PLUGIN_EXEC | `OFF`   |

For example:

```bash
cmake -DBUILD_PLUGIN_NOOP=ON ..
```

will enable building the noop backend plugin.

## Build the examples

To build the examples included with vaccel you can use:

```bash
cmake -DBUILD_EXAMPLES=ON ..
make
```
