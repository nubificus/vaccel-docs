# Jetson-inference

vAccel is a hardware acceleration framework, so, in order to use it the system
must have a hardware accelerator and its software stack installed in the Host
OS. To walk through the requirements for running a vAccel-enabled workload with
the jetson-inference plugin, we will use a set of NVIDIA GPUs (GTX 1030,
RTX 2060 and a Tesla T4) and a common distribution like Ubuntu. 

The Jetson-inference vAccel plugin is based on
[jetson-inference](https://github.com/), a frontend for TensorRT, developed by
NVIDIA. This intro section will serve as a guide to install TensorRT, CUDA and
jetson inference on a Ubuntu 18.04 system.

## Setup NVIDIA custom repos

The first step is to prepare the package system for NVIDIA's custom repos:

```
# install common utils & get NVIDIA's key
apt-get update && apt-get install -y --no-install-recommends gnupg2 curl ca-certificates wget sudo
curl -fsSL https://developer.download.nvidia.com/compute/cuda/repos/${os}/x86_64/7fa2af80.pub | apt-key add -

# download repo pkgs and install them
wget https://developer.download.nvidia.com/compute/cuda/repos/${os}/x86_64/cuda-repo-${os}_${cuda}-1_amd64.deb
wget https://developer.download.nvidia.com/compute/machine-learning/repos/${os}/x86_64/nvidia-machine-learning-repo-${os}_1.0.0-1_amd64.deb
dpkg -i cuda-repo-*.deb
dpkg -i nvidia-machine-learning-repo-*.deb

# update pkg list
apt-get update
```

## Install CUDA and TensorRT

Next, we need to install CUDA and TensorRT:

```
# install TensorRT
DEBIAN_FRONTEND=noninteractive apt-get install -yy eatmydata && \
	DEBIAN_FRONTEND=noninteractive eatmydata apt-get install -y cuda-11-1 libnvinfer7 libnvonnxparsers7 libnvparsers7 libnvinfer-plugin7
```

## Prepare for building jetson-inference

Following the successful installation of TensorRT, we need to install the requirements for the jetson-inference build system:

```
apt-get update && apt-get install -y git \
	libnvinfer-dev \
	libnvinfer-plugin-dev \
	libpython3-dev \
	pkg-config \
	python3-libnvinfer-dev \
	python3-numpy
```

Finally, we clone jetson-inference:

```
git clone --recursive https://github.com/nubificus/jetson-inference
cd jetson-inference
```

## Patch to support GTX 1030 & RTX 2060

To support GTX 1030 and RTX 2060 we need to patch the source tree to add the relevant compute versions (`Enable-CM-60-75.patch`):


```
diff --git a/CMakeLists.txt b/CMakeLists.txt
index 46c997dd..d4c3a56c 100644
--- a/CMakeLists.txt
+++ b/CMakeLists.txt
@@ -60,16 +60,18 @@ set(
        ${CUDA_NVCC_FLAGS}; 
     -O3 
        -gencode arch=compute_53,code=sm_53
+       -gencode arch=compute_60,code=sm_60
        -gencode arch=compute_62,code=sm_62
 )
 
 if(CUDA_VERSION_MAJOR GREATER 9)
-       message("-- CUDA ${CUDA_VERSION_MAJOR} detected, enabling SM_72")
+       message("-- CUDA ${CUDA_VERSION_MAJOR} detected, enabling SM_72 and SM75")
 
        set(
                CUDA_NVCC_FLAGS
                ${CUDA_NVCC_FLAGS}; 
                -gencode arch=compute_72,code=sm_72
+               -gencode arch=compute_75,code=sm_75
        )
 endif()
```

```
patch -p1 < Enable-CM-60-75.patch
```

Then, let's make sure we have a proper compiler & Cmake installed:

```
TZ=Europe/London 
ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
apt-get install -y cmake build-essential
```

Jetson-inference assumes CUDA is installed in /usr/local/cuda. There is a
possibility that cuda will be installed in a folder using the version numbering
so to make sure the build system can find it we do the following:

```
ln -sf /usr/local/cuda-11.1 /usr/local/cuda
```

## Building jetson-inference

We create a build dir, enter it prepare the Makefiles:
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
