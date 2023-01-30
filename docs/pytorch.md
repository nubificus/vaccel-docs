
### Install requirements

Assuming cuda (v11.6) and cudnn (v8) are installed on a Ubuntu 20.04 system, we need the following packages for pytorch:

```sh
apt-get install -y build-essential \
         cmake \
         git \
         wget \
         vim \
         software-properties-common \
         libatlas-base-dev \
         libleveldb-dev \
         libsnappy-dev \
         libhdf5-serial-dev \
         libboost-all-dev \
         libgflags-dev \
         libgoogle-glog-dev \
         liblmdb-dev \
         pciutils \
         python3-setuptools \
         python3-dev \
         python3-pip \
         opencl-headers \
         ocl-icd-opencl-dev \
         libviennacl-dev \
	 unzip \
	 libcanberra-gtk-module
```

Make sure you have a recent version of cmake (`v3.10` and newer). If not, upgrade through the official repo:

```sh
wget -qO - https://apt.kitware.com/keys/kitware-archive-latest.asc | apt-key add - && \
    apt-add-repository 'deb https://apt.kitware.com/ubuntu/ bionic main' && \
    apt update -y && \
    apt install cmake --upgrade -y
```

Optionally install OpenCV python bindings:

```sh
apt-get install -y libopencv-dev python3-opencv
```

### Setup the python environment

```sh
apt-get install python-is-python3
python3 -m pip install pip --upgrade
python3 -m pip install numpy scikit-build
```

### Get pytorch shared libraries

Get the shared libraries needed:

```sh
# Get the CPU-Only libtorch for testing
wget https://download.pytorch.org/libtorch/nightly/cpu/libtorch-shared-with-deps-latest.zip
unzip libtorch-shared-with-deps-latest.zip

# or Download the CUDA version
wget https://download.pytorch.org/libtorch/cu116/libtorch-shared-with-deps-1.12.1%2Bcu116.zip
unzip libtorch-shared-with-deps-1.12.1+cu116.zip

mv libtorch torch
sudo mv torch /opt/
```

