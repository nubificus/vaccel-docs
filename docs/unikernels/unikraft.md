---
title: "How to run a vAccel application using Unikraft"
date: 2021-02-03T17:15:12+02:00
author: Charalampos Mainas
description : "Instructions to use vAccel in Unikraft"
---

To run an image classification app in Unikraft using vAccel, we need:

- an NVIDIA GPU which supports CUDA 
- the appropriate device drivers
- [jetson-inference](https://github.com/dusty-nv/jetson-inference)

As long as we have the above dependencies, we can proceed setting up the vAccel
environment for our example. A comprehensive walk through on installing the
above dependencies is given in [Jetson-inference](/jetson). 

Additionally, we will need to set up 3 components:

- The vAccel Runtime system, [vAccelrt](https://github.com/cloudkernels/vaccelrt) on the bost
- A hypervisor with vAccel support, in our case [QEMU](https://github.com/cloudkernels/qemu-vaccel/tree/vaccelrt_legacy_virtio)
- and of course [Unikraft](https://github.com/cloudkernels/unikraft/tree/vaccelrt_rel010)

To make things easier we have created some scripts and Docketfiles which
produce a vAccel enabled QEMU and a Unikraft unikernel. You can get them from
[this](https://github.com/nubificus/qemu-x86-build/tree/unikernels_vaccelrt)
repo. The first 2 components can be built using the build.sh script with the -u
option, like:

```
bash build.sh -u
```
The last component can be created using the build\_guest.sh script with the -u option, like:
```
bash build_guest.sh -u
```

After succefully building all components we can just fire up our unikernel
using the command:
```
bash run.sh
```

This command will start Unikraft over QEMU classifying the image `dog_0.jpg`
under `guest/data/` directory of this repo.

Let's take a closer look on what is happening inside the containers and how we
can perform each step by ourselves.

### Setting up vAccert for the host

Follow the relevant documentation to install the [vAccelrt core
library](/binaries/#deb-package) and the [jetson-infernece
plugin](binaries/#deb-package_1).  ```

### Build QEMU with vAccel support

For the time being we have a seperated branch where QEMU exposes vAccel to the
guest with legacy virtio. First lets get the source code:

```sh
git clone --recursive https://github.com/cloudkernels/qemu-vaccel.git -b vaccelrt
cd qemu-vaccel
```

We will configure QEMU with only one target and we need to point out the
install location of vAccelrt with cflags and ldflags. Please set the install
prefix in case you do not want it to be installed in the default directory.

```sh
mkdir build && cd build
../configure --extra-cflags="-I /usr/local/include" --extra-ldflags="-L/usr/local/lib" --target-list=x86_64-softmmu --enable-virtfs
make -j$(nproc) && make install
```

THat's it. We are done with the host side!

### Build the Unikraft application

We will follow the instructions from [Unikraft's
documentation](https://unikraft.org/docs/usage/make_build/) with a minor
change. We will not use the official Unikraft repo but our fork. In our fork we
have added an example application for image classification.

```
git clone https://github.com/cloudkernels/unikraft.git
mkdir apps/
cp -r unikraft/example apps/classify
cd apps/classify
```

Our example has a config which enables vAccel support for Unikraft and a lot of
debug messages. You can use that config or you can make your own config, but
make sure you select vaccelrt under library configuration inside menuconfig.

```
cp vaccel_config .config && make olddefconfig
make
```

After building is done, there will be a Unikraft image for KVM under the build directory.

### Fire it up!

After that long journey of building let's see what we have done. Not yet...

One more thing. We need to get the model which will be used for the image
classification. We will use a script which is already provided by
jetson-inference (normally under `/usr/local/share/jetson-inference/tools`. Also
we need to point vAccel's jetson plugin the path to that model.

```sh
/path/to/download-models.sh
cp /usr/local/share/jetson-inference/data/networks/* networks
export VACCEL_IMAGENET_NETWORKS=/full/path/to/newly/downloaded/networks/directory
```

Finally we can run our unikernel using the command below:

```sh
LD_LIBRARY_PATH=/usr/local/lib:/usr/local/nvidia/lib:/usr/local/nvidia/lib64 qemu-system-x86_64 -cpu host -m 512 -enable-kvm -nographic -vga none \
	-fsdev local,id=myid,path=/data/data,security_model=none -device virtio-9p-pci,fsdev=myid,mount_tag=data,disable-modern=on,disable-legacy=off \
	-object acceldev-backend-vaccelrt,id=gen0 -device virtio-accel-pci,id=accl0,runtime=gen0,disable-legacy=off,disable-modern=on \
	-kernel /data/classify_kvm-x86_64 -append "vfs.rootdev=data -- dog_0.jpg 1"
```

Let's highlight some parts of the qemu command:
 
- `LD\_LIBRARY\_PATH` environment variable: QEMU will dynamically link with every library it needs and in this case it also needs the vAccelrt library
- `-fsdev local,id=myid,path=./data,security\_model=none`: We need to tell QEMU where will find the data that will pass to the guest. The data directory contains the image we want to classify
- `-object acceldev-backend-vaccelrt,id=gen0 -device virtio-accel-pci,id=accl0,runtime=gen0,disable-legacy=off,disable-modern=on`: For the vAccel driver
- `-append "vfs.rootdev=data -- dog_0.jpg 1"`: In the command line we need to tell the classify application which image to classify and how many iterations to do
