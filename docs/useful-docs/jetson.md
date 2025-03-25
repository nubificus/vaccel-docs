# Build and Install Jetson-inference

To walk through the requirements for running a vAccel-enabled workload with the
jetson-inference plugin, we will use a set of NVIDIA GPUs (RTX 2060 SUPER,
Jetson Nano and Xavier AGX) and a common distribution like Ubuntu.

The Jetson-inference vAccel plugin is based on
[jetson-inference](https://github.com/dusty-nv/jetson-inference), a frontend for
TensorRT, developed by NVIDIA. This intro section will serve as a guide to
install TensorRT, CUDA and jetson inference on a Ubuntu 20.04 system.

## Install prerequisites

The first step is to prepare the system for building and installing
jetson-inference.

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

```bash
git clone --recursive https://github.com/nubificus/jetson-inference
cd jetson-inference
```

## Build and install jetson-inference

We create a build dir, enter it and prepare the Makefiles:

```bash
mkdir build
cd build

BUILD_DEPS=YES cmake -DBUILD_INTERACTIVE=NO ../
```

Finally, we issue the build command and we install it to our system:

```bash
make -j$(nproc)
make install
```

**Note**: _For `aarch64` hosts, this process is slightly different (one would
say easier!) as it assumes the Host system is a `L4T` distro. Just clone the
repo and follow the
[Build & install](jetson.md#build-and-install-jetson-inference) step_

## Build a jetson-inference container image

We use a container file to capture the individual steps to install jetson
inference. Assuming the host is debian-based (we tried that on Ubuntu 20.04),
and has a recent NVIDIA driver (`520.61.05`) we follow the steps below:

- clone the container repo:

```bash
git clone https://github.com/nubificus/jetson-inference-container
```

- build the container image:

```bash
docker build -t nubificus/jetson-inference-updated:x86_64 -f Dockerfile .
```

or just get the one we've built (could take some time, i'ts 12GB...):

```bash
docker pull nubificus/jetson-inference-updated:x86_64
```

- run the `jetson-inference` example:

Run the container:

```bash
# docker run --gpus all --rm -it -v/data/code:/data/code -w $PWD nubificus/jetson-inference-updated:x86_64 /bin/bash
root@9f5224cb28cc:/data/code#
```

Use pre-installed example images and models to do image inference:

```console
root@9f5224cb28cc:/data/code# ln -s /usr/local/data/images .
root@9f5224cb28cc:/data/code# ln -s /usr/local/data/networks .

root@9f5224cb28cc:/data/code# imagenet-console images/dog_0.jpg
[video]  created imageLoader from file:///data/code/images/dog_0.jpg
------------------------------------------------
imageLoader video options:
------------------------------------------------
  -- URI: file:///data/code/images/dog_0.jpg
     - protocol:  file
     - location:  images/dog_0.jpg
     - extension: jpg
  -- deviceType: file
  -- ioType:     input
  -- codec:      unknown
  -- width:      0
  -- height:     0
  -- frameRate:  0.000000
  -- bitRate:    0
  -- numBuffers: 4
  -- zeroCopy:   true
  -- flipMethod: none
  -- loop:       0
  -- rtspLatency 2000
------------------------------------------------
[video]  videoOptions -- failed to parse output resource URI (null)
[video]  videoOutput -- failed to parse command line options
imagenet:  failed to create output stream

imageNet -- loading classification network model from:
         -- prototxt     networks/googlenet.prototxt
         -- model        networks/bvlc_googlenet.caffemodel
         -- class_labels networks/ilsvrc12_synset_words.txt
         -- input_blob   'data'
         -- output_blob  'prob'
         -- batch_size   1

[TRT]    TensorRT version 8.5.1
[TRT]    loading NVIDIA plugins...
[TRT]    Registered plugin creator - ::BatchedNMSDynamic_TRT version 1
[TRT]    Registered plugin creator - ::BatchedNMS_TRT version 1
[TRT]    Registered plugin creator - ::BatchTilePlugin_TRT version 1
[TRT]    Registered plugin creator - ::Clip_TRT version 1
[TRT]    Registered plugin creator - ::CoordConvAC version 1
[TRT]    Registered plugin creator - ::CropAndResizeDynamic version 1
[TRT]    Registered plugin creator - ::CropAndResize version 1
[TRT]    Registered plugin creator - ::DecodeBbox3DPlugin version 1
[TRT]    Registered plugin creator - ::DetectionLayer_TRT version 1
[TRT]    Registered plugin creator - ::EfficientNMS_Explicit_TF_TRT version 1
[TRT]    Registered plugin creator - ::EfficientNMS_Implicit_TF_TRT version 1
[TRT]    Registered plugin creator - ::EfficientNMS_ONNX_TRT version 1
[TRT]    Registered plugin creator - ::EfficientNMS_TRT version 1
[TRT]    Could not register plugin creator -  ::FlattenConcat_TRT version 1
[TRT]    Registered plugin creator - ::GenerateDetection_TRT version 1
[TRT]    Registered plugin creator - ::GridAnchor_TRT version 1
[TRT]    Registered plugin creator - ::GridAnchorRect_TRT version 1
[TRT]    Registered plugin creator - ::InstanceNormalization_TRT version 1
[TRT]    Registered plugin creator - ::InstanceNormalization_TRT version 2
[TRT]    Registered plugin creator - ::LReLU_TRT version 1
[TRT]    Registered plugin creator - ::MultilevelCropAndResize_TRT version 1
[TRT]    Registered plugin creator - ::MultilevelProposeROI_TRT version 1
[TRT]    Registered plugin creator - ::MultiscaleDeformableAttnPlugin_TRT version 1
[TRT]    Registered plugin creator - ::NMSDynamic_TRT version 1
[TRT]    Registered plugin creator - ::NMS_TRT version 1
[TRT]    Registered plugin creator - ::Normalize_TRT version 1
[TRT]    Registered plugin creator - ::PillarScatterPlugin version 1
[TRT]    Registered plugin creator - ::PriorBox_TRT version 1
[TRT]    Registered plugin creator - ::ProposalDynamic version 1
[TRT]    Registered plugin creator - ::ProposalLayer_TRT version 1
[TRT]    Registered plugin creator - ::Proposal version 1
[TRT]    Registered plugin creator - ::PyramidROIAlign_TRT version 1
[TRT]    Registered plugin creator - ::Region_TRT version 1
[TRT]    Registered plugin creator - ::Reorg_TRT version 1
[TRT]    Registered plugin creator - ::ResizeNearest_TRT version 1
[TRT]    Registered plugin creator - ::ROIAlign_TRT version 1
[TRT]    Registered plugin creator - ::RPROI_TRT version 1
[TRT]    Registered plugin creator - ::ScatterND version 1
[TRT]    Registered plugin creator - ::SpecialSlice_TRT version 1
[TRT]    Registered plugin creator - ::Split version 1
[TRT]    Registered plugin creator - ::VoxelGeneratorPlugin version 1
[TRT]    detected model format - caffe  (extension '.caffemodel')
[TRT]    desired precision specified for GPU: FASTEST
[TRT]    requested fasted precision for device GPU without providing valid calibrator, disabling INT8
[TRT]    [MemUsageChange] Init CUDA: CPU +298, GPU +0, now: CPU 321, GPU 223 (MiB)
[TRT]    Trying to load shared library libnvinfer_builder_resource.so.8.5.1
[TRT]    Loaded shared library libnvinfer_builder_resource.so.8.5.1
[TRT]    [MemUsageChange] Init builder kernel library: CPU +262, GPU +76, now: CPU 637, GPU 299 (MiB)
[TRT]    CUDA lazy loading is not enabled. Enabling it can significantly reduce device memory usage. See `CUDA_MODULE_LOADING` in https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#env-vars
[TRT]    native precisions detected for GPU:  FP32, FP16, INT8
[TRT]    selecting fastest native precision for GPU:  FP16
[TRT]    attempting to open engine cache file networks/bvlc_googlenet.caffemodel.1.1.8501.GPU.FP16.engine
[TRT]    loading network plan from engine cache... networks/bvlc_googlenet.caffemodel.1.1.8501.GPU.FP16.engine
[TRT]    device GPU, loaded networks/bvlc_googlenet.caffemodel
[TRT]    Loaded engine size: 15 MiB
[TRT]    Trying to load shared library libcudnn.so.8
[TRT]    Loaded shared library libcudnn.so.8
[TRT]    Using cuDNN as plugin tactic source
[TRT]    Using cuDNN as core library tactic source
[TRT]    [MemUsageChange] Init cuDNN: CPU +576, GPU +236, now: CPU 978, GPU 477 (MiB)
[TRT]    Deserialization required 506628 microseconds.
[TRT]    [MemUsageChange] TensorRT-managed allocation in engine deserialization: CPU +0, GPU +13, now: CPU 0, GPU 13 (MiB)
[TRT]    Trying to load shared library libcudnn.so.8
[TRT]    Loaded shared library libcudnn.so.8
[TRT]    Using cuDNN as plugin tactic source
[TRT]    Using cuDNN as core library tactic source
[TRT]    [MemUsageChange] Init cuDNN: CPU +1, GPU +8, now: CPU 979, GPU 477 (MiB)
[TRT]    Total per-runner device persistent memory is 94720
[TRT]    Total per-runner host persistent memory is 147808
[TRT]    Allocated activation device memory of size 3612672
[TRT]    [MemUsageChange] TensorRT-managed allocation in IExecutionContext creation: CPU +0, GPU +3, now: CPU 0, GPU 16 (MiB)
[TRT]    CUDA lazy loading is not enabled. Enabling it can significantly reduce device memory usage. See `CUDA_MODULE_LOADING` in https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#env-vars
[TRT]
[TRT]    CUDA engine context initialized on device GPU:
[TRT]       -- layers       75
[TRT]       -- maxBatchSize 1
[TRT]       -- deviceMemory 3612672
[TRT]       -- bindings     2
[TRT]       binding 0
                -- index   0
                -- name    'data'
                -- type    FP32
                -- in/out  INPUT
                -- # dims  3
                -- dim #0  3
                -- dim #1  224
                -- dim #2  224
[TRT]       binding 1
                -- index   1
                -- name    'prob'
                -- type    FP32
                -- in/out  OUTPUT
                -- # dims  3
                -- dim #0  1000
                -- dim #1  1
                -- dim #2  1
[TRT]
[TRT]    binding to input 0 data  binding index:  0
[TRT]    binding to input 0 data  dims (b=1 c=3 h=224 w=224) size=602112
[TRT]    binding to output 0 prob  binding index:  1
[TRT]    binding to output 0 prob  dims (b=1 c=1000 h=1 w=1) size=4000
[TRT]
[TRT]    device GPU, networks/bvlc_googlenet.caffemodel initialized.
[TRT]    imageNet -- loaded 1000 class info entries
[TRT]    imageNet -- networks/bvlc_googlenet.caffemodel initialized.
[image]  loaded 'images/dog_0.jpg'  (500x375, 3 channels)
class 0248 - 0.229980  (Eskimo dog, husky)
class 0249 - 0.605469  (malamute, malemute, Alaskan malamute)
class 0250 - 0.160400  (Siberian husky)
imagenet:  60.54688% class #249 (malamute, malemute, Alaskan malamute)

[TRT]    ------------------------------------------------
[TRT]    Timing Report networks/bvlc_googlenet.caffemodel
[TRT]    ------------------------------------------------
[TRT]    Pre-Process   CPU   0.02498ms  CUDA   0.21392ms
[TRT]    Network       CPU   1.04583ms  CUDA   0.86154ms
[TRT]    Post-Process  CPU   0.02265ms  CUDA   0.02288ms
[TRT]    Total         CPU   1.09346ms  CUDA   1.09834ms
[TRT]    ------------------------------------------------

[TRT]    note -- when processing a single image, run 'sudo jetson_clocks' before
                to disable DVFS for more accurate profiling/timing measurements

[image]  imageLoader -- End of Stream (EOS) has been reached, stream has been closed
imagenet:  shutting down...
imagenet:  shutdown complete.
```

**Note**: _The first time the engine needs to do some autotuning, so it will
take some time and drop output similar to the one below_:

```console
...
[TRT]    Tactic: 0x89c2d153627e52ba Time: 0.0134678
[TRT]    loss3/classifier Set Tactic Name: volta_h884cudnn_256x128_ldg8_relu_exp_small_nhwc_tn_v1 Tactic: 0xc110e19c9f5aa36e
[TRT]    Tactic: 0xc110e19c9f5aa36e Time: 0.0752844
[TRT]    loss3/classifier Set Tactic Name: turing_h1688cudnn_256x128_ldg8_relu_exp_medium_nhwc_tn_v1 Tactic: 0xdc1c841ef1cd3e8e
[TRT]    Tactic: 0xdc1c841ef1cd3e8e Time: 0.0422516
[TRT]    loss3/classifier Set Tactic Name: sm70_xmma_fprop_implicit_gemm_f16f16_f16f16_f16_nhwckrsc_nhwc_tilesize128x64x32_stage1_warpsize2x2x1_g1_tensor8x8x4_t1r1s1 Tactic: 0x4c17dc9d992e6a1d
[TRT]    Tactic: 0x4c17dc9d992e6a1d Time: 0.0231476
[TRT]    loss3/classifier Set Tactic Name: sm75_xmma_fprop_implicit_gemm_f16f16_f16f16_f16_nhwckrsc_nhwc_tilesize128x128x64_stage1_warpsize2x2x1_g1_tensor16x8x8_t1r1s1 Tactic: 0xc399fdbffdc34032
[TRT]    Tactic: 0xc399fdbffdc34032 Time: 0.0262451
[TRT]    loss3/classifier Set Tactic Name: turing_h1688cudnn_256x64_sliced1x2_ldg8_relu_exp_interior_nhwc_tn_v1 Tactic: 0x105f56cf03ee5549
[TRT]    Tactic: 0x105f56cf03ee5549 Time: 0.0241811
[TRT]    Fastest Tactic: 0x017a89ce2d82b850 Time: 0.00878863
[TRT]    >>>>>>>>>>>>>>> Chose Runner Type: CaskGemmConvolution Tactic: 0x0000000000020318
[TRT]    =============== Computing costs for
[TRT]    *************** Autotuning format combination: Float(1000,1,1,1) -> Float(1000,1,1,1) ***************
[TRT]    --------------- Timing Runner: prob (CudaSoftMax)
[TRT]    Tactic: 0x00000000000003ea Time: 0.00364102
[TRT]    Fastest Tactic: 0x00000000000003ea Time: 0.00364102
[TRT]    --------------- Timing Runner: prob (CaskSoftMax)
[TRT]    CaskSoftMax has no valid tactics for this config, skipping
[TRT]    >>>>>>>>>>>>>>> Chose Runner Type: CudaSoftMax Tactic: 0x00000000000003ea
[TRT]    *************** Autotuning format combination: Half(1000,1,1,1) -> Half(1000,1,1,1) ***************
[TRT]    --------------- Timing Runner: prob (CudaSoftMax)
[TRT]    Tactic: 0x00000000000003ea Time: 0.00370118
[TRT]    Fastest Tactic: 0x00000000000003ea Time: 0.00370118
[TRT]    --------------- Timing Runner: prob (CaskSoftMax)
[TRT]    CaskSoftMax has no valid tactics for this config, skipping
[TRT]    >>>>>>>>>>>>>>> Chose Runner Type: CudaSoftMax Tactic: 0x00000000000003ea
[TRT]    *************** Autotuning format combination: Half(500,1:2,1,1) -> Half(500,1:2,1,1) ***************
[TRT]    --------------- Timing Runner: prob (CudaSoftMax)
[TRT]    Tactic: 0x0000000000000012 Time: 0.00347464
[TRT]    Fastest Tactic: 0x0000000000000012 Time: 0.00347464
[TRT]    >>>>>>>>>>>>>>> Chose Runner Type: CudaSoftMax Tactic: 0x0000000000000012
[TRT]    Adding reformat layer: Reformatted Input Tensor 0 to conv1/7x7_s2 + conv1/relu_7x7 (data) from Float(150528,50176,224,1) to Half(100352,50176:2,224,1)
[TRT]    Adding reformat layer: Reformatted Input Tensor 0 to conv2/3x3_reduce + conv2/relu_3x3_reduce (pool1/norm1) from Half(100352,3136:2,56,1) to Half(25088,1:8,448,8)
[TRT]    Adding reformat layer: Reformatted Input Tensor 0 to conv2/norm2 (conv2/3x3) from Half(75264,1:8,1344,24) to Half(301056,3136:2,56,1)
[TRT]    Adding reformat layer: Reformatted Output Tensor 0 to pool2/3x3_s2 (pool2/3x3_s2) from Half(75264,784:2,28,1) to Half(18816,1:8,672,24)
[TRT]    Adding reformat layer: Reformatted Output Tensor 0 to inception_4a/1x1 + inception_4a/relu_1x1 || inception_4a/3x3_reduce + inception_4a/relu_3x3_reduce || inception_4a/5x5_reduce + inception_4a/relu_5x5_reduce (inception_4a/1x1 + inception_4a/relu_1x1 || inception_4a/3x3_reduce + inception_4a/relu_3x3_reduce || inception_4a/5x5_reduce + inception_4a/relu_5x5_reduce) from Half(7448,1:8,532,38) to Half(29792,196:2,14,1)
...
```

**Note**: _If you want to avoid that everytime you run the container, keep the
networks folder outside the container and bind mount it (eg. in the `/data/code`
path). That is, instead of doing `ln -s /usr/local/data/networks .` do a
`cp -avf /usr/local/data/networks .`. Thus, every time you re-run the example
using this folder, the auto-tuned engine will be there._
