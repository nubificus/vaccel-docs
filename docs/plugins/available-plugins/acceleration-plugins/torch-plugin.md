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
$ VACCEL_PLUGINS=libvaccel-torch.so VACCEL_TORCH_LABELS=/usr/local/share/vaccel/labels/imagenet.txt VACCEL_LOG_LEVEL=4 classify /usr/local/share/vaccel/images/example.jpg 1 https://s3.nbfc.io/torch/resnet18.pt
2026.05.02-23:20:15.00 - <debug> Initializing vAccel
2026.05.02-23:20:15.00 - <info> vAccel 0.8.0
2026.05.02-23:20:15.00 - <debug> Config:
2026.05.02-23:20:15.00 - <debug>   plugins = libvaccel-torch.so
2026.05.02-23:20:15.00 - <debug>   log_level = debug
2026.05.02-23:20:15.00 - <debug>   log_file = (null)
2026.05.02-23:20:15.00 - <debug>   profiling_enabled = false
2026.05.02-23:20:15.00 - <debug>   version_ignore = false
2026.05.02-23:20:15.00 - <debug> Created top-level rundir: /run/user/0/vaccel/0QlxRy
2026.05.02-23:20:15.35 - <info> Registered plugin torch 0.3.0+vaccel.0.8.0
2026.05.02-23:20:15.35 - <debug> Registered op torch_model_load from plugin torch
2026.05.02-23:20:15.35 - <debug> Registered op torch_model_run from plugin torch
2026.05.02-23:20:15.35 - <debug> Registered op torch_sgemm from plugin torch
2026.05.02-23:20:15.35 - <debug> Registered op image_classify from plugin torch
2026.05.02-23:20:15.35 - <debug> Loaded plugin torch from libvaccel-torch.so
2026.05.02-23:20:15.35 - <debug> New rundir for session 1: /run/user/0/vaccel/0QlxRy/session.1
2026.05.02-23:20:15.35 - <debug> Initialized session 1 with plugin torch
Initialized session with id: 1
2026.05.02-23:20:15.35 - <debug> Initialized resource 1
2026.05.02-23:20:15.35 - <debug> New rundir for resource 1: /run/user/0/vaccel/0QlxRy/resource.1
2026.05.02-23:20:15.35 - <debug> Downloading https://s3.nbfc.io/torch/resnet18.pt
2026.05.02-23:20:16.51 - <debug> Downloaded: 44.7 MB of 44.7 MB (100.0%) | Speed: 38.52 MB/sec
2026.05.02-23:20:16.51 - <debug> Download completed successfully
2026.05.02-23:20:16.51 - <debug> session:1 Registered resource 1
2026.05.02-23:20:16.51 - <debug> session:1 Looking for func implementing op image_classify
2026.05.02-23:20:16.51 - <debug> Returning func for op image_classify from plugin torch
2026.05.02-23:20:16.51 - <warn> [torch] Registered model is not loaded; loading...
2026.05.02-23:20:16.51 - <debug> [torch] Running in CPU mode
2026.05.02-23:20:16.51 - <debug> [torch] Loading model from /run/user/0/vaccel/0QlxRy/resource.1/resnet18.pt
2026.05.02-23:20:16.61 - <debug> [torch] Loaded registered model
2026.05.02-23:20:16.63 - <debug> [torch] Disabling graph executor optimization
2026.05.02-23:20:16.69 - <debug> [torch] Prediction: banana 87.34%
classification tags: banana
classification imagename: PLACEHOLDER
2026.05.02-23:20:16.69 - <debug> session:1 Unregistered resource 1
2026.05.02-23:20:16.69 - <debug> Removing file /run/user/0/vaccel/0QlxRy/resource.1/resnet18.pt
2026.05.02-23:20:16.70 - <debug> Released resource 1
2026.05.02-23:20:16.70 - <debug> Released session 1
2026.05.02-23:20:16.78 - <debug> Cleaning up vAccel
2026.05.02-23:20:16.78 - <debug> Cleaning up sessions
2026.05.02-23:20:16.78 - <debug> Cleaning up resources
2026.05.02-23:20:16.78 - <debug> Cleaning up plugins
2026.05.02-23:20:16.78 - <debug> Unregistered plugin torch
```

To run a torch inference example with the generic `jitload_forward` operation:

```console
$ VACCEL_PLUGINS=libvaccel-torch.so VACCEL_TORCH_LABELS=/usr/local/share/vaccel/labels/imagenet.txt VACCEL_LOG_LEVEL=4 torch_inference /usr/local/share/vaccel/images/example.jpg https://s3.nbfc.io/torch/resnet18.pt "$VACCEL_TORCH_LABELS"
2026.05.02-23:20:16.81 - <debug> Initializing vAccel
2026.05.02-23:20:16.81 - <info> vAccel 0.8.0
2026.05.02-23:20:16.81 - <debug> Config:
2026.05.02-23:20:16.81 - <debug>   plugins = libvaccel-torch.so
2026.05.02-23:20:16.81 - <debug>   log_level = debug
2026.05.02-23:20:16.81 - <debug>   log_file = (null)
2026.05.02-23:20:16.81 - <debug>   profiling_enabled = false
2026.05.02-23:20:16.81 - <debug>   version_ignore = false
2026.05.02-23:20:16.81 - <debug> Created top-level rundir: /run/user/0/vaccel/bZnzXV
2026.05.02-23:20:17.16 - <info> Registered plugin torch 0.3.0+vaccel.0.8.0
2026.05.02-23:20:17.16 - <debug> Registered op torch_model_load from plugin torch
2026.05.02-23:20:17.16 - <debug> Registered op torch_model_run from plugin torch
2026.05.02-23:20:17.16 - <debug> Registered op torch_sgemm from plugin torch
2026.05.02-23:20:17.16 - <debug> Registered op image_classify from plugin torch
2026.05.02-23:20:17.16 - <debug> Loaded plugin torch from libvaccel-torch.so
2026.05.02-23:20:17.16 - <debug> Initialized resource 1
Initialized model resource 1
2026.05.02-23:20:17.16 - <debug> New rundir for session 1: /run/user/0/vaccel/bZnzXV/session.1
2026.05.02-23:20:17.16 - <debug> Initialized session 1 with plugin torch
Initialized vAccel session 1
2026.05.02-23:20:17.16 - <debug> New rundir for resource 1: /run/user/0/vaccel/bZnzXV/resource.1
2026.05.02-23:20:17.16 - <debug> Downloading https://s3.nbfc.io/torch/resnet18.pt
2026.05.02-23:20:18.19 - <debug> Downloaded: 44.7 MB of 44.7 MB (100.0%) | Speed: 43.19 MB/sec
2026.05.02-23:20:18.19 - <debug> Download completed successfully
2026.05.02-23:20:18.19 - <debug> session:1 Registered resource 1
2026.05.02-23:20:18.19 - <debug> session:1 Looking for func implementing op torch_model_load
2026.05.02-23:20:18.19 - <debug> Returning func for op torch_model_load from plugin torch
2026.05.02-23:20:18.19 - <debug> [torch] Running in CPU mode
2026.05.02-23:20:18.20 - <debug> [torch] Loading model from /run/user/0/vaccel/bZnzXV/resource.1/resnet18.pt
2026.05.02-23:20:18.30 - <debug> session:1 Looking for func implementing op torch_model_run
2026.05.02-23:20:18.30 - <debug> Returning func for op torch_model_run from plugin torch
2026.05.02-23:20:18.30 - <debug> [torch] session:1 Jitload & Forward Process
2026.05.02-23:20:18.30 - <debug> [torch] Model: /run/user/0/vaccel/bZnzXV/resource.1/resnet18.pt
2026.05.02-23:20:18.30 - <debug> [torch] Disabling graph executor optimization
Success!
Result Tensor :
Output tensor => type:7 nr_dims:2 size:4000B
Prediction: banana
2026.05.02-23:20:18.36 - <debug> session:1 Unregistered resource 1
2026.05.02-23:20:18.36 - <debug> Released session 1
2026.05.02-23:20:18.36 - <debug> Removing file /run/user/0/vaccel/bZnzXV/resource.1/resnet18.pt
2026.05.02-23:20:18.37 - <debug> Released resource 1
2026.05.02-23:20:18.45 - <debug> Cleaning up vAccel
2026.05.02-23:20:18.45 - <debug> Cleaning up sessions
2026.05.02-23:20:18.45 - <debug> Cleaning up resources
2026.05.02-23:20:18.45 - <debug> Cleaning up plugins
2026.05.02-23:20:18.45 - <debug> Unregistered plugin torch
```
