---
title: "How to run a vAccel application using Unikraft"
date: 2021-02-03T17:15:12+02:00
author: Charalampos Mainas
description : "Instructions to use vAccel in Unikraft"
---

Consuming the vAccel API from the Unikraft Unikernel can be a challenge! In
what follows we will walk through the steps of the integration and show a
simple example application running on Unikraft using the vAccel API.

### Build a vAccel-enabled QEMU

First, we treat unikraft as a single application OS kernel -- so, essentially,
we bundle a vAccel application in a Unikraft binary and run this as a Virtual
Machine. We use QEMU/KVM as the hypervisor.

For now, only the `virtio` plugin is supported on Unikraft, so we will have to
use our [downstream
QEMU](https://github.com/cloudkernels/qemu-vaccel/tree/unikraft_vaccelrt) port,
with the vAccel virtio backend built in.

To get the code & build it, we can use the following commands:

```sh
git clone --recursive https://github.com/cloudkernels/qemu-vaccel.git -b unikraft_vaccelrt
export QEMU_SOURCE=$PWD/qemu-vaccel
cd qemu-vaccel
mkdir build && cd build
../configure --extra-cflags="-I /usr/local/include" --extra-ldflags="-L/usr/local/lib" --target-list=x86_64-softmmu --enable-virtfs && make -j $(nproc)
```

Now the QEMU binary is at `$QEMU_SOURCE/build/x86_64-softmmu/qemu-system-x86_64`. Save this path:

```sh
export QEMU_BINARY="$QEMU_SOURCE/build/x86_64-softmmu/qemu-system-x86_64"
cd ../../
```

### Build a vAccel app in Unikraft

We will follow the instructions from [Unikraft's
documentation](https://unikraft.org/docs/usage/make_build/) with a minor
change. We will not use the official Unikraft repo but our fork. 

```
mkdir unikraft_dev && cd unikraft_dev
git clone https://github.com/cloudkernels/unikraft.git -b vaccelrt_rel010
mkdir apps/ && mkdir libs 
cd libs && git clone https://github.com/unikraft/lib-newlib && cd ..
cd apps
git clone https://github.com/cloudkernels/unikraft_vaccel_examples
cd unikraft_vaccel_examples
```

Our examples repo has a config which enables vAccel support for Unikraft and a
lot of debug messages. You can use that config or you can make your own config,
but make sure you select vaccelrt under library configuration inside
menuconfig. Also, make sure you choose one application (eg. Image
Classification).

```
cp vaccel_config .config && make olddefconfig
make menuconfig
## Choose Image classification, exit & save
make
```

You should be presented with a binary: `build/unikraft_vaccel_examples_kvm-x86_64`

save this in an env variable:

```sh
export UNIKRAFT_BINARY=$PWD/build/unikraft_vaccel_examples_kvm-x86_64
```

### Install vAccel dependencies

Now, we need to install the vAccel core library and a plugin. Follow the
instructions from the
[docs](../user-guide/binaries.md#install-vaccelrt-core-library). Bundled
with the core library is the `noop` plugin which we will use as the example.

*TL;DR*

```sh
wget https://s3.nbfc.io/nbfc-assets/github/vaccelrt/main/x86_64/Release-deb/vaccel-0.6.0-Linux.deb
dpkg -i vaccel-0.6.0-Linux.deb
```

### Run the application

To execute the application we have all the binaries we need; we just need to set some env variables and fire-up the unikernel.

#### Prepare the environment

Set the `LD_LIBRARY_PATH` and the plugin (`VACCEL_BACKENDS`)
```sh
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
export VACCEL_BACKENDS=/usr/local/lib/libvaccel-noop.so
```

set the path in host we will share:

```sh
export DATA=/usr/local/share/images
```

set the arguments for the application

```sh
export ARGS="example.jpg 1"
```

#### Spawn the Unikernel

the QEMU spawn command is a bit bulky, so we will walk it through:

```sh
$QEMU_BINARY -cpu host \
                -m 4 \
                -enable-kvm \
                -nographic -vga none \
                -fsdev local,id=myid,path=$DATA,security_model=none \
                -device virtio-9p-pci,fsdev=myid,mount_tag=data,disable-modern=on,disable-legacy=off \
                -object acceldev-backend-vaccelrt,id=gen0 \
                -device virtio-accel-pci,id=accl0,runtime=gen0,disable-legacy=off,disable-modern=on \
                -kernel $UNIKRAFT_BINARY \
                -append "vfs.rootdev=data -- $ARGS"
```

- `-cpu host`:  # CPU mode, copy the host's CPU arch
- `-m 4 `: Memory, yes, we only need 4 MBs of memory!
- `-enable-kvm`: Enable hardware virtualization support
- `-nographic -vga none`: we don't need any graphics support
- `-fsdev local,id=myid,path=$DATA,security_model=none`: Folder where input files are stored
- `-device virtio-9p-pci,fsdev=myid,mount_tag=data,disable-modern=on,disable-legacy=off`: device for virtio-9p fs
- `-object acceldev-backend-vaccelrt,id=gen0`: the vAccel virtio backend device file
- `-device virtio-accel-pci,id=accl0,runtime=gen0,disable-legacy=off,disable-modern=on`: the vAccel virtio device
- `-kernel $UNIKRAFT_BINARY`: our unikernel Image
- `-append "vfs.rootdev=data -- $ARGS"`: our command line arguments


### Setup the host for GPU acceleration

To run a more realistic scenario (i.e. the above example with a hardware
plugin), we could use jetson-inference, a simple AI framework from NVIDIA that
exposes Image inference operations through a simple, intuitive API.

To run such an example, we will need:

- an NVIDIA GPU which supports CUDA and TensorRT
- the appropriate device drivers (nvidia-drivers-460+)
- the [jetson-inference](https://github.com/dusty-nv/jetson-inference) framework

As long as we have the above dependencies, the only thing we need to change in
the example we just ran is the plugin.  A comprehensive walk through on
installing the above dependencies is given in
[Jetson-inference](../useful-docs/jetson.md).

### Install the jetson-inference vAccel plugin

Given we have a working jetson-inference installation, we need to get the
vAccel jetson-inference plugin. Have a look at [how we install plugins for
vAccel](../user-guide/binaries.md#install plugins) and pick-up the jetson-inference
binary from the [binaries](../user-guide/binaries.md#binaries) table.

TL;DR

```sh
wget https://s3.nbfc.io/nbfc-assets/github/vaccelrt/plugins/jetson_inference/main/x86_64/Release-deb/vaccelrt-plugin-jetson-0.1-Linux.deb
dpkg -i vaccelrt-plugin-jetson-0.1-Linux.deb
```

Having the same env variables set as above, we need to change the plugin:

```sh
export VACCEL_BACKENDS=/usr/local/lib/libvaccel-jetson.so
```

and if we re-run the QEMU command above, we will get a real response for Image
classification, from the GPU.

```console
# $QEMU_BINARY -cpu host \
                -m 4 \
                -enable-kvm \
                -nographic -vga none \
                -fsdev local,id=myid,path=$DATA,security_model=none \
                -device virtio-9p-pci,fsdev=myid,mount_tag=data,disable-modern=on,disable-legacy=off \
                -object acceldev-backend-vaccelrt,id=gen0 \
                -device virtio-accel-pci,id=accl0,runtime=gen0,disable-legacy=off,disable-modern=on \
                -kernel $UNIKRAFT_BINARY \
                -append "vfs.rootdev=data -- $ARGS"
Booting from ROM..[    0.000000] Info: [libkvmplat] <setup.c @  468> Entering from KVM (x86)...
[    0.000000] Info: [libkvmplat] <setup.c @  469>      multiboot: 0x9500
[    0.000000] Info: [libkvmplat] <setup.c @  487>     heap start: 0x170000
[    0.000000] Info: [libkvmplat] <setup.c @  492>      stack top: 0x3d0000
[    0.000000] Info: [libkvmplat] <setup.c @  519> Switch from bootstrap stack to stack @0x3e0000
[    0.000000] Info: [libukboot] <boot.c @  200> Unikraft constructor table at 0x13c000 - 0x13c040
[    0.000000] Info: [libuklibparam] <param.c @  113> libname: vfs, 96
[    0.000000] Info: [libuklibparam] <param.c @  655> Parsed 1 args
[    0.000000] Info: [libukboot] <boot.c @  213> Found 2 library args
[    0.000000] Info: [libukboot] <boot.c @  221> Initialize memory allocator...
[    0.000000] Info: [libukallocbbuddy] <bbuddy.c @  516> Initialize binary buddy allocator 170000
[    0.000000] Info: [libukboot] <boot.c @  264> Initialize IRQ subsystem...
[    0.000000] Info: [libukboot] <boot.c @  271> Initialize platform time...
[    0.000000] Info: [libkvmplat] <tscclock.c @  253> Calibrating TSC clock against i8254 timer
[    0.100002] Info: [libkvmplat] <tscclock.c @  275> Clock source: TSC, frequency estimate is 3400051000 Hz
[    0.103194] Info: [libukschedcoop] <schedcoop.c @  232> Initializing cooperative scheduler
[    0.105880] Info: [libuksched] <thread.c @  181> Thread "Idle": pointer: 0x173060, stack: 0x390000, tls: 0x174020
[    0.109225] Info: [libuksched] <thread.c @  181> Thread "main": pointer: 0x176010, stack: 0x310000, tls: 0x177020
[    0.112698] Info: [libukboot] <boot.c @   96> Init Table @ 0x13c040 - 0x13c060
[    0.115131] Info: [libukbus] <bus.c @  134> Initialize bus handlers...
[    0.117423] Info: [libuk9p] <9pdev_trans.c @   59> Registered transport virtio
[    0.119917] Info: [libukbus] <bus.c @  136> Probe buses...
[    0.121811] Info: [libkvmpci] <pci_bus_x86.c @  164> PCI 00:00.00 (0600 8086:1237): <no driver>
[    0.124901] Info: [libkvmpci] <pci_bus_x86.c @  164> PCI 00:01.00 (0600 8086:7000): <no driver>
[    0.128151] Info: [libkvmpci] <pci_bus_x86.c @  164> PCI 00:02.00 (0200 8086:100e): <no driver>
[    0.131345] Info: [libkvmpci] <pci_bus_x86.c @  164> PCI 00:03.00 (0000 1af4:1009): driver 0x1430a0
[    0.134400] Info: [libkvmvirtio] <virtio_pci.c @  380> Added virtio-pci device 1009
[    0.136950] Info: [libkvmvirtio] <virtio_pci.c @  382> Added virtio-pci subsystem_device_id 0009
[    0.140147] Info: [libkvmvirtio] <virtio_bus.c @  127> Virtio device 0x17a010 initialized
[    0.143132] Info: [libkvmvirtio9p] <virtio_9p.c @  405> virtio-9p: Configured: features=0x1 tag=data
[    0.146458] Info: [libkvmvirtio9p] <virtio_9p.c @  418> virtio-9p: data started
[    0.149328] Info: [libkvmpci] <pci_bus_x86.c @  164> PCI 00:04.00 (0000 1af4:1015): driver 0x1430a0
[    0.152823] Info: [libkvmvirtio] <virtio_pci.c @  380> Added virtio-pci device 1015
[    0.155504] Info: [libkvmvirtio] <virtio_pci.c @  382> Added virtio-pci subsystem_device_id 0015
[    0.158626] Info: [libkvmvirtio] <virtio_bus.c @  127> Virtio device 0x17f010 initialized
[    0.161435] Info: [libkvmvirtioaccel] <accel.c @   95> Register 'accel' to devfs
[    0.164312] Info: [libkvmvirtioaccel] <virtio_accel-core.c @  369> Accelerator is ready
[    0.167155] Info: [libkvmvirtioaccel] <virtio_accel-core.c @  377> vaccel: started
[    0.170185] Info: [libvfscore] <rootfs.c @  120> Mount 9pfs to /...
[    0.172484] Info: [libvfscore] <mount.c @  122> VFS: mounting 9pfs at /
[    0.175120] Info: [libdevfs] <devfs_vnops.c @  309> Mount devfs to /dev...VFS: mounting devfs at /dev
Powered by
o.   .o       _ _               __ _
Oo   Oo  ___ (_) | __ __  __ _ ' _) :_
oO   oO ' _ `| | |/ /  _)' _` | |_|  _)
oOo oOO| | | | |   (| | | (_) |  _) :_
 OoOoO ._, ._:_:_,\_._,  .__,_:_, \___)
                 Phoebe 0.10.0~f7d1c557
[    0.186934] Info: [libukboot] <boot.c @  126> Pre-init table at 0x142238 - 0x142238
[    0.189672] Info: [libukboot] <boot.c @  137> Constructor table at 0x142238 - 0x142238
[    0.192617] Info: [libukboot] <boot.c @  146> Calling main(3, ['unikraft-testbed/unikraft_dev/apps/unikraft_vaccel_examples/build/unikraft_vaccel_examples_kvm-x86_64', 'example.jpg', '1'])
Initialized session with id: 1
Image size: 79281B

imageNet -- loading classification network model from:
         -- prototxt     networks/googlenet.prototxt
         -- model        networks/bvlc_googlenet.caffemodel
         -- class_labels networks/ilsvrc12_synset_words.txt
         -- input_blob   'data'
         -- output_blob  'prob'
         -- batch_size   1

[TRT]    TensorRT version 8.5.2
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
[TRT]    Registered plugin creator - ::fMHA_V2 version 1
[TRT]    Registered plugin creator - ::fMHCA version 1
[TRT]    Registered plugin creator - ::GenerateDetection_TRT version 1
[TRT]    Registered plugin creator - ::GridAnchor_TRT version 1
[TRT]    Registered plugin creator - ::GridAnchorRect_TRT version 1
[TRT]    Registered plugin creator - ::GroupNorm version 1
[TRT]    Registered plugin creator - ::InstanceNormalization_TRT version 1
[TRT]    Registered plugin creator - ::InstanceNormalization_TRT version 2
[TRT]    Registered plugin creator - ::LayerNorm version 1
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
[TRT]    Registered plugin creator - ::SeqLen2Spatial version 1
[TRT]    Registered plugin creator - ::SpecialSlice_TRT version 1
[TRT]    Registered plugin creator - ::SplitGeLU version 1
[TRT]    Registered plugin creator - ::Split version 1
[TRT]    Registered plugin creator - ::VoxelGeneratorPlugin version 1
[TRT]    detected model format - caffe  (extension '.caffemodel')
[TRT]    desired precision specified for GPU: FASTEST
[TRT]    requested fasted precision for device GPU without providing valid calibrator, disabling INT8
[TRT]    [MemUsageChange] Init CUDA: CPU +307, GPU +0, now: CPU 326, GPU 223 (MiB)
[TRT]    Trying to load shared library libnvinfer_builder_resource.so.8.5.2
[TRT]    Loaded shared library libnvinfer_builder_resource.so.8.5.2
[TRT]    [MemUsageChange] Init builder kernel library: CPU +262, GPU +74, now: CPU 642, GPU 297 (MiB)
[TRT]    CUDA lazy loading is not enabled. Enabling it can significantly reduce device memory usage. See `CUDA_MODULE_LOADING` in https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#env-vars
[TRT]    native precisions detected for GPU:  FP32, FP16, INT8
[TRT]    selecting fastest native precision for GPU:  FP16
[TRT]    found engine cache file networks/bvlc_googlenet.caffemodel.1.1.8502.GPU.FP16.engine
[TRT]    found model checksum networks/bvlc_googlenet.caffemodel.sha256sum
[TRT]    echo "$(cat networks/bvlc_googlenet.caffemodel.sha256sum) networks/bvlc_googlenet.caffemodel" | sha256sum --check --status
[TRT]    model matched checksum networks/bvlc_googlenet.caffemodel.sha256sum
[TRT]    loading network plan from engine cache... networks/bvlc_googlenet.caffemodel.1.1.8502.GPU.FP16.engine
[TRT]    device GPU, loaded networks/bvlc_googlenet.caffemodel
[TRT]    Loaded engine size: 15 MiB
[TRT]    Deserialization required 8816 microseconds.
[TRT]    [MemUsageChange] TensorRT-managed allocation in engine deserialization: CPU +0, GPU +13, now: CPU 0, GPU 13 (MiB)
[TRT]    Total per-runner device persistent memory is 94720
[TRT]    Total per-runner host persistent memory is 149856
[TRT]    Allocated activation device memory of size 3612672
[TRT]    [MemUsageChange] TensorRT-managed allocation in IExecutionContext creation: CPU +0, GPU +3, now: CPU 0, GPU 16 (MiB)
[TRT]    CUDA lazy loading is not enabled. Enabling it can significantly reduce device memory usage. See `CUDA_MODULE_LOADING` in https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#env-vars
[TRT]    
[TRT]    CUDA engine context initialized on device GPU:
[TRT]       -- layers       72
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
[TRT]    loaded 1000 class labels
[TRT]    imageNet -- networks/bvlc_googlenet.caffemodel initialized.
class 0954 - 0.999023  (banana)
imagenet: 99.90234% class #954 (banana)
imagenet: attempting to save output image
imagenet: completed saving
imagenet: shutting down...
classification tags: 99.902% banana
[    2.994096] Info: [libukboot] <boot.c @  155> main returned 0, halting system
[    2.999903] Info: [libkvmplat] <shutdown.c @   35> Unikraft halted
```

**Note**
We need to get the model which will be used for the image classification. We
will use a script which is already provided by jetson-inference (normally under
`/usr/local/share/jetson-inference`. Also we need to point vAccel's jetson
plugin the path to that model. The jetson-inference installation handles that
just fine using the [`download_models.sh`](https://github.com/dusty-nv/jetson-inference/blob/master/tools/download-models.sh) script.

For the vAccel `jetson-inference` plugin, you can specify the path
to the `networks` folder using the `VACCEL_IMAGENET_NETWORKS` environment
variable.

e.g.:

```sh
export VACCEL_IMAGENET_NETWORKS=/jetson-inference/data/networks
```
