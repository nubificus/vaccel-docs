# Build and Install PyTorch

Official instructions for building and installing [PyTorch](https://pytorch.org)
can be found [here](https://github.com/pytorch/pytorch#installation).

In the sections below we provide a short version that can be used to build and
install PyTorch C++ API files (LibTorch) for use with vAccel. We assume that the
required dependencies are already installed.

## Build PyTorch C++ API files (LibTorch)

Clone the PyTorch repo, adjusting `TORCH_VERSION` to the desired version:

```sh
TORCH_VERSION=2.6.0
git clone https://github.com/pytorch/pytorch --depth 1 --recursive \
    -b "${TORCH_VERSION}"
cd pytorch
```

Build the source code:

```sh
export _GLIBCXX_USE_CXX11_ABI=1
# If CUDA dependencies are installed set this to `1` for CUDA support
export USE_CUDA=0

cmake -S . -B build
cmake --build build --parallel "$(nproc)"
```

and install the binaries:

```sh
cmake --install build --prefix=/usr/local
```

## [Alternative] Install pre-built PyTorch C++ API files (LibTorch)

PyTorch provides pre-built binaries for LibTorch. Ie. for version 2.6.0:

Download and extract CPU-only binaries:

```sh
wget https://download.pytorch.org/libtorch/cpu/libtorch-cxx11-abi-shared-with-deps-2.6.0%2Bcpu.zip
unzip libtorch-cxx11-abi-shared-with-deps-2.6.0+cpu.zip
```

or download and extract binaries with CUDA support (here for CUDA 11.8):

```sh
wget https://download.pytorch.org/libtorch/cu118/libtorch-cxx11-abi-shared-with-deps-2.6.0%2Bcu118.zip
unzip libtorch-cxx11-abi-shared-with-deps-2.6.0+cu118.zip
```

and move files to the desired installation directory:

```sh
sudo mv libtorch /opt/torch
```
