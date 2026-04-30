# TVM Plugin

The TVM plugin for vAccel implements image inference vAccel operations with
[TVM](https://tvm.apache.org).

## Supported operations

- [Image classification](../../../api/api-reference/operations.md#image-classification)

## Installing TVM C/C++ API files

You can find instructions on how to install the required files on the [Build and
Install TVM] page. The rest of this guide assumes TVM is installed at `/opt/tvm`
and its' libraries are at `/opt/tvm/build`.

[Build and Install TVM]: ../../../useful-docs/build-and-install-tvm.md

## Installing the plugin

You can get the latest TVM plugin binary release from the
[Releases](https://github.com/nubificus/vaccel/releases) page of the vAccel
repository. Releases include binaries for x86_64/aarch64 Ubuntu-based systems.

### TAR

To install the TAR binary package of the latest TVM plugin release:

/// tab | x86

```sh
wget https://github.com/nubificus/vaccel/releases/download/v[[ versions.vaccel ]]/vaccel-tvm_[[ versions.plugins.tvm ]]_x86_64.tar.gz
# Replace '/usr/local' below with the desired installation prefix
tar xfv vaccel-tvm_[[ versions.plugins.tvm ]]_x86_64.tar.gz --strip-components=2 -C /usr/local
# Update pkg-config files with the correct prefix
find /usr/local -name "vaccel-tvm.pc" -exec sed -i 's:^\(prefix=\).*:\1/usr/local:g' {} \;
```

///

/// tab | ARM (64-bit)

```sh
wget https://github.com/nubificus/vaccel/releases/download/v[[ versions.vaccel ]]/vaccel-tvm_[[ versions.plugins.tvm ]]_aarch64.tar.gz
# Replace '/usr/local' below with the desired installation prefix
tar xfv vaccel-tvm_[[ versions.plugins.tvm ]]_aarch64.tar.gz --strip-components=2 -C /usr/local
# Update pkg-config files with the correct prefix
find /usr/local -name "vaccel-tvm.pc" -exec sed -i 's:^\(prefix=\).*:\1/usr/local:g' {} \;
```

///

### Latest artifacts

You can also find prebuilt artifacts of the latest TVM plugin revision at:

/// tab | x86

```sh
# TAR
https://s3.nbfc.io/nbfc-assets/github/vaccel/plugins/tvm/rev/main/x86_64/release/vaccel-tvm_latest_x86_64.tar.gz
```

///

/// tab | ARM (64-bit)

```sh
# TAR
https://s3.nbfc.io/nbfc-assets/github/vaccel/plugins/tvm/rev/main/aarch64/release/vaccel-tvm_latest_aarch64.tar.gz
```

///

## Usage

To specify TVM plugin as the selected plugin for vAccel execution:

```sh
export VACCEL_PLUGINS=libvaccel-tvm.so
```

Ensure TVM, vAccel and the TVM plugin libraries are in the library search paths
before trying to use the plugin.

## Running an example

Export the necessary variables:

```sh
export LD_LIBRARY_PATH=/opt/tvm/build
export VACCEL_PLUGINS=libvaccel-tvm.so
# Optionally, for verbose output
export VACCEL_LOG_LEVEL=4
```

Assuming vAccel is installed at `/usr/local`, you can run an image
classification with a ResNet model from
`https://s3.nbfc.io/models/tvm/x86_64/resnet18-v2-7.so` with:

/// tab | x86

```console
$ classify /usr/local/share/vaccel/images/example.jpg 1 \
      https://s3.nbfc.io/models/tvm/x86_64/resnet18-v2-7.so
2026.04.29-15:22:46.01 - <debug> Initializing vAccel
2026.04.29-15:22:46.01 - <info> vAccel 0.7.1-93-ebc23b1f
2026.04.29-15:22:46.01 - <debug> Config:
2026.04.29-15:22:46.01 - <debug>   plugins = libvaccel-tvm.so
2026.04.29-15:22:46.01 - <debug>   log_level = debug
2026.04.29-15:22:46.01 - <debug>   log_file = (null)
2026.04.29-15:22:46.01 - <debug>   profiling_enabled = false
2026.04.29-15:22:46.01 - <debug>   version_ignore = false
2026.04.29-15:22:46.01 - <debug> Created top-level rundir: /run/user/0/vaccel/sCOIDY
2026.04.29-15:22:46.01 - <info> Registered plugin tvm 0.1.0-11-6da3ba19
2026.04.29-15:22:46.01 - <debug> Registered op image_classify from plugin tvm
2026.04.29-15:22:46.01 - <debug> Loaded plugin tvm from libvaccel-tvm.so
2026.04.29-15:22:46.01 - <debug> New rundir for session 1: /run/user/0/vaccel/sCOIDY/session.1
2026.04.29-15:22:46.01 - <debug> Initialized session 1 with plugin tvm
Initialized session with id: 1
2026.04.29-15:22:46.01 - <debug> Initialized resource 1
2026.04.29-15:22:46.01 - <debug> New rundir for resource 1: /run/user/0/vaccel/sCOIDY/resource.1
2026.04.29-15:22:46.01 - <debug> Downloading https://s3.nbfc.io/models/tvm/x86_64/resnet18-v2-7.so
2026.04.29-15:22:47.36 - <debug> Downloaded: 45.8 MB of 45.8 MB (100.0%) | Speed: 34.00 MB/sec
2026.04.29-15:22:47.36 - <debug> Download completed successfully
2026.04.29-15:22:47.36 - <debug> session:1 Registered resource 1
2026.04.29-15:22:47.36 - <debug> session:1 Looking for func implementing op image_classify
2026.04.29-15:22:47.36 - <debug> Returning func for op image_classify from plugin tvm
2026.04.29-15:22:47.36 - <debug> [tvm] Resource path: /run/user/0/vaccel/sCOIDY/resource.1/resnet18-v2-7.so
loading file: /run/user/0/vaccel/sCOIDY/resource.1/resnet18-v2-7.so
2026.04.29-15:22:47.47 - <debug> [tvm] Prediction: banana
classification tags: banana
classification imagename: PLACEHOLDER
2026.04.29-15:22:47.47 - <debug> session:1 Unregistered resource 1
2026.04.29-15:22:47.47 - <debug> Removing file /run/user/0/vaccel/sCOIDY/resource.1/resnet18-v2-7.so
2026.04.29-15:22:47.47 - <debug> Released resource 1
2026.04.29-15:22:47.47 - <debug> Released session 1
2026.04.29-15:22:47.54 - <debug> Cleaning up vAccel
2026.04.29-15:22:47.54 - <debug> Cleaning up sessions
2026.04.29-15:22:47.54 - <debug> Cleaning up resources
2026.04.29-15:22:47.54 - <debug> Cleaning up plugins
2026.04.29-15:22:47.54 - <debug> Unregistered plugin tvm
```

///

/// tab | ARM (64-bit)

```console
$ classify /usr/local/share/vaccel/images/example.jpg 1 \
      https://s3.nbfc.io/models/tvm/aarch64/resnet18-v2-7.so
2026.04.29-15:22:46.01 - <debug> Initializing vAccel
2026.04.29-15:22:46.01 - <info> vAccel 0.7.1-93-ebc23b1f
2026.04.29-15:22:46.01 - <debug> Config:
2026.04.29-15:22:46.01 - <debug>   plugins = libvaccel-tvm.so
2026.04.29-15:22:46.01 - <debug>   log_level = debug
2026.04.29-15:22:46.01 - <debug>   log_file = (null)
2026.04.29-15:22:46.01 - <debug>   profiling_enabled = false
2026.04.29-15:22:46.01 - <debug>   version_ignore = false
2026.04.29-15:22:46.01 - <debug> Created top-level rundir: /run/user/0/vaccel/sCOIDY
2026.04.29-15:22:46.01 - <info> Registered plugin tvm 0.1.0-11-6da3ba19
2026.04.29-15:22:46.01 - <debug> Registered op image_classify from plugin tvm
2026.04.29-15:22:46.01 - <debug> Loaded plugin tvm from libvaccel-tvm.so
2026.04.29-15:22:46.01 - <debug> New rundir for session 1: /run/user/0/vaccel/sCOIDY/session.1
2026.04.29-15:22:46.01 - <debug> Initialized session 1 with plugin tvm
Initialized session with id: 1
2026.04.29-15:22:46.01 - <debug> Initialized resource 1
2026.04.29-15:22:46.01 - <debug> New rundir for resource 1: /run/user/0/vaccel/sCOIDY/resource.1
2026.04.29-15:22:46.01 - <debug> Downloading https://s3.nbfc.io/models/tvm/aarch64/resnet18-v2-7.so
2026.04.29-15:22:47.36 - <debug> Downloaded: 45.8 MB of 45.8 MB (100.0%) | Speed: 34.00 MB/sec
2026.04.29-15:22:47.36 - <debug> Download completed successfully
2026.04.29-15:22:47.36 - <debug> session:1 Registered resource 1
2026.04.29-15:22:47.36 - <debug> session:1 Looking for func implementing op image_classify
2026.04.29-15:22:47.36 - <debug> Returning func for op image_classify from plugin tvm
2026.04.29-15:22:47.36 - <debug> [tvm] Resource path: /run/user/0/vaccel/sCOIDY/resource.1/resnet18-v2-7.so
loading file: /run/user/0/vaccel/sCOIDY/resource.1/resnet18-v2-7.so
2026.04.29-15:22:47.47 - <debug> [tvm] Prediction: banana
classification tags: banana
classification imagename: PLACEHOLDER
2026.04.29-15:22:47.47 - <debug> session:1 Unregistered resource 1
2026.04.29-15:22:47.47 - <debug> Removing file /run/user/0/vaccel/sCOIDY/resource.1/resnet18-v2-7.so
2026.04.29-15:22:47.47 - <debug> Released resource 1
2026.04.29-15:22:47.47 - <debug> Released session 1
2026.04.29-15:22:47.54 - <debug> Cleaning up vAccel
2026.04.29-15:22:47.54 - <debug> Cleaning up sessions
2026.04.29-15:22:47.54 - <debug> Cleaning up resources
2026.04.29-15:22:47.54 - <debug> Cleaning up plugins
2026.04.29-15:22:47.54 - <debug> Unregistered plugin tvm
```

///
