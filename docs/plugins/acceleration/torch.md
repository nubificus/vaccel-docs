# Torch Plugin

The Torch plugin for vAccel implements basic [PyTorch](https://pytorch.org) C++
API (LibTorch) support for vAccel operations.

## Supported operations

- [JIT loading and forwarding](../../api.md#jit-loading-and-forwarding)
- [Matrix-to-matrix multiplication](../../api.md#matrix-to-matrix-multiplication)
- [Image classification](../../api.md#image-classification)

## Install PyTorch C/C++ API files (LibTorch)

You can find instructions on how to install the required files
[here](../../pytorch.md). The rest of this guide assumes PyTorch is installed at
`/opt/pytorch` and its' libraries are at `/opt/pytorch/lib`.

## Install vAccel

Information about vAccel installation can be found [here](../../quickstart.md).
The rest of this guide assumes vAccel is installed at `/usr/local`.

## Install the plugin

Download the plugin for `x86_64`:

```sh
https://s3.nbfc.io/nbfc-assets/github/vaccel/plugins/torch/rev/main/x86_64/release/vaccel-torch-latest-bin.tar.gz
```

or `aarch64`:

```sh
https://s3.nbfc.io/nbfc-assets/github/vaccel/plugins/torch/rev/main/aarch64/release/vaccel-torch-latest-bin.tar.gz
```

and extract to the desired installation directory, ie. to install in
`/usr/local`:

```sh
sudo tar xfv vaccel-torch-latest-bin.tar.gz --strip-components=2 -C /usr/local
```

## Run an example

After having installed PyTorch, vAccel and the Torch plugin you are ready to run
an image classification example.

Ensure PyTorch libraries are in the library search path:

```sh
export LD_LIBRARY_PATH=/opt/pytorch/lib
```

If vAccel and/or the Torch plugin are installed in a non-standard library path
you will also need to include them in the `LD_LIBRARY_PATH`.

Define the Torch plugin as the selected plugin for vAccel execution:

```sh
export VACCEL_PLUGINS=libvaccel-torch.so
```

Alternatively, you can provide the full path to the plugin library, without
needing to have the plugin in your library search path:

```sh
export VACCEL_PLUGINS=/usr/local/lib/x86_64-linux-gnu/libvaccel-torch.so
```

Configure the vaccel log level for more verbose output:

```sh
export VACCEL_LOG_LEVEL=4
```

And finally run an image classification with a ResNet model from
`https://s3.nbfc.io/torch/resnet18.pt`:

```console
$ classify /usr/local/share/vaccel/images/example.jpg 1 \
      https://s3.nbfc.io/torch/resnet18.pt
2025.03.24-21:20:51.16 - <debug> Initializing vAccel
2025.03.24-21:20:51.16 - <info> vAccel 0.6.1-194-19056528
2025.03.24-21:20:51.16 - <debug> Config:
2025.03.24-21:20:51.16 - <debug>   plugins = libvaccel-torch.so
2025.03.24-21:20:51.16 - <debug>   log_level = debug
2025.03.24-21:20:51.16 - <debug>   log_file = (null)
2025.03.24-21:20:51.16 - <debug>   profiling_enabled = false
2025.03.24-21:20:51.16 - <debug>   version_ignore = false
2025.03.24-21:20:51.16 - <debug> Created top-level rundir: /run/user/1002/vaccel/SJ4uXX
2025.03.24-21:20:51.72 - <info> Registered plugin torch 0.1.0-22-7cf3d0e4
2025.03.24-21:20:51.72 - <debug> Registered op torch_jitload_forward from plugin torch
2025.03.24-21:20:51.72 - <debug> Registered op torch_sgemm from plugin torch
2025.03.24-21:20:51.72 - <debug> Registered op image_classify from plugin torch
2025.03.24-21:20:51.72 - <debug> Loaded plugin torch from libvaccel-torch.so
2025.03.24-21:20:51.72 - <debug> New rundir for session 1: /run/user/1002/vaccel/SJ4uXX/session.1
2025.03.24-21:20:51.72 - <debug> Initialized session 1
Initialized session with id: 1
2025.03.24-21:20:51.72 - <debug> Initialized resource 1
2025.03.24-21:20:51.72 - <debug> New rundir for resource 1: /run/user/1002/vaccel/SJ4uXX/resource.1
2025.03.24-21:20:51.72 - <debug> Downloading https://s3.nbfc.io/torch/mobilenet.pt
2025.03.24-21:20:56.72 - <debug> Downloaded: 5.8 MB of 13.7 MB (42.0%) | Speed: 1.15 MB/sec
2025.03.24-21:20:59.95 - <debug> Downloaded: 13.7 MB of 13.7 MB (100.0%) | Speed: 1.67 MB/sec
2025.03.24-21:20:59.95 - <debug> Download completed successfully
2025.03.24-21:20:59.95 - <debug> session:1 Registered resource 1
2025.03.24-21:20:59.95 - <debug> session:1 Looking for plugin implementing VACCEL_OP_IMAGE_CLASSIFY
2025.03.24-21:20:59.95 - <debug> Returning func from hint plugin torch
2025.03.24-21:20:59.95 - <debug> Found implementation in torch plugin
2025.03.24-21:21:00.40 - <debug> [torch] Model loaded successfully from: /run/user/1002/vaccel/SJ4uXX/resource.1/mobil
enet.pt
2025.03.24-21:21:00.86 - <debug> [torch] Prediction: banana
classification tags: banana
classification imagename: PLACEHOLDER
2025.03.24-21:21:00.89 - <debug> session:1 Unregistered resource 1
2025.03.24-21:21:00.89 - <debug> Removing file /run/user/1002/vaccel/SJ4uXX/resource.1/mobilenet.pt
2025.03.24-21:21:00.90 - <debug> Released resource 1
2025.03.24-21:21:00.90 - <debug> Released session 1
2025.03.24-21:21:01.02 - <debug> Cleaning up vAccel
2025.03.24-21:21:01.02 - <debug> Cleaning up sessions
2025.03.24-21:21:01.02 - <debug> Cleaning up resources
2025.03.24-21:21:01.02 - <debug> Cleaning up plugins
2025.03.24-21:21:01.02 - <debug> Unregistered plugin torch
```

To run a torch inference example with the generic `jitload_forward` operation:

```console
$ torch_inference /usr/local/share/vaccel/images/example.jpg \
      https://s3.nbfc.io/torch/resnet18.pt \
      /usr/local/share/vaccel/labels/imagenet.txt
2025.03.24-21:20:40.79 - <debug> Initializing vAccel
2025.03.24-21:20:40.79 - <info> vAccel 0.6.1-194-19056528
2025.03.24-21:20:40.79 - <debug> Config:
2025.03.24-21:20:40.80 - <debug>   plugins = libvaccel-torch.so
2025.03.24-21:20:40.80 - <debug>   log_level = debug
2025.03.24-21:20:40.80 - <debug>   log_file = (null)
2025.03.24-21:20:40.80 - <debug>   profiling_enabled = false
2025.03.24-21:20:40.80 - <debug>   version_ignore = false
2025.03.24-21:20:40.80 - <debug> Created top-level rundir: /run/user/1002/vaccel/7pAihg
2025.03.24-21:20:41.40 - <info> Registered plugin torch 0.1.0-22-7cf3d0e4
2025.03.24-21:20:41.40 - <debug> Registered op torch_jitload_forward from plugin torch
2025.03.24-21:20:41.40 - <debug> Registered op torch_sgemm from plugin torch
2025.03.24-21:20:41.40 - <debug> Registered op image_classify from plugin torch
2025.03.24-21:20:41.40 - <debug> Loaded plugin torch from libvaccel-torch.so
2025.03.24-21:20:41.40 - <debug> Initialized resource 1
Initialized model resource 1
2025.03.24-21:20:41.40 - <debug> New rundir for session 1: /run/user/1002/vaccel/7pAihg/session.1
2025.03.24-21:20:41.40 - <debug> Initialized session 1
Initialized vAccel session 1
2025.03.24-21:20:41.40 - <debug> New rundir for resource 1: /run/user/1002/vaccel/7pAihg/resource.1
2025.03.24-21:20:41.40 - <debug> Downloading https://s3.nbfc.io/torch/mobilenet.pt
2025.03.24-21:20:46.41 - <debug> Downloaded: 4.1 KB of 13.7 MB (30.1%) | Speed: 847.20 KB/sec
2025.03.24-21:20:50.48 - <debug> Downloaded: 13.7 MB of 13.7 MB (100.0%) | Speed: 1.51 MB/sec
2025.03.24-21:20:50.48 - <debug> Download completed successfully
2025.03.24-21:20:50.48 - <debug> session:1 Registered resource 1
2025.03.24-21:20:50.52 - <debug> session:1 Looking for plugin implementing torch_jitload_forward operation
2025.03.24-21:20:50.52 - <debug> Returning func from hint plugin torch
2025.03.24-21:20:50.52 - <debug> Found implementation in torch plugin
2025.03.24-21:20:50.52 - <debug> [torch] session:1 Jitload & Forward Process
2025.03.24-21:20:50.52 - <debug> [torch] Model: /run/user/1002/vaccel/7pAihg/resource.1/mobilenet.pt
2025.03.24-21:20:50.52 - <debug> [torch] CUDA not available, running in CPU mode
Success!
Result Tensor :
Output tensor => type:7 nr_dims:2
size: 4000 B
Prediction: banana
2025.03.24-21:20:50.98 - <debug> session:1 Unregistered resource 1
2025.03.24-21:20:50.98 - <debug> Released session 1
2025.03.24-21:20:50.98 - <debug> Removing file /run/user/1002/vaccel/7pAihg/resource.1/mobilenet.pt
2025.03.24-21:20:50.99 - <debug> Released resource 1
2025.03.24-21:20:51.12 - <debug> Cleaning up vAccel
2025.03.24-21:20:51.12 - <debug> Cleaning up sessions
2025.03.24-21:20:51.12 - <debug> Cleaning up resources
2025.03.24-21:20:51.12 - <debug> Cleaning up plugins
2025.03.24-21:20:51.12 - <debug> Unregistered plugin torch
```
