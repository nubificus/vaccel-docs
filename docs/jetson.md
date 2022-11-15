# Jetson-inference

vAccel is a hardware acceleration framework, so, in order to use it the system
must have a hardware accelerator and its software stack installed in the Host
OS. To walk through the requirements for running a vAccel-enabled workload with
the jetson-inference plugin, we will use a set of NVIDIA GPUs (RTX 2060 SUPER,
Jetson Nano and Xavier AGX) and a common distribution like Ubuntu. 

The Jetson-inference vAccel plugin is based on
[jetson-inference](https://github.com/dusty-nv/jetson-inference), a frontend
for TensorRT, developed by NVIDIA. This intro section will serve as a guide to
install TensorRT, CUDA and jetson inference on a Ubuntu 20.04 system.

## Install prerequisites

The first step is to prepare the system for building and installing jetson-inference.

### Install common tools

```bash
apt update && TZ=Etc/UTC apt install -y build-essential \
        git \
        cmake \
        python3 \
        python3-venv \
        libpython3-dev \
        python3-numpy \
        gcc-8 \
        g++-8 \
        lsb-release \
        wget \
        software-properties-common && \
```

### Set gcc-8 as the default compiler

```bash
update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-8 8 && \
update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-8 8 && \
update-alternatives --set gcc /usr/bin/gcc-8
```

### setup NVIDIA's custom repositories



```bash
export OS=ubuntu2004
wget http://developer.download.nvidia.com/compute/machine-learning/repos/${OS}/x86_64/nvidia-machine-learning-repo-${OS}_1.0.0-1_amd64.deb
dpkg -i nvidia-machine-learning-repo-${OS}_1.0.0-1_amd64.deb
apt-key adv --fetch-keys http://developer.download.nvidia.com/compute/machine-learning/repos/${OS}/x86_64/7fa2af80.pub
wget https://developer.download.nvidia.com/compute/cuda/repos/${OS}/x86_64/cuda-${OS}.pin
mv cuda-${OS}.pin /etc/apt/preferences.d/cuda-repository-pin-600
apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/${OS}/x86_64/3bf863cc.pub
add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/${OS}/x86_64/ /"
```

### Install NVIDIA CUDA, CUDNN and TENSORRT

```bash
apt-get update
apt-get install -y libcudnn8 libcudnn8-dev tensorrt nvidia-cuda-toolkit
```



## Prepare for building jetson-inference

We clone jetson-inference:

```
git clone --recursive https://github.com/nubificus/jetson-inference
cd jetson-inference
```

## Building jetson-inference

We create a build dir, enter it and prepare the Makefiles:

```
mkdir build
cd build

BUILD_DEPS=YES cmake -DBUILD_INTERACTIVE=NO ../
```

Finally, we issue the build command and we install it to our system:

```
make -j$(nproc)
make install
```
