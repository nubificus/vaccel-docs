# Torch Plugin

The Torch plugin for vAccel implements basic [PyTorch](https://pytorch.org) C++
API (LibTorch) support for vAccel operations.

## Supported operations

- [Image classification](../../../api/api-reference/operations.md#image-classification)
- [JIT loading and forwarding](../../../api/api-reference/operations.md#jit-loading-and-forwarding)
- [Matrix-to-matrix multiplication](../../../api/api-reference/operations.md#matrix-to-matrix-multiplication_1)

## Installing PyTorch C/C++ API files (LibTorch)

You can find instructions on how to install the required files
[here](../../../useful-docs/pytorch.md). The rest of this guide assumes PyTorch
is installed at `/opt/pytorch` and its' libraries are at `/opt/pytorch/lib`.

## Installing the plugin

You can get the latest Torch plugin binary release from the
[Releases](https://github.com/nubificus/vaccel/releases) page of the vAccel
repository. Releases include binaries for x86_64/aarch64 Ubuntu-based systems.

### TAR

To install the TAR binary package of the latest Torch plugin release:

/// tab | x86

```sh
wget https://github.com/nubificus/vaccel/releases/download/v[[ versions.vaccel ]]/vaccel-torch_[[ versions.plugins.torch ]]_amd64.tar.gz
# Replace '/usr/local' below with the desired installation prefix
tar xfv vaccel-torch_[[ versions.plugins.torch ]]_amd64.tar.gz --strip-components=2 -C /usr/local
# Update pkg-config files with the correct prefix
find /usr/local -name "vaccel-torch.pc" -exec sed -i 's:^\(prefix=\).*:\1/usr/local:g' {} \;
```

///

/// tab | ARM (64-bit)

```sh
wget https://github.com/nubificus/vaccel/releases/download/v[[ versions.vaccel ]]/vaccel-torch_[[ versions.plugins.torch ]]_arm64.tar.gz
# Replace '/usr/local' below with the desired installation prefix
tar xfv vaccel-torch_[[ versions.plugins.torch ]]_arm64.tar.gz --strip-components=2 -C /usr/local
# Update pkg-config files with the correct prefix
find /usr/local -name "vaccel-torch.pc" -exec sed -i 's:^\(prefix=\).*:\1/usr/local:g' {} \;
```

///

### Latest artifacts

You can also find prebuilt artifacts of the latest Torch plugin revision at:

/// tab | x86

```sh
# TAR
https://s3.nbfc.io/nbfc-assets/github/vaccel/plugins/torch/rev/main/x86_64/release/vaccel-torch-latest-bin.tar.gz
```

///

/// tab | ARM (64-bit)

```sh
# TAR
https://s3.nbfc.io/nbfc-assets/github/vaccel/plugins/torch/rev/main/aarch64/release/vaccel-torch-latest-bin.tar.gz
```

///

## Usage

To specify Torch plugin as the selected plugin for vAccel execution:

```sh
export VACCEL_PLUGINS=libvaccel-torch.so
```

Ensure LibTorch, vAccel and the Torch plugin libraries are in the library search
paths before trying to use the plugin.

To run image classification you will also need to specify a file with labels
using `VACCEL_TORCH_LABELS`. vAccel includes an file imagenet labels file.
Assuming vAccel is installed at `/usr/local`, you can specify the file with:

```sh
export VACCEL_TORCH_LABELS=/usr/local/share/vaccel/labels/imagenet.txt
```

If vAccel is installed using the DEB package (at `/usr`) you can omit the
variable.

## Running an example

Export the necessary variables:

```sh
export VACCEL_PLUGINS=libvaccel-torch.so
export VACCEL_TORCH_LABELS=/usr/local/share/vaccel/labels/imagenet.txt
# Optionally, for verbose output
export VACCEL_LOG_LEVEL=4
```

Assuming vAccel is installed at `/usr/local`, you can run an image
classification with a ResNet model from `https://s3.nbfc.io/torch/resnet18.pt`
with:

```console
$ classify /usr/local/share/vaccel/images/example.jpg 1 \
      https://s3.nbfc.io/torch/resnet18.pt
2025.04.11-15:46:20.07 - <debug> Initializing vAccel
2025.04.11-15:46:20.07 - <info> vAccel 0.6.1-194-19056528
2025.04.11-15:46:20.07 - <debug> Config:
2025.04.11-15:46:20.07 - <debug>   plugins = libvaccel-torch.so
2025.04.11-15:46:20.07 - <debug>   log_level = debug
2025.04.11-15:46:20.07 - <debug>   log_file = (null)
2025.04.11-15:46:20.07 - <debug>   profiling_enabled = false
2025.04.11-15:46:20.07 - <debug>   version_ignore = false
2025.04.11-15:46:20.07 - <debug> Created top-level rundir: /run/user/1002/vaccel/w8BHSP
2025.04.11-15:46:20.53 - <info> Registered plugin torch 0.1.0-25-ab85fa03
2025.04.11-15:46:20.53 - <debug> Registered op torch_jitload_forward from plugin torch
2025.04.11-15:46:20.53 - <debug> Registered op torch_sgemm from plugin torch
2025.04.11-15:46:20.53 - <debug> Registered op image_classify from plugin torch
2025.04.11-15:46:20.53 - <debug> Loaded plugin torch from libvaccel-torch.so
2025.04.11-15:46:20.53 - <debug> New rundir for session 1: /run/user/1002/vaccel/w8BHSP/session.1
2025.04.11-15:46:20.53 - <debug> Initialized session 1
Initialized session with id: 1
2025.04.11-15:46:20.53 - <debug> Initialized resource 1
2025.04.11-15:46:20.53 - <debug> New rundir for resource 1: /run/user/1002/vaccel/w8BHSP/resource.1
2025.04.11-15:46:20.53 - <debug> Downloading https://s3.nbfc.io/torch/resnet18.pt
...
2025.04.11-15:48:41.53 - <debug> Download completed successfully
2025.04.11-15:48:41.53 - <debug> session:1 Registered resource 1
2025.04.11-15:48:41.53 - <debug> session:1 Looking for plugin implementing VACCEL_OP_IMAGE_CLASSIFY
2025.04.11-15:48:41.53 - <debug> Returning func from hint plugin torch
2025.04.11-15:48:41.53 - <debug> Found implementation in torch plugin
2025.04.11-15:48:41.73 - <debug> [torch] Model loaded successfully from: /run/user/1002/vaccel/w8BHSP/resource.1/resnet18.pt
2025.04.11-15:48:41.89 - <debug> [torch] Prediction: banana
classification tags: banana
classification imagename: PLACEHOLDER
2025.04.11-15:48:41.91 - <debug> session:1 Unregistered resource 1
2025.04.11-15:48:41.91 - <debug> Removing file /run/user/1002/vaccel/w8BHSP/resource.1/resnet18.pt
2025.04.11-15:48:41.92 - <debug> Released resource 1
2025.04.11-15:48:41.92 - <debug> Released session 1
2025.04.11-15:48:42.06 - <debug> Cleaning up vAccel
2025.04.11-15:48:42.06 - <debug> Cleaning up sessions
2025.04.11-15:48:42.06 - <debug> Cleaning up resources
2025.04.11-15:48:42.06 - <debug> Cleaning up plugins
2025.04.11-15:48:42.06 - <debug> Unregistered plugin torch
```

To run a torch inference example with the generic `jitload_forward` operation:

```console
$ torch_inference /usr/local/share/vaccel/images/example.jpg \
      https://s3.nbfc.io/torch/resnet18.pt \
      "${VACCEL_TORCH_LABELS}"
2025.04.11-15:59:42.95 - <debug> Initializing vAccel
2025.04.11-15:59:42.95 - <info> vAccel 0.6.1-194-19056528
2025.04.11-15:59:42.95 - <debug> Config:
2025.04.11-15:59:42.95 - <debug>   plugins = libvaccel-torch.so
2025.04.11-15:59:42.95 - <debug>   log_level = debug
2025.04.11-15:59:42.95 - <debug>   log_file = (null)
2025.04.11-15:59:42.95 - <debug>   profiling_enabled = false
2025.04.11-15:59:42.95 - <debug>   version_ignore = false
2025.04.11-15:59:42.95 - <debug> Created top-level rundir: /run/user/1002/vaccel/fEe2aO
2025.04.11-15:59:43.41 - <info> Registered plugin torch 0.1.0-25-ab85fa03
2025.04.11-15:59:43.41 - <debug> Registered op torch_jitload_forward from plugin torch
2025.04.11-15:59:43.41 - <debug> Registered op torch_sgemm from plugin torch
2025.04.11-15:59:43.41 - <debug> Registered op image_classify from plugin torch
2025.04.11-15:59:43.41 - <debug> Loaded plugin torch from libvaccel-torch.so
2025.04.11-15:59:43.41 - <debug> Initialized resource 1
Initialized model resource 1
2025.04.11-15:59:43.41 - <debug> New rundir for session 1: /run/user/1002/vaccel/fEe2aO/session.1
2025.04.11-15:59:43.41 - <debug> Initialized session 1
Initialized vAccel session 1
2025.04.11-15:59:43.41 - <debug> New rundir for resource 1: /run/user/1002/vaccel/fEe2aO/resource.1
2025.04.11-15:59:43.41 - <debug> Downloading https://s3.nbfc.io/torch/resnet18.pt
...
2025.04.11-16:05:21.23 - <debug> Download completed successfully
2025.04.11-16:05:21.23 - <debug> session:1 Registered resource 1
2025.04.11-16:05:21.27 - <debug> session:1 Looking for plugin implementing torch_jitload_forward operation
2025.04.11-16:05:21.27 - <debug> Returning func from hint plugin torch
2025.04.11-16:05:21.27 - <debug> Found implementation in torch plugin
2025.04.11-16:05:21.27 - <debug> [torch] session:1 Jitload & Forward Process
2025.04.11-16:05:21.27 - <debug> [torch] Model: /run/user/1002/vaccel/1nB5aC/resource.1/resnet18.pt
2025.04.11-16:05:21.27 - <debug> [torch] CUDA not available, running in CPU mode
Success!
Result Tensor :
Output tensor => type:7 nr_dims:2
size: 4000 B
Prediction: banana
2025.04.11-16:05:21.50 - <debug> session:1 Unregistered resource 1
2025.04.11-16:05:21.50 - <debug> Released session 1
2025.04.11-16:05:21.50 - <debug> Removing file /run/user/1002/vaccel/1nB5aC/resource.1/resnet18.pt
2025.04.11-16:05:21.51 - <debug> Released resource 1
2025.04.11-16:05:21.61 - <debug> Cleaning up vAccel
2025.04.11-16:05:21.61 - <debug> Cleaning up sessions
2025.04.11-16:05:21.61 - <debug> Cleaning up resources
2025.04.11-16:05:21.61 - <debug> Cleaning up plugins
2025.04.11-16:05:21.61 - <debug> Unregistered plugin torch
```
