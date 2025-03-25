# Build and Install TVM

Official instructions for building and installing [TVM](https://tvm.apache.org)
can be found [here](https://tvm.apache.org/docs/install/from_source.html).

In the sections below we provide a short version that can be used to build and
install TVM C/C++ API files for use with vAccel.

## Install dependencies

Install the required dependencies:

```sh
sudo apt update && sudo apt install -y cmake git python3 python3-pip \
    libtinfo-dev zlib1g-dev libedit-dev

# Optional, for CUDA builds
sudo apt install libllvm15 and libllvm15-dev
```

## Build TVM C/C++ API files

Clone the repo, adjusting `TVM_VERSION` to the desired version:

```sh
TVM_VERSION="v0.19.0"
git clone https://github.com/apache/tvm --depth 1 --recursive \
    -b "${TVM_VERSION}"
cd tvm
```

Build source code and install:

```sh
# Replace this with the desired installation directory
cd /opt

# Configure build
cmake -S . -B build
cp cmake/config.cmake build/
echo >> build/config.cmake
echo "set(CMAKE_BUILD_TYPE RelWithDebInfo)" >> build/config.cmake
echo "set(USE_LLVM \"llvm-config --ignore-libllvm --link-static\")" \
    >> build/config.cmake
echo "set(HIDE_PRIVATE_SYMBOLS ON)" >> build/config.cmake

# Optionally, enable CUDA
echo "set(USE_CUDA   ON)" >> build/config.cmake

# Build C/C++ files
cmake --build build --parallel "$(nproc)"

# Install python files
export TVM_LIBRARY_PATH=/opt/tvm/build
pip install -e /opt/tvm/python
```

For convenience, the TVM library path can be added to system paths:

```sh
echo "/opt/tvm/build" >> /etc/ld.so.conf.d/tvm.conf
ldconfig
```
