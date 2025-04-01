# Tensorflow

## Install requirements

Assuming cuda (v11.6) and cudnn (v8) are installed on a Ubuntu 20.04 system, we
need the following packages for tensorflow:

```sh
apt-get install -y build-essential \
         cmake \
         git \
         wget \
         curl \
         gnupg \
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
         libcanberra-gtk-module
```

Make sure you have a recent version of cmake (`v3.10` and newer). If not,
upgrade through the official repo:

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

## Setup the python environment

```sh
apt-get install python-is-python3
python3 -m pip install pip --upgrade
python3 -m pip install numpy scikit-build
```

## Install Bazel

```sh
curl -fsSL https://bazel.build/bazel-release.pub.gpg | gpg --dearmor > bazel.gpg
mv bazel.gpg /etc/apt/trusted.gpg.d/
echo "deb [arch=amd64] https://storage.googleapis.com/bazel-apt stable jdk1.8" | tee /etc/apt/sources.list.d/bazel.list
apt-get update -y && apt-get install bazel-5.3.0 -y
ln -s /usr/bin/bazel-5.3.0 /usr/bin/bazel
ldconfig
```

## Get and build Protobuf

```sh
mkdir /protocol_buffers
cd /protocol_buffers
wget -c https://github.com/protocolbuffers/protobuf/releases/download/v3.9.2/protobuf-all-3.9.2.tar.gz
tar xvf protobuf-all-3.9.2.tar.gz && cd protobuf-3.9.2/
./configure
make
make install
ldconfig
```

## Build tensorflow

Set some config environment variables:

```sh
export PYTHON_BIN_PATH=/usr/bin/python3.8
export PYTHON_LIB_PATH=/usr/lib/python3/dist-packages
export CUDA_TOOLKIT_PATH=/usr/local/cuda-11.6
export CUDNN_INSTALL_PATH=/usr/lib/x86_64-linux-gnu
export TF_NEED_GCP=0
export TF_NEED_CUDA=1
export TF_CUDA_VERSION=11.6
export TF_CUDA_COMPUTE_CAPABILITIES=7.5
export TF_NEED_HDFS=0
export TF_NEED_OPENCL=0
export TF_NEED_JEMALLOC=1
export TF_ENABLE_XLA=0
export TF_NEED_VERBS=0
export TF_CUDA_CLANG=0
export TF_CUDNN_VERSION=8
export TF_NEED_MKL=0
export TF_DOWNLOAD_MKL=0
export TF_NEED_AWS=0
export TF_NEED_MPI=0
export TF_NEED_GDR=0
export TF_NEED_S3=0
export TF_NEED_OPENCL_SYCL=0
export TF_SET_ANDROID_WORKSPACE=0
export TF_NEED_COMPUTECPP=0
export GCC_HOST_COMPILER_PATH=/usr/bin/gcc
export CC_OPT_FLAGS="-march=native"
export TF_NEED_KAFKA=0
export TF_NEED_TENSORRT=0
```

### Get and compile tensorflow

```sh
git clone https://github.com/tensorflow/tensorflow.git
cd tensorflow
git checkout v2.11.0
./configure
bazel build --local_ram_resources=HOST_RAM*.7 \
            --local_cpu_resources=HOST_CPUS-1 \
            --jobs=4 \
            --config=v2 \
            --copt=-O3 \
            --copt=-m64 \
            --copt=-march=native \
            --config=cuda \
            --verbose_failures \
            //tensorflow:tensorflow_cc \
            //tensorflow:install_headers \
            //tensorflow:tensorflow \
            //tensorflow:tensorflow_framework \
            //tensorflow/c:c_api \
            //tensorflow/tools/lib_package:libtensorflow
mkdir -p /opt/tensorflow/lib
cp -r bazel-bin/tensorflow/* /opt/tensorflow/lib/
cd /opt/tensorflow/lib
ln -s libtensorflow_cc.so.2.11.0 libtensorflow_cc.so
ln -s libtensorflow_cc.so.2.11.0 libtensorflow_cc.so.2
ln -s libtensorflow.so.2.11.0 libtensorflow.so
ln -s libtensorflow.so.2.11.0 libtensorflow.so.2
```

### install TF runtime & libs to some dir in the host

```sh
wget https://raw.githubusercontent.com/tensorflow/tensorflow/master/tensorflow/c/c_api_internal.h \
     -O /opt/tensorflow/lib/include/tensorflow/c/c_api_internal.h
wget https://raw.githubusercontent.com/tensorflow/tensorflow/master/tensorflow/core/framework/op_gen_lib.h \
     -O /opt/tensorflow/lib/include/tensorflow/core/framework/op_gen_lib.h
```
