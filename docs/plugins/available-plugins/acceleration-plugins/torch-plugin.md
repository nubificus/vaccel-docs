# Torch Plugin

The Torch plugin for vAccel implements basic [PyTorch](https://pytorch.org) C++
API (LibTorch) support for vAccel operations.

## Supported operations

- [Image classification](../../../api/api-reference/operations.md#image-classification)
- [Torch model load](../../../api/api-reference/operations.md#torch-model-load)
- [Torch model run](../../../api/api-reference/operations.md#torch-model-run)
- [Torch matrix-to-matrix multiplication](../../../api/api-reference/operations.md#torch-matrix-to-matrix-multiplication)

## Installing PyTorch C/C++ API files (LibTorch)

You can find instructions on how to install the required files on the [Build and
Install PyTorch] page. The rest of this guide assumes PyTorch is installed at
`/opt/pytorch` and its' libraries are at `/opt/pytorch/lib`.

[Build and Install PyTorch]: ../../../useful-docs/build-and-install-pytorch.md

## Installing the plugin

You can get the latest Torch plugin binary release from the
[Releases](https://github.com/nubificus/vaccel/releases) page of the vAccel
repository. Releases include binaries for x86_64/aarch64 Ubuntu-based systems.

### Requirements

The prebuilt Torch plugin binaries depend on
[libstb](https://github.com/nothings/stb/). You can install it with:

```sh
sudo apt install libstb0
```

### TAR

To install the TAR binary package of the latest Torch plugin release:

/// tab | x86

```sh
wget https://github.com/nubificus/vaccel/releases/download/v[[ versions.vaccel ]]/vaccel-torch_[[ versions.plugins.torch ]]_x86_64.tar.gz
# Replace '/usr/local' below with the desired installation prefix
tar xfv vaccel-torch_[[ versions.plugins.torch ]]_x86_64.tar.gz --strip-components=2 -C /usr/local
# Update pkg-config files with the correct prefix
find /usr/local -name "vaccel-torch.pc" -exec sed -i 's:^\(prefix=\).*:\1/usr/local:g' {} \;
```

///

/// tab | ARM (64-bit)

```sh
wget https://github.com/nubificus/vaccel/releases/download/v[[ versions.vaccel ]]/vaccel-torch_[[ versions.plugins.torch ]]_aarch64.tar.gz
# Replace '/usr/local' below with the desired installation prefix
tar xfv vaccel-torch_[[ versions.plugins.torch ]]_aarch64.tar.gz --strip-components=2 -C /usr/local
# Update pkg-config files with the correct prefix
find /usr/local -name "vaccel-torch.pc" -exec sed -i 's:^\(prefix=\).*:\1/usr/local:g' {} \;
```

///

### Latest artifacts

You can also find prebuilt artifacts of the latest Torch plugin revision at:

/// tab | x86

```sh
# TAR
https://s3.nbfc.io/nbfc-assets/github/vaccel/plugins/torch/rev/main/x86_64/release/vaccel-torch_latest_x86_64.tar.gz
```

///

/// tab | ARM (64-bit)

```sh
# TAR
https://s3.nbfc.io/nbfc-assets/github/vaccel/plugins/torch/rev/main/aarch64/release/vaccel-torch_latest_aarch64.tar.gz
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
2026.04.29-15:19:39.63 - <debug> Initializing vAccel
2026.04.29-15:19:39.63 - <info> vAccel 0.7.1-93-ebc23b1f
2026.04.29-15:19:39.63 - <debug> Config:
2026.04.29-15:19:39.63 - <debug>   plugins = libvaccel-torch.so
2026.04.29-15:19:39.63 - <debug>   log_level = debug
2026.04.29-15:19:39.63 - <debug>   log_file = (null)
2026.04.29-15:19:39.63 - <debug>   profiling_enabled = false
2026.04.29-15:19:39.63 - <debug>   version_ignore = false
2026.04.29-15:19:39.74 - <debug> Created top-level rundir: /run/user/0/vaccel/uscxgC
2026.04.29-15:19:39.95 - <info> Registered plugin torch 0.2.1-27-abc7d840
2026.04.29-15:19:39.95 - <debug> Registered op torch_model_load from plugin torch
2026.04.29-15:19:39.95 - <debug> Registered op torch_model_run from plugin torch
2026.04.29-15:19:39.95 - <debug> Registered op torch_sgemm from plugin torch
2026.04.29-15:19:39.95 - <debug> Registered op image_classify from plugin torch
2026.04.29-15:19:39.95 - <debug> Loaded plugin torch from libvaccel-torch.so
2026.04.29-15:19:39.95 - <debug> New rundir for session 1: /run/user/0/vaccel/uscxgC/session.1
2026.04.29-15:19:39.95 - <debug> Initialized session 1 with plugin torch
Initialized session with id: 1
2026.04.29-15:19:39.95 - <debug> Initialized resource 1
2026.04.29-15:19:39.95 - <debug> New rundir for resource 1: /run/user/0/vaccel/uscxgC/resource.1
2026.04.29-15:19:39.95 - <debug> Downloading https://s3.nbfc.io/torch/resnet18.pt
2026.04.29-15:19:40.99 - <debug> Downloaded: 44.7 MB of 44.7 MB (100.0%) | Speed: 43.19 MB/sec
2026.04.29-15:19:40.99 - <debug> Download completed successfully
2026.04.29-15:19:40.99 - <debug> session:1 Registered resource 1
2026.04.29-15:19:40.99 - <debug> session:1 Looking for func implementing op image_classify
2026.04.29-15:19:40.99 - <debug> Returning func for op image_classify from plugin torch
2026.04.29-15:19:40.99 - <warn> [torch] Registered model is not loaded; loading...
2026.04.29-15:19:40.99 - <debug> [torch] Running in CPU mode
2026.04.29-15:19:40.99 - <debug> [torch] Loading model from /run/user/0/vaccel/uscxgC/resource.1/resnet18.pt
2026.04.29-15:19:41.05 - <debug> [torch] Loaded registered model
2026.04.29-15:19:41.06 - <debug> [torch] Disabling graph executor optimization
2026.04.29-15:19:41.09 - <debug> [torch] Prediction: banana 87.34%
classification tags: banana
classification imagename: PLACEHOLDER
2026.04.29-15:19:41.09 - <debug> session:1 Unregistered resource 1
2026.04.29-15:19:41.09 - <debug> Removing file /run/user/0/vaccel/uscxgC/resource.1/resnet18.pt
2026.04.29-15:19:41.10 - <debug> Released resource 1
2026.04.29-15:19:41.10 - <debug> Released session 1
2026.04.29-15:19:41.16 - <debug> Cleaning up vAccel
2026.04.29-15:19:41.16 - <debug> Cleaning up sessions
2026.04.29-15:19:41.16 - <debug> Cleaning up resources
2026.04.29-15:19:41.16 - <debug> Cleaning up plugins
2026.04.29-15:19:41.16 - <debug> Unregistered plugin torch
```

To run a torch inference example with the generic `jitload_forward` operation:

```console
$ torch_inference /usr/local/share/vaccel/images/example.jpg \
      https://s3.nbfc.io/torch/resnet18.pt \
      "${VACCEL_TORCH_LABELS}"
2026.04.29-15:19:57.82 - <debug> Initializing vAccel
2026.04.29-15:19:57.82 - <info> vAccel 0.7.1-93-ebc23b1f
2026.04.29-15:19:57.82 - <debug> Config:
2026.04.29-15:19:57.82 - <debug>   plugins = libvaccel-torch.so
2026.04.29-15:19:57.82 - <debug>   log_level = debug
2026.04.29-15:19:57.82 - <debug>   log_file = (null)
2026.04.29-15:19:57.82 - <debug>   profiling_enabled = false
2026.04.29-15:19:57.82 - <debug>   version_ignore = false
2026.04.29-15:19:57.82 - <debug> Created top-level rundir: /run/user/0/vaccel/d2iSTG
2026.04.29-15:19:58.01 - <info> Registered plugin torch 0.2.1-27-abc7d840
2026.04.29-15:19:58.01 - <debug> Registered op torch_model_load from plugin torch
2026.04.29-15:19:58.01 - <debug> Registered op torch_model_run from plugin torch
2026.04.29-15:19:58.01 - <debug> Registered op torch_sgemm from plugin torch
2026.04.29-15:19:58.01 - <debug> Registered op image_classify from plugin torch
2026.04.29-15:19:58.01 - <debug> Loaded plugin torch from libvaccel-torch.so
2026.04.29-15:19:58.01 - <debug> Initialized resource 1
Initialized model resource 1
2026.04.29-15:19:58.01 - <debug> New rundir for session 1: /run/user/0/vaccel/d2iSTG/session.1
2026.04.29-15:19:58.01 - <debug> Initialized session 1 with plugin torch
Initialized vAccel session 1
2026.04.29-15:19:58.01 - <debug> New rundir for resource 1: /run/user/0/vaccel/d2iSTG/resource.1
2026.04.29-15:19:58.01 - <debug> Downloading https://s3.nbfc.io/torch/resnet18.pt
2026.04.29-15:19:59.04 - <debug> Downloaded: 44.7 MB of 44.7 MB (100.0%) | Speed: 43.19 MB/sec
2026.04.29-15:19:59.04 - <debug> Download completed successfully
2026.04.29-15:19:59.04 - <debug> session:1 Registered resource 1
2026.04.29-15:19:59.04 - <debug> session:1 Looking for func implementing op torch_model_load
2026.04.29-15:19:59.04 - <debug> Returning func for op torch_model_load from plugin torch
2026.04.29-15:19:59.04 - <debug> [torch] Running in CPU mode
2026.04.29-15:19:59.05 - <debug> [torch] Loading model from /run/user/0/vaccel/d2iSTG/resource.1/resnet18.pt
2026.04.29-15:19:59.12 - <debug> session:1 Looking for func implementing op torch_model_run
2026.04.29-15:19:59.12 - <debug> Returning func for op torch_model_run from plugin torch
2026.04.29-15:19:59.12 - <debug> [torch] session:1 Jitload & Forward Process
2026.04.29-15:19:59.12 - <debug> [torch] Model: /run/user/0/vaccel/d2iSTG/resource.1/resnet18.pt
2026.04.29-15:19:59.12 - <debug> [torch] Disabling graph executor optimization
Success!
Result Tensor :
Output tensor => type:7 nr_dims:2 size:4000B
Prediction: banana
2026.04.29-15:19:59.16 - <debug> session:1 Unregistered resource 1
2026.04.29-15:19:59.16 - <debug> Released session 1
2026.04.29-15:19:59.16 - <debug> Removing file /run/user/0/vaccel/d2iSTG/resource.1/resnet18.pt
2026.04.29-15:19:59.17 - <debug> Released resource 1
2026.04.29-15:19:59.23 - <debug> Cleaning up vAccel
2026.04.29-15:19:59.23 - <debug> Cleaning up sessions
2026.04.29-15:19:59.23 - <debug> Cleaning up resources
2026.04.29-15:19:59.23 - <debug> Cleaning up plugins
2026.04.29-15:19:59.23 - <debug> Unregistered plugin torch
```
