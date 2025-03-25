# TVM Plugin

The TVM plugin for vAccel implements image inference vAccel operations with
[TVM](https://tvm.apache.org).

## Supported operations

- [Image classification](../../api.md#image-classification)

## Install TVM C/C++ API files

You can find instructions on how to install the required files
[here](../../useful-docs/tvm.md). The rest of this guide assumes TVM is
installed at `/opt/tvm` and its' libraries are at `/opt/tvm/build`.

## Install vAccel

Information about vAccel installation can be found [here](../../quickstart.md).
The rest of this guide assumes vAccel is installed at `/usr/local`.

## Install the plugin

Download the plugin for `x86_64`:

```sh
https://s3.nbfc.io/nbfc-assets/github/vaccel/plugins/tvm/rev/main/x86_64/release/vaccel-tvm-latest-bin.tar.gz
```

or `aarch64`:

```sh
https://s3.nbfc.io/nbfc-assets/github/vaccel/plugins/tvm/rev/main/aarch64/release/vaccel-tvm-latest-bin.tar.gz
```

and extract to the desired installation directory, ie. to install in
`/usr/local`:

```sh
sudo tar xfv vaccel-tvm-latest-bin.tar.gz --strip-components=2 -C /usr/local
```

## Run an example

After having installed TVM, vAccel and the TVM plugin you are ready to run an
image classification example.

Ensure TVM libraries are in the library search path:

```sh
export LD_LIBRARY_PATH=/opt/tvm/build
```

If vAccel and/or the TVM plugin are installed in a non-standard library path you
will also need to include them in the `LD_LIBRARY_PATH`.

Define the TVM plugin as the selected plugin for vAccel execution:

```sh
export VACCEL_PLUGINS=libvaccel-tvm.so
```

Alternatively, you can provide the full path to the plugin library, without
needing to have the plugin in your library search path:

```sh
export VACCEL_PLUGINS=/usr/local/lib/x86_64-linux-gnu/libvaccel-tvm.so
```

Configure the vaccel log level for more verbose output:

```sh
export VACCEL_LOG_LEVEL=4
```

And finally run an image classification with a ResNet model from
`https://s3.nbfc.io/models/tvm/x86_64/resnet18-v2-7.so`:

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

You can find the same ResNet model built for `aarch64` by changing the
architecture of the previous link, at
`https://s3.nbfc.io/models/tvm/aarch64/resnet18-v2-7.so`
