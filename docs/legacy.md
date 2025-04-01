# Build and Install using CMake

Here are the instructions using the old legacy version of building, vaccel -
using CMake. Do note that these instructions may be out of date and it is
recommended to use Meson where possible.

## Prerequisites

In Ubuntu-based systems, you need to have the following packages to build
`vaccelrt`:

- cmake
- build-essential

You can install them using the following command:

```bash
sudo apt-get install -y cmake build-essential
```

## Get the source code

Get the source code for **vaccelrt**:

```bash
git clone https://github.com/cloudkernels/vaccelrt --recursive
```

## Build and install vaccelrt

Build vaccelrt and install it in `/usr/local`:

```bash
cd vaccelrt
mkdir build
cd build
cmake ../ -DCMAKE_INSTALL_PREFIX=/usr/local -DBUILD_PLUGIN_NOOP=ON -DBUILD_EXAMPLES=ON -DCMAKE_BUILD_TYPE=Release
make
make install
```
