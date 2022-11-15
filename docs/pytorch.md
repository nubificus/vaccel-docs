## Get & Build the torch C/C++ API files
```shell
git clone --recursive https://github.com/pytorch/pytorch
cd pytorch
git submodule sync
git submodule update --init --recursive --jobs 8

# Optional, if CUDA is enable
export CMAKE_PREFIX_PATH=${CONDA_PREFIX:-"$(dirname $(which conda))/../"}

# Run the setup, should take some times
python setup.py install
```

## Install Torch runtime & libs to some dir in the host. Should put the libtorch inside the `/opt/torch` (same with the libtorch_cuda). 
```shell
mkdir /opt

# Get the CPU-Only libtorch for testing
wget https://download.pytorch.org/libtorch/nightly/cpu/libtorch-shared-with-deps-latest.zip
unzip libtorch-shared-with-deps-latest.zip

# Download the CUDA version
wget https://download.pytorch.org/libtorch/cu116/libtorch-shared-with-deps-1.12.1%2Bcu116.zip
unzip libtorch-shared-with-deps-1.12.1+cu116.zip

mv libtorch torch
sudo mv torch /opt/
```

## Path setting [WiP]
```shell
mkdir -p /opt/torch/lib
cp -r ~./pytorch/* /opt/torch/lib/

LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
LD_LIBRARY_PATH=/opt/tensorflow/lib:$LD_LIBRARY_PATH
ldconfig
```

