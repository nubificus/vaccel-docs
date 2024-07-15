# Building the vAccel Runtime

## vAccelRT

vAccel is a runtime system for hardware acceleration. It provides an API with a set of functions that the runtime is able to offload to hardware acceleration
devices. The design of the runtime is modular, it consists of a front-end library which exposes the API to the user application and a set of back-end plugins
that are responsible to offload computations to the accelerator.

This design decouples the user application from the actual accelerator specific code. The advantage of this choice is that the application can make use of
different hardware accelerators without extra development cost or re-compiling.

[This](https://github.com/cloudkernels/vaccel) repo includes the core runtime system, and back-end plugins for VirtIO and the Jetson Inference framework.

### Build & Installation

#### 1. Cloning and preparing the build directory

```zsh
~ » git clone https://github.com/cloudkernels/vaccel.git

Cloning into 'vaccelrt'...
remote: Enumerating objects: 215, done.
remote: Counting objects: 100% (215/215), done.
remote: Compressing objects: 100% (130/130), done.
remote: Total 215 (delta 115), reused 173 (delta 82), pack-reused 0
Receiving objects: 100% (215/215), 101.37 KiB | 804.00 KiB/s, done.
Resolving deltas: 100% (115/115), done.
~ » cd vaccelrt
~/vaccelrt(master) » mkdir build
~/vaccelrt(master) » cd build
~/vaccelrt/build(master) »                                                                                   
```

#### 2. Building the core runtime system
```zsh
# This sets the installation path to ${HOME}/.local
~/vaccelrt/build(master) » cmake -DCMAKE_INSTALL_PREFIX=~/.local ..
~/vaccelrt/build(master) » mak
~/vaccelrt/build(master) » mak install
```

#### 3. Building the plugins

Building the plugins is disabled, by default. You can enable building one or
more plugins at configuration time of CMake by setting the corresponding
variable of the following table to `ON`

Backend Plugin | Variable | Default
-------------- | -------- | -------
virtio | BUILD\_PLUGIN\_VIRTIO | `OFF`
jetson | BUILD\_PLUGIN\_JETSON | `OFF`

For example:

```sh
cmake -DBUILD_PLUGIN_VIRTIO=ON ..
```

will enable building the virtio backend plugin.

#### VirtIO plugin building options

Variable | Values | Default
-------- | ------ | -------
VIRTIO\_ACCEL\_ROOT | Path to virtio module installation | `/usr/local/include`


The VirtIO plugin uses the [virtio-accel](https://github.com/cloudkernels/virtio-accel)
kernel module to offload requests to the host. When building we need to point
CMake to the location of virtio-accel installation prefix using the
`VIRTIO_ACCEL_ROOT` variable.

#### Jetson plugin building options

The jetson inference backends depends on the Jetson inference framework, a
corresponding CUDA installation and the STB library.

Variable | Values | Default
-------- | ------ | -------
CUDA\_DIR | Path to CUDA installation | `/usr/local/cuda/targets/x86_64-linux`
JETSON\_DIR | Path to Jetson installation | `/usr/local`
STB\_DIR | Path to STB installation | `/usr/local`
