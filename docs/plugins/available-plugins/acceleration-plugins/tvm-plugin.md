# TVM Plugin

The TVM plugin for vAccel implements image inference vAccel operations with
[TVM](https://tvm.apache.org).

## Supported operations

- [Image classification](../../../api/api-reference/operations.md#image-classification)

## Installing TVM C/C++ API files

You can find instructions on how to install the required files
[here](../../../useful-docs/tvm.md). The rest of this guide assumes TVM is
installed at `/opt/tvm` and its' libraries are at `/opt/tvm/build`.

## Installing the plugin

You can get the latest TVM plugin binary release from the
[Releases](https://github.com/nubificus/vaccel/releases) page of the vAccel
repository. Releases include binaries for x86_64/aarch64 Ubuntu-based systems.

### TAR

To install the TAR binary package of the latest TVM plugin release:

/// tab | x86

```sh
wget https://github.com/nubificus/vaccel/releases/download/v[[ versions.vaccel ]]/vaccel-tvm_[[ versions.plugins.tvm ]]_amd64.tar.gz
# Replace '/usr/local' below with the desired installation prefix
tar xfv vaccel-tvm_[[ versions.plugins.tvm ]]_amd64.tar.gz --strip-components=2 -C /usr/local
# Update pkg-config files with the correct prefix
find /usr/local -name "vaccel-tvm.pc" -exec sed -i 's:^\(prefix=\).*:\1/usr/local:g' {} \;
```

///

/// tab | ARM (64-bit)

```sh
wget https://github.com/nubificus/vaccel/releases/download/v[[ versions.vaccel ]]/vaccel-tvm_[[ versions.plugins.tvm ]]_arm64.tar.gz
# Replace '/usr/local' below with the desired installation prefix
tar xfv vaccel-tvm_[[ versions.plugins.tvm ]]_arm64.tar.gz --strip-components=2 -C /usr/local
# Update pkg-config files with the correct prefix
find /usr/local -name "vaccel-tvm.pc" -exec sed -i 's:^\(prefix=\).*:\1/usr/local:g' {} \;
```

///

### Latest artifacts

You can also find prebuilt artifacts of the latest TVM plugin revision at:

/// tab | x86

```sh
# TAR
https://s3.nbfc.io/nbfc-assets/github/vaccel/plugins/tvm/rev/main/x86_64/release/vaccel-tvm-latest-bin.tar.gz
```

///

/// tab | ARM (64-bit)

```sh
# TAR
https://s3.nbfc.io/nbfc-assets/github/vaccel/plugins/tvm/rev/main/aarch64/release/vaccel-tvm-latest-bin.tar.gz
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
2025.03.25-19:37:03.39 - <debug> Initializing vAccel
2025.03.25-19:37:03.39 - <info> vAccel 0.6.1-194-19056528
2025.03.25-19:37:03.39 - <debug> Config:
2025.03.25-19:37:03.39 - <debug>   plugins = libvaccel-tvm.so
2025.03.25-19:37:03.39 - <debug>   log_level = debug
2025.03.25-19:37:03.39 - <debug>   log_file = (null)
2025.03.25-19:37:03.39 - <debug>   profiling_enabled = false
2025.03.25-19:37:03.39 - <debug>   version_ignore = false
2025.03.25-19:37:03.39 - <debug> Created top-level rundir: /run/user/1002/vaccel/7CYHmR
2025.03.25-19:37:03.40 - <info> Registered plugin tvm 0.0.0-19-d720e616
2025.03.25-19:37:03.40 - <debug> Registered op image_classify from plugin tvm
2025.03.25-19:37:03.40 - <debug> Loaded plugin tvm from libvaccel-tvm.so
2025.03.25-19:37:03.40 - <debug> New rundir for session 1: /run/user/1002/vaccel/7CYHmR/session.1
2025.03.25-19:37:03.40 - <debug> Initialized session 1
Initialized session with id: 1
2025.03.25-19:37:03.40 - <debug> Initialized resource 1
2025.03.25-19:37:03.40 - <debug> New rundir for resource 1: /run/user/1002/vaccel/7CYHmR/resource.1
2025.03.25-19:37:03.40 - <debug> Downloading https://s3.nbfc.io/models/tvm/x86_64/resnet18-v2-7.so
2025.03.25-19:37:08.40 - <debug> Downloaded: 9.0 MB of 45.8 MB (19.7%) | Speed: 1.80 MB/sec
2025.03.25-19:37:13.40 - <debug> Downloaded: 20.2 MB of 45.8 MB (44.1%) | Speed: 2.02 MB/sec
2025.03.25-19:37:18.40 - <debug> Downloaded: 31.1 MB of 45.8 MB (67.9%) | Speed: 2.07 MB/sec
2025.03.25-19:37:23.40 - <debug> Downloaded: 40.2 MB of 45.8 MB (87.8%) | Speed: 2.01 MB/sec
2025.03.25-19:37:26.28 - <debug> Downloaded: 45.8 MB of 45.8 MB (100.0%) | Speed: 2.00 MB/sec
2025.03.25-19:37:26.28 - <debug> Download completed successfully
2025.03.25-19:37:26.28 - <debug> session:1 Registered resource 1
2025.03.25-19:37:26.28 - <debug> session:1 Looking for plugin implementing VACCEL_OP_IMAGE_CLASSIFY
2025.03.25-19:37:26.28 - <debug> Returning func from hint plugin tvm
2025.03.25-19:37:26.28 - <debug> Found implementation in tvm plugin
2025.03.25-19:37:26.28 - <debug> [tvm] Resource path: /run/user/1002/vaccel/7CYHmR/resource.1/resnet18-v2-7.so
loading file: /run/user/1002/vaccel/7CYHmR/resource.1/resnet18-v2-7.so
2025.03.25-19:37:26.43 - <debug> [tvm] Prediction: banana
classification tags: banana
classification imagename: PLACEHOLDER
2025.03.25-19:37:26.43 - <debug> session:1 Unregistered resource 1
2025.03.25-19:37:26.43 - <debug> Removing file /run/user/1002/vaccel/7CYHmR/resource.1/resnet18-v2-7.so
2025.03.25-19:37:26.44 - <debug> Released resource 1
2025.03.25-19:37:26.44 - <debug> Released session 1
2025.03.25-19:37:26.65 - <debug> Cleaning up vAccel
2025.03.25-19:37:26.65 - <debug> Cleaning up sessions
2025.03.25-19:37:26.65 - <debug> Cleaning up resources
2025.03.25-19:37:26.65 - <debug> Cleaning up plugins
2025.03.25-19:37:26.65 - <debug> Unregistered plugin tvm
```

///

/// tab | ARM (64-bit)

```console
$ classify /usr/local/share/vaccel/images/example.jpg 1 \
      https://s3.nbfc.io/models/tvm/aarch64/resnet18-v2-7.so
2025.03.25-19:37:03.39 - <debug> Initializing vAccel
2025.03.25-19:37:03.39 - <info> vAccel 0.6.1-194-19056528
2025.03.25-19:37:03.39 - <debug> Config:
2025.03.25-19:37:03.39 - <debug>   plugins = libvaccel-tvm.so
2025.03.25-19:37:03.39 - <debug>   log_level = debug
2025.03.25-19:37:03.39 - <debug>   log_file = (null)
2025.03.25-19:37:03.39 - <debug>   profiling_enabled = false
2025.03.25-19:37:03.39 - <debug>   version_ignore = false
2025.03.25-19:37:03.39 - <debug> Created top-level rundir: /run/user/1002/vaccel/7CYHmR
2025.03.25-19:37:03.40 - <info> Registered plugin tvm 0.0.0-19-d720e616
2025.03.25-19:37:03.40 - <debug> Registered op image_classify from plugin tvm
2025.03.25-19:37:03.40 - <debug> Loaded plugin tvm from libvaccel-tvm.so
2025.03.25-19:37:03.40 - <debug> New rundir for session 1: /run/user/1002/vaccel/7CYHmR/session.1
2025.03.25-19:37:03.40 - <debug> Initialized session 1
Initialized session with id: 1
2025.03.25-19:37:03.40 - <debug> Initialized resource 1
2025.03.25-19:37:03.40 - <debug> New rundir for resource 1: /run/user/1002/vaccel/7CYHmR/resource.1
2025.03.25-19:37:03.40 - <debug> Downloading https://s3.nbfc.io/models/tvm/x86_64/resnet18-v2-7.so
2025.03.25-19:37:08.40 - <debug> Downloaded: 9.0 MB of 45.8 MB (19.7%) | Speed: 1.80 MB/sec
2025.03.25-19:37:13.40 - <debug> Downloaded: 20.2 MB of 45.8 MB (44.1%) | Speed: 2.02 MB/sec
2025.03.25-19:37:18.40 - <debug> Downloaded: 31.1 MB of 45.8 MB (67.9%) | Speed: 2.07 MB/sec
2025.03.25-19:37:23.40 - <debug> Downloaded: 40.2 MB of 45.8 MB (87.8%) | Speed: 2.01 MB/sec
2025.03.25-19:37:26.28 - <debug> Downloaded: 45.8 MB of 45.8 MB (100.0%) | Speed: 2.00 MB/sec
2025.03.25-19:37:26.28 - <debug> Download completed successfully
2025.03.25-19:37:26.28 - <debug> session:1 Registered resource 1
2025.03.25-19:37:26.28 - <debug> session:1 Looking for plugin implementing VACCEL_OP_IMAGE_CLASSIFY
2025.03.25-19:37:26.28 - <debug> Returning func from hint plugin tvm
2025.03.25-19:37:26.28 - <debug> Found implementation in tvm plugin
2025.03.25-19:37:26.28 - <debug> [tvm] Resource path: /run/user/1002/vaccel/7CYHmR/resource.1/resnet18-v2-7.so
loading file: /run/user/1002/vaccel/7CYHmR/resource.1/resnet18-v2-7.so
2025.03.25-19:37:26.43 - <debug> [tvm] Prediction: banana
classification tags: banana
classification imagename: PLACEHOLDER
2025.03.25-19:37:26.43 - <debug> session:1 Unregistered resource 1
2025.03.25-19:37:26.43 - <debug> Removing file /run/user/1002/vaccel/7CYHmR/resource.1/resnet18-v2-7.so
2025.03.25-19:37:26.44 - <debug> Released resource 1
2025.03.25-19:37:26.44 - <debug> Released session 1
2025.03.25-19:37:26.65 - <debug> Cleaning up vAccel
2025.03.25-19:37:26.65 - <debug> Cleaning up sessions
2025.03.25-19:37:26.65 - <debug> Cleaning up resources
2025.03.25-19:37:26.65 - <debug> Cleaning up plugins
2025.03.25-19:37:26.65 - <debug> Unregistered plugin tvm
```

///
