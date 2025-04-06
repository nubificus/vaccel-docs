# VirtIO Plugin

The VirtIO plugin for vAccel implements VirtIO-based transport for vAccel
operations using the [virtio-accel](https://github.com/nubificus/virtio-accel)
kernel module. This plugin is meant to be a more efficient alternative to
standard VirtIO mechanisms like vSock.

## Overview

The plugin forwards vAccel calls from a VM to the virtualization host. To use
this plugin you will need both the virtio-accel module (on the VM) and a custom
VMM with a virtio-accel backend (on the host).

The VMM handles the plugin requests and translates the forwarded calls to host
vAccel calls. Essentially, to use the VirtIO plugin the following components
must be in place:

1. _Guest:_ vAccel + the VirtIO plugin, to forward the application calls
2. _Host:_ VMM w/ virtio-accel support + vAccel + an acceleration plugin, to
   handle the forwarded calls and perform the actual acceleration

Currently, there is a [custom QEMU](https://github.com/cloudkernels/qemu-vaccel)
implementation of the virtio-accel backend.

## Supported operations

- [Image classification](../../../api/api-reference/operations.md#image-classification)
- [Image segmentation](../../../api/api-reference/operations.md#image-segmentation)
- [Object detection](../../../api/api-reference/operations.md#object-detection)
- [Pose estimation](../../../api/api-reference/operations.md#pose-estimation)
- [Monocular depth](../../../api/api-reference/operations.md#monocular-depth)

- [Matrix-to-matrix multiplication](../../../api/api-reference/operations.md#matrix-to-matrix-multiplication)
- [Array copy](../../../api/api-reference/operations.md#array-copy)
- [Matrix-to-matrix multiplication simple](../../../api/api-reference/operations.md#matrix-to-matrix-multiplication-simple)
- [Matrix-to-matrix multiplication and addition simple](../../../api/api-reference/operations.md#matrix-to-matrix-multiplication-and-addition-simple-wip)
- [Vector add](../../../api/api-reference/operations.md#vector-add)

- [Exec](../../../api/api-reference/operations.md#exec)
- [Exec with resource](../../../api/api-reference/operations.md#exec-with-resource)

- [MinMax](../../../api/api-reference/operations.md#minmax)
- [Generic operation](../../../api/api-reference/operations.md#generic-operation)
- [Debug operation](../../../api/api-reference/operations.md#debug-operation)

## Installing the plugin

You can get the latest VirtIO plugin binary release from the
[Releases](https://github.com/nubificus/vaccel/releases) page of the vAccel
repository. Releases include DEB packages and binaries for x86_64/aarch64/armv7l
Ubuntu-based systems.

### DEB

To install the DEB package of the latest VirtIO plugin release:

/// tab | x86

```sh
wget https://github.com/nubificus/vaccel/releases/download/v[[ versions.vaccel ]]/vaccel-virtio_[[ versions.plugins.virtio ]]-1_amd64.deb
sudo dpkg -i vaccel-virtio_[[ versions.plugins.virtio ]]-1_amd64.deb
```

///

/// tab | ARM (64-bit)

```sh
wget https://github.com/nubificus/vaccel/releases/download/v[[ versions.vaccel ]]/vaccel-virtio_[[ versions.plugins.virtio ]]-1_arm64.deb
sudo dpkg -i vaccel-virtio_[[ versions.plugins.virtio ]]-1_arm64.deb
```

///

/// tab | ARM (32-bit)

```sh
wget https://github.com/nubificus/vaccel/releases/download/v[[ versions.vaccel ]]/vaccel-virtio_[[ versions.plugins.virtio ]]-1_armhf.deb
sudo dpkg -i vaccel-virtio_[[ versions.plugins.virtio ]]-1_armhf.deb
```

///

### TAR

To install the TAR binary package of the latest VirtIO plugin release:

/// tab | x86

```sh
wget https://github.com/nubificus/vaccel/releases/download/v[[ versions.vaccel ]]/vaccel-virtio_[[ versions.plugins.virtio ]]_amd64.tar.gz
# Replace '/usr/local' below with the desired installation prefix
tar xfv vaccel-virtio_[[ versions.plugins.virtio ]]_amd64.tar.gz --strip-components=2 -C /usr/local
```

///

/// tab | ARM (64-bit)

```sh
wget https://github.com/nubificus/vaccel/releases/download/v[[ versions.vaccel ]]/vaccel-virtio_[[ versions.plugins.virtio ]]_arm64.tar.gz
# Replace '/usr/local' below with the desired installation prefix
tar xfv vaccel-virtio_[[ versions.plugins.virtio ]]_arm64.tar.gz --strip-components=2 -C /usr/local
```

///

/// tab | ARM (32-bit)

```sh
wget https://github.com/nubificus/vaccel/releases/download/v[[ versions.vaccel ]]/vaccel-virtio_[[ versions.plugins.virtio ]]_armhf.tar.gz
# Replace '/usr/local' below with the desired installation prefix
tar xfv vaccel-virtio_[[ versions.plugins.virtio ]]_armhf.tar.gz --strip-components=2 -C /usr/local
```

///

### Latest artifacts

You can also find prebuilt artifacts of the latest VirtIO plugin revision at:

/// tab | x86

```sh
# DEB
https://s3.nbfc.io/nbfc-assets/github/vaccel/plugins/virtio/rev/main/x86_64/release/vaccel-virtio_latest_amd64.deb
# TAR
https://s3.nbfc.io/nbfc-assets/github/vaccel/plugins/virtio/rev/main/x86_64/release/vaccel-virtio-latest-bin.tar.gz
```

///

/// tab | ARM (64-bit)

```sh
wget https://github.com/nubificus/vaccel/releases/download/v[[ versions.vaccel ]]/vaccel-virtio_[[ versions.plugins.virtio ]]_arm64.tar.gz
# Replace '/usr/local' below with the desired installation prefix
tar xfv vaccel-virtio_[[ versions.plugins.virtio ]]_arm64.tar.gz --strip-components=2 -C /usr/local
```

///

/// tab | ARM (32-bit)

```sh
wget https://github.com/nubificus/vaccel/releases/download/v[[ versions.vaccel ]]/vaccel-virtio_[[ versions.plugins.virtio ]]_armhf.tar.gz
# Replace '/usr/local' below with the desired installation prefix
tar xfv vaccel-virtio_[[ versions.plugins.virtio ]]_armhf.tar.gz --strip-components=2 -C /usr/local
```

///

## Getting the prebuilt VM artifacts

Besides the plugin binaries, you can find prebuilt x86_64/aarch64 artifacts for
running a VM with the
[latest release](https://github.com/nubificus/vaccel/releases). The provided
artifacts contain an Ubuntu `rootfs.img` with the virtio-accel module, VirtIO
plugin and vAccel pre-installed. A Linux kernel image that can be used to run a
vAccel-enabled VM is also included.

### TAR

To get the TAR archive with the prebuilt VM artifacts of the latest VirtIO
plugin release:

/// tab | x86

```sh
wget https://github.com/nubificus/vaccel/releases/download/v[[ versions.vaccel ]]/vaccel-virtio-vm_[[ versions.plugins.virtio ]]_amd64.tar.xz
# Replace 'vm-artifacts' with the desired artifact directory
mkdir -p vm-artifacts && tar xfv vaccel-virtio_[[ versions.plugins.virtio ]]_amd64.tar.gz -C vm-artifacts
find vm-artifacts -name "virtio*.tar.xz" -exec tar xfv {} -C vm-artifacts \;
rm -r vm-artifacts/virtio*.tar.xz
```

///

/// tab | ARM (64-bit)

```sh
wget https://github.com/nubificus/vaccel/releases/download/v[[ versions.vaccel ]]/vaccel-virtio-vm_[[ versions.plugins.virtio ]]_arm64.tar.gz
# Replace 'vm-artifacts' with the desired artifact directory
mkdir -p vm-artifacts && tar xfv vaccel-virtio_[[ versions.plugins.virtio ]]_arm64.tar.gz -C vm-artifacts
find vm-artifacts -name "virtio*.tar.xz" -exec tar xfv {} -C vm-artifacts \;
rm -r vm-artifacts/virtio*.tar.xz
```

///

### Latest artifacts

You can also find the prebuilt VM artifacts of the latest VirtIO plugin revision
at:

/// tab | x86

```sh
# TAR
https://s3.nbfc.io/nbfc-assets/github/vaccel/plugins/virtio/rev/main/x86_64/release/vaccel-virtio-latest-vm.tar.xz
```

///

/// tab | ARM (64-bit)

```sh
# TAR
https://s3.nbfc.io/nbfc-assets/github/vaccel/plugins/virtio/rev/main/aarch64/release/vaccel-virtio-latest-vm.tar.xz
```

///

## Installing a virtio-accel-enabled QEMU

You can get a [Docker](https://www.docker.com/) image with a
virtio-accel-enabled QEMU & vAccel pre-installed for x86_64/aarch64 with:

```sh
docker pull harbor.nbfc.io/nubificus/qemu-vaccel
```

## Usage

To specify VirtIO plugin as the selected plugin for vAccel execution:

```sh
export VACCEL_PLUGINS=libvaccel-virtio.so
```

Ensure vAccel and the VirtIO plugin libraries are in the library search paths
before trying to use the plugin. In order to use the plugin, the
[virtio-accel](https://github.com/nubificus/virtio-accel) module must be loaded
in the VM, the used VMM must have virtio-accel support and the respective
`accel` device must exist.

### Prebuilt VM artifacts usage

Assuming KVM is enabled on your system and you have the
[prebuilt VM artifacts](#getting-the-prebuilt-vm-artifacts) at `vm-artifacts`,
you can boot a virtio-accel-enabled VM with vAccel & the VirtIO plugin
preinstalled using:

/// tab | x86

```sh
cd vm-artifacts
docker run --rm --device=/dev/kvm -it \
    --mount type=bind,source="$(pwd)",destination=/data \
    harbor.nbfc.io/nubificus/qemu-vaccel \
    -r rootfs.img --drive-cache -k bzImage* \
    -M pc,accel=kvm --vcpus 2 -m 2048 \
    /bin/bash
```

///

/// tab | ARM (64-bit)

```sh
cd vm-artifacts
docker run --rm --device=/dev/kvm -it \
    --mount type=bind,source="$(pwd)",destination=/data \
    harbor.nbfc.io/nubificus/qemu-vaccel \
    -r rootfs.img --drive-cache -k Image* \
    --cmdline-append "console=ttyAMA0,115200" \
    -M virt --no-pci --vcpus 2 -m 2048 \
    /bin/bash
```

///

This will start the host vAccel with the `NoOp` plugin by default. To use
plugins not bundled with vAccel you can install them in the current dir and use
them by setting `VACCEL_PLUGINS` in the `docker run` env.

## Running an example

You can run a command directly using the `-c` argument of the qemu-vaccel Docker
image.

Assuming you have the
[prebuilt VM artifacts](#getting-the-prebuilt-vm-artifacts) at `vm-artifacts`,
to run an image classification with the 'NoOp' plugin use:

/// tab | x86

```console
$ cd vm-artifacts
$ docker run --rm --device=/dev/kvm -it \
      --mount type=bind,source="$(pwd)",destination=/data \
      harbor.nbfc.io/nubificus/qemu-vaccel \
      -r rootfs.img --drive-cache -k bzImage* \
      -M pc,accel=kvm --vcpus 2 -m 2048 \
      -c "classify /usr/local/share/vaccel/images/example.jpg"
2025.04.12-20:01:09.85 - <debug> Initializing vAccel
2025.04.12-20:01:09.85 - <info> vAccel 0.6.1-194-19056528
2025.04.12-20:01:09.85 - <debug> Config:
2025.04.12-20:01:09.85 - <debug>   plugins = libvaccel-noop.so
2025.04.12-20:01:09.85 - <debug>   log_level = debug
2025.04.12-20:01:09.85 - <debug>   log_file = (null)
2025.04.12-20:01:09.85 - <debug>   profiling_enabled = false
2025.04.12-20:01:09.85 - <debug>   version_ignore = false
2025.04.12-20:01:09.85 - <debug> Created top-level rundir: /run/user/0/vaccel/u05Rjf
2025.04.12-20:01:09.85 - <info> Registered plugin noop 0.6.1-194-19056528
2025.04.12-20:01:09.85 - <debug> Registered op noop from plugin noop
2025.04.12-20:01:09.85 - <debug> Registered op blas_sgemm from plugin noop
2025.04.12-20:01:09.85 - <debug> Registered op image_classify from plugin noop
2025.04.12-20:01:09.85 - <debug> Registered op image_detect from plugin noop
2025.04.12-20:01:09.85 - <debug> Registered op image_segment from plugin noop
2025.04.12-20:01:09.85 - <debug> Registered op image_pose from plugin noop
2025.04.12-20:01:09.85 - <debug> Registered op image_depth from plugin noop
2025.04.12-20:01:09.85 - <debug> Registered op exec from plugin noop
2025.04.12-20:01:09.85 - <debug> Registered op tf_session_load from plugin noop
2025.04.12-20:01:09.85 - <debug> Registered op tf_session_run from plugin noop
2025.04.12-20:01:09.85 - <debug> Registered op tf_session_delete from plugin noop
2025.04.12-20:01:09.85 - <debug> Registered op minmax from plugin noop
2025.04.12-20:01:09.85 - <debug> Registered op fpga_arraycopy from plugin noop
2025.04.12-20:01:09.85 - <debug> Registered op fpga_vectoradd from plugin noop
2025.04.12-20:01:09.85 - <debug> Registered op fpga_parallel from plugin noop
2025.04.12-20:01:09.85 - <debug> Registered op fpga_mmult from plugin noop
2025.04.12-20:01:09.85 - <debug> Registered op exec_with_resource from plugin noop
2025.04.12-20:01:09.85 - <debug> Registered op torch_jitload_forward from plugin noop
2025.04.12-20:01:09.85 - <debug> Registered op torch_sgemm from plugin noop
2025.04.12-20:01:09.85 - <debug> Registered op opencv from plugin noop
2025.04.12-20:01:09.85 - <debug> Registered op tflite_session_load from plugin noop
2025.04.12-20:01:09.85 - <debug> Registered op tflite_session_run from plugin noop
2025.04.12-20:01:09.85 - <debug> Registered op tflite_session_delete from plugin noop
2025.04.12-20:01:09.85 - <debug> Loaded plugin noop from libvaccel-noop.so
2025.04.12-20:01:16.73 - <debug> New rundir for session 1: /run/user/0/vaccel/u05Rjf/session.1
2025.04.12-20:01:16.73 - <debug> Initialized session 1
2025.04.12-20:01:16.73 - <debug> session:1 Looking for plugin implementing VACCEL_OP_IMAGE_CLASSIFY
2025.04.12-20:01:16.73 - <debug> Returning func from hint plugin noop
2025.04.12-20:01:16.73 - <debug> Found implementation in noop plugin
2025.04.12-20:01:16.73 - <debug> [noop] Calling Image classification for session 1
2025.04.12-20:01:16.73 - <debug> [noop] Dumping arguments for Image classification:
2025.04.12-20:01:16.73 - <debug> [noop] model: (null)
2025.04.12-20:01:16.73 - <debug> [noop] len_img: 79281
2025.04.12-20:01:16.73 - <debug> [noop] len_out_text: 512
2025.04.12-20:01:16.73 - <debug> [noop] len_out_imgname: 512
2025.04.12-20:01:16.73 - <debug> [noop] will return a dummy result
2025.04.12-20:01:16.73 - <debug> [noop] will return a dummy result
2025.04.12-20:01:16.73 - <debug> Released session 1
Initialized session with id: 1
classification tags: This is a dummy classification tag!
classification imagename: This is a dummy imgname!
2025.04.12-20:01:17.06 - <debug> Cleaning up vAccel
2025.04.12-20:01:17.06 - <debug> Cleaning up sessions
2025.04.12-20:01:17.06 - <debug> Cleaning up resources
2025.04.12-20:01:17.06 - <debug> Cleaning up plugins
2025.04.12-20:01:17.06 - <debug> Unregistered plugin noop
```

///

/// tab | ARM (64-bit)

```console
$ cd vm-artifacts
$ docker run --rm --device=/dev/kvm -it \
      --mount type=bind,source="$(pwd)",destination=/data \
      harbor.nbfc.io/nubificus/qemu-vaccel \
      -r rootfs.img --drive-cache -k Image* \
      --cmdline-append "console=ttyAMA0,115200" \
      -M virt --no-pci --vcpus 2 -m 2048 \
      -c "classify /usr/local/share/vaccel/images/example.jpg"
2025.04.12-20:01:09.85 - <debug> Initializing vAccel
2025.04.12-20:01:09.85 - <info> vAccel 0.6.1-194-19056528
2025.04.12-20:01:09.85 - <debug> Config:
2025.04.12-20:01:09.85 - <debug>   plugins = libvaccel-noop.so
2025.04.12-20:01:09.85 - <debug>   log_level = debug
2025.04.12-20:01:09.85 - <debug>   log_file = (null)
2025.04.12-20:01:09.85 - <debug>   profiling_enabled = false
2025.04.12-20:01:09.85 - <debug>   version_ignore = false
2025.04.12-20:01:09.85 - <debug> Created top-level rundir: /run/user/0/vaccel/u05Rjf
2025.04.12-20:01:09.85 - <info> Registered plugin noop 0.6.1-194-19056528
2025.04.12-20:01:09.85 - <debug> Registered op noop from plugin noop
2025.04.12-20:01:09.85 - <debug> Registered op blas_sgemm from plugin noop
2025.04.12-20:01:09.85 - <debug> Registered op image_classify from plugin noop
2025.04.12-20:01:09.85 - <debug> Registered op image_detect from plugin noop
2025.04.12-20:01:09.85 - <debug> Registered op image_segment from plugin noop
2025.04.12-20:01:09.85 - <debug> Registered op image_pose from plugin noop
2025.04.12-20:01:09.85 - <debug> Registered op image_depth from plugin noop
2025.04.12-20:01:09.85 - <debug> Registered op exec from plugin noop
2025.04.12-20:01:09.85 - <debug> Registered op tf_session_load from plugin noop
2025.04.12-20:01:09.85 - <debug> Registered op tf_session_run from plugin noop
2025.04.12-20:01:09.85 - <debug> Registered op tf_session_delete from plugin noop
2025.04.12-20:01:09.85 - <debug> Registered op minmax from plugin noop
2025.04.12-20:01:09.85 - <debug> Registered op fpga_arraycopy from plugin noop
2025.04.12-20:01:09.85 - <debug> Registered op fpga_vectoradd from plugin noop
2025.04.12-20:01:09.85 - <debug> Registered op fpga_parallel from plugin noop
2025.04.12-20:01:09.85 - <debug> Registered op fpga_mmult from plugin noop
2025.04.12-20:01:09.85 - <debug> Registered op exec_with_resource from plugin noop
2025.04.12-20:01:09.85 - <debug> Registered op torch_jitload_forward from plugin noop
2025.04.12-20:01:09.85 - <debug> Registered op torch_sgemm from plugin noop
2025.04.12-20:01:09.85 - <debug> Registered op opencv from plugin noop
2025.04.12-20:01:09.85 - <debug> Registered op tflite_session_load from plugin noop
2025.04.12-20:01:09.85 - <debug> Registered op tflite_session_run from plugin noop
2025.04.12-20:01:09.85 - <debug> Registered op tflite_session_delete from plugin noop
2025.04.12-20:01:09.85 - <debug> Loaded plugin noop from libvaccel-noop.so
2025.04.12-20:01:16.73 - <debug> New rundir for session 1: /run/user/0/vaccel/u05Rjf/session.1
2025.04.12-20:01:16.73 - <debug> Initialized session 1
2025.04.12-20:01:16.73 - <debug> session:1 Looking for plugin implementing VACCEL_OP_IMAGE_CLASSIFY
2025.04.12-20:01:16.73 - <debug> Returning func from hint plugin noop
2025.04.12-20:01:16.73 - <debug> Found implementation in noop plugin
2025.04.12-20:01:16.73 - <debug> [noop] Calling Image classification for session 1
2025.04.12-20:01:16.73 - <debug> [noop] Dumping arguments for Image classification:
2025.04.12-20:01:16.73 - <debug> [noop] model: (null)
2025.04.12-20:01:16.73 - <debug> [noop] len_img: 79281
2025.04.12-20:01:16.73 - <debug> [noop] len_out_text: 512
2025.04.12-20:01:16.73 - <debug> [noop] len_out_imgname: 512
2025.04.12-20:01:16.73 - <debug> [noop] will return a dummy result
2025.04.12-20:01:16.73 - <debug> [noop] will return a dummy result
2025.04.12-20:01:16.73 - <debug> Released session 1
Initialized session with id: 1
classification tags: This is a dummy classification tag!
classification imagename: This is a dummy imgname!
2025.04.12-20:01:17.06 - <debug> Cleaning up vAccel
2025.04.12-20:01:17.06 - <debug> Cleaning up sessions
2025.04.12-20:01:17.06 - <debug> Cleaning up resources
2025.04.12-20:01:17.06 - <debug> Cleaning up plugins
2025.04.12-20:01:17.06 - <debug> Unregistered plugin noop
```
