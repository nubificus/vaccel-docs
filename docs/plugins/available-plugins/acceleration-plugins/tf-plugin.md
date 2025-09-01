# Tensorflow Plugin

The Tensorflow plugin for vAccel implements basic
[Tensorflow](https://www.tensorflow.org/) and Tensorflow Lite support for vAccel
operations.

## Supported operations

- [TensorFlow model load](../../../api/api-reference/operations.md#tensorflow-model-load)
- [TensorFlow model unload](../../../api/api-reference/operations.md#tensorflow-model-unload)
- [TensorFlow model run](../../../api/api-reference/operations.md#tensorflow-model-run)
- [TensorFlow Lite model load](../../../api/api-reference/operations.md#tensorflow-lite-model-load)
- [TensorFlow Lite model unload](../../../api/api-reference/operations.md#tensorflow-lite-model-unload)
- [TensorFlow Lite model run](../../../api/api-reference/operations.md#tensorflow-lite-model-run)

## Installing Tensorflow and Tensorflow Lite C/C++ API files

You can find instructions on how to install the required files on the [Build and
Install Tensorflow] page. The rest of this guide assumes Tensorflow is installed
at `/usr/local` and its' libraries are at `/usr/local/lib`.

[Build and Install Tensorflow]:
    ../../../useful-docs/build-and-install-tensorflow.md

## Installing the plugin

You can get the latest Tensorflow plugin binary release from the
[Releases](https://github.com/nubificus/vaccel/releases) page of the vAccel
repository. Releases include binaries for x86_64/aarch64 Ubuntu-based systems.

### Requirements

The prebuilt TF plugin binaries depend on
[libarchive](https://www.libarchive.org/). You can install it with:

```sh
sudo apt install libarchive13
```

### TAR

To install the TAR binary package of the latest Tensorflow plugin release:

/// tab | x86

```sh
wget https://github.com/nubificus/vaccel/releases/download/v[[ versions.vaccel ]]/vaccel-tf_[[ versions.plugins.tf ]]_amd64.tar.gz
# Replace '/usr/local' below with the desired installation prefix
tar xfv vaccel-tf_[[ versions.plugins.tf ]]_amd64.tar.gz --strip-components=2 -C /usr/local
# Update pkg-config files with the correct prefix
find /usr/local -name "vaccel-tf.pc" -exec sed -i 's:^\(prefix=\).*:\1/usr/local:g' {} \;
```

///

/// tab | ARM (64-bit)

```sh
wget https://github.com/nubificus/vaccel/releases/download/v[[ versions.vaccel ]]/vaccel-tf_[[ versions.plugins.tf ]]_arm64.tar.gz
# Replace '/usr/local' below with the desired installation prefix
tar xfv vaccel-tf_[[ versions.plugins.tf ]]_arm64.tar.gz --strip-components=2 -C /usr/local
# Update pkg-config files with the correct prefix
find /usr/local -name "vaccel-tf.pc" -exec sed -i 's:^\(prefix=\).*:\1/usr/local:g' {} \;
```

///

### Latest artifacts

You can also find prebuilt artifacts of the latest Tensorflow plugin revision
at:

/// tab | x86

```sh
# TAR
https://s3.nbfc.io/nbfc-assets/github/vaccel/plugins/tf/rev/main/x86_64/release/vaccel-tf-latest-bin.tar.gz
```

///

/// tab | ARM (64-bit)

```sh
# TAR
https://s3.nbfc.io/nbfc-assets/github/vaccel/plugins/tf/rev/main/aarch64/release/vaccel-tf-latest-bin.tar.gz
```

///

## Usage

To specify Tensorflow plugin as the selected plugin for vAccel execution:

```sh
export VACCEL_PLUGINS=libvaccel-tf.so
```

Ensure Tensorflow, vAccel and the Tensorflow plugin libraries are in the library
search paths before trying to use the plugin.

## Running an example

Export the necessary variables:

```sh
export VACCEL_PLUGINS=libvaccel-tf.so
# Optionally, for verbose output
export VACCEL_LOG_LEVEL=4
```

Assuming vAccel is installed at `/usr/local`, you can run an image
classification with a ResNet model from
`https://s3.nbfc.io/models/tf/resnet18-v2-7_saved_model.tar.xz` with:

```console
$ tf_inference \
      /usr/local/share/vaccel/images/example.jpg \
      https://s3.nbfc.io/models/tf/resnet18-v2-7_saved_model.tar.xz \
      /usr/local/share/vaccel/labels/imagenet.txt
2025.07.19-20:55:09.21 - <debug> Initializing vAccel
2025.07.19-20:55:09.21 - <info> vAccel 0.7.1-22-edced930
2025.07.19-20:55:09.21 - <debug> Config:
2025.07.19-20:55:09.21 - <debug>   plugins = libvaccel-tf.so
2025.07.19-20:55:09.21 - <debug>   log_level = debug
2025.07.19-20:55:09.21 - <debug>   log_file = (null)
2025.07.19-20:55:09.21 - <debug>   profiling_enabled = false
2025.07.19-20:55:09.21 - <debug>   version_ignore = false
2025.07.19-20:55:09.21 - <debug> Created top-level rundir: /run/user/0/vaccel/sZDGgp
2025-07-19 20:55:09.252594: I tensorflow/core/util/port.cc:153] oneDNN custom operations are on. You may see slightly different numerical results due to floating-point round-off errors from different computation orders. To turn them off, set the environment variable `TF_ENABLE_ONEDNN_OPTS=0`.
2025-07-19 20:55:09.274317: I tensorflow/core/util/port.cc:153] oneDNN custom operations are on. You may see slightly different numerical results due to floating-point round-off errors from different computation orders. To turn them off, set the environment variable `TF_ENABLE_ONEDNN_OPTS=0`.
2025.07.19-20:55:09.27 - <info> Registered plugin tf 0.2.0-4-4c18a4c1
2025.07.19-20:55:09.27 - <debug> Registered op tf_model_load from plugin tf
2025.07.19-20:55:09.27 - <debug> Registered op tf_model_unload from plugin tf
2025.07.19-20:55:09.27 - <debug> Registered op tf_model_run from plugin tf
2025.07.19-20:55:09.27 - <debug> Registered op tflite_model_load from plugin tf
2025.07.19-20:55:09.27 - <debug> Registered op tflite_model_unload from plugin tf
2025.07.19-20:55:09.27 - <debug> Registered op tflite_model_run from plugin tf
2025.07.19-20:55:09.27 - <debug> Loaded plugin tf from libvaccel-tf.so
2025.07.19-20:55:09.27 - <debug> Initialized resource 1
Initialized model resource 1
2025.07.19-20:55:09.27 - <debug> New rundir for session 1: /run/user/0/vaccel/sZDGgp/session.1
2025.07.19-20:55:09.27 - <debug> Initialized session 1
Initialized vAccel session 1
2025.07.19-20:55:09.27 - <debug> New rundir for resource 1: /run/user/0/vaccel/sZDGgp/resource.1
2025.07.19-20:55:09.27 - <debug> Downloading https://s3.nbfc.io/models/tf/resnet18-v2-7_saved_model.tar.xz
2025.07.19-20:55:10.56 - <debug> Downloaded: 41.0 MB of 41.0 MB (100.0%) | Speed: 31.91 MB/sec
2025.07.19-20:55:10.56 - <debug> Download completed successfully
2025.07.19-20:55:10.56 - <debug> session:1 Registered resource 1
2025.07.19-20:55:10.56 - <debug> session:1 Looking for plugin implementing op tf_model_load
2025.07.19-20:55:10.56 - <debug> Returning func from hint plugin tf
2025.07.19-20:55:10.56 - <debug> Found implementation in tf plugin
2025.07.19-20:55:10.56 - <debug> [tf] Loading session from SavedModel
2025.07.19-20:55:10.57 - <debug> [tf][archive] Extracting: /run/user/0/vaccel/sZDGgp/resource.1/resnet18-v2-7_saved_model/
2025.07.19-20:55:10.57 - <debug> [tf][archive] Extracting: /run/user/0/vaccel/sZDGgp/resource.1/resnet18-v2-7_saved_model/assets/
2025.07.19-20:55:10.57 - <debug> [tf][archive] Extracting: /run/user/0/vaccel/sZDGgp/resource.1/resnet18-v2-7_saved_model/fingerprint.pb
2025.07.19-20:55:10.57 - <debug> [tf][archive] Extracting: /run/user/0/vaccel/sZDGgp/resource.1/resnet18-v2-7_saved_model/saved_model.pb
2025.07.19-20:55:12.64 - <debug> [tf][archive] Extracting: /run/user/0/vaccel/sZDGgp/resource.1/resnet18-v2-7_saved_model/variables/
2025.07.19-20:55:12.64 - <debug> [tf][archive] Extracting: /run/user/0/vaccel/sZDGgp/resource.1/resnet18-v2-7_saved_model/variables/variables.data-00000-of-00001
2025.07.19-20:55:12.64 - <debug> [tf][archive] Extracting: /run/user/0/vaccel/sZDGgp/resource.1/resnet18-v2-7_saved_model/variables/variables.index
2025-07-19 20:55:12.648567: I tensorflow/cc/saved_model/reader.cc:83] Reading SavedModel from: /run/user/0/vaccel/sZDGgp/resource.1/resnet18-v2-7_saved_model
2025-07-19 20:55:12.668441: I tensorflow/cc/saved_model/reader.cc:52] Reading meta graph with tags { serve }
2025-07-19 20:55:12.668473: I tensorflow/cc/saved_model/reader.cc:147] Reading SavedModel debug info (if present) from: /run/user/0/vaccel/sZDGgp/resource.1/resnet18-v2-7_saved_model
2025-07-19 20:55:12.668536: I tensorflow/core/platform/cpu_feature_guard.cc:210] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.
To enable the following instructions: SSE3 SSE4.1 SSE4.2 AVX AVX2 AVX_VNNI FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.
2025-07-19 20:55:12.742341: I tensorflow/compiler/mlir/mlir_graph_optimization_pass.cc:388] MLIR V1 optimization pass is not enabled
2025-07-19 20:55:12.743065: I tensorflow/cc/saved_model/loader.cc:236] Restoring SavedModel bundle.
2025-07-19 20:55:12.776518: I tensorflow/cc/saved_model/loader.cc:220] Running initialization op on SavedModel bundle at path: /run/user/0/vaccel/sZDGgp/resource.1/resnet18-v2-7_saved_model
2025-07-19 20:55:12.806477: I tensorflow/cc/saved_model/loader.cc:462] SavedModel load for tags { serve }; Status: success: OK. Took 157910 microseconds.
2025.07.19-20:55:12.82 - <debug> [tf] Model loaded correctly
Session load status => code:0 message:
2025.07.19-20:55:12.86 - <debug> session:1 Looking for plugin implementing op tf_model_run
2025.07.19-20:55:12.86 - <debug> Returning func from hint plugin tf
2025.07.19-20:55:12.86 - <debug> Found implementation in tf plugin
2025.07.19-20:55:12.86 - <debug> [tf] Running session
2025.07.19-20:55:13.50 - <debug> [tf] Success
Session run status => code:0 message:
Success!
Output tensor => type:1 nr_dims:2 size:4000B
Prediction: banana
2025.07.19-20:55:13.50 - <debug> session:1 Looking for plugin implementing op tf_model_unload
2025.07.19-20:55:13.50 - <debug> Returning func from hint plugin tf
2025.07.19-20:55:13.50 - <debug> Found implementation in tf plugin
2025.07.19-20:55:13.50 - <debug> [tf] Deleting session
2025.07.19-20:55:13.50 - <debug> [tf][archive] Removed file: /run/user/0/vaccel/sZDGgp/resource.1/resnet18-v2-7_saved_model/fingerprint.pb
2025.07.19-20:55:13.50 - <debug> [tf][archive] Removed file: /run/user/0/vaccel/sZDGgp/resource.1/resnet18-v2-7_saved_model/variables/variables.index
2025.07.19-20:55:13.50 - <debug> [tf][archive] Removed file: /run/user/0/vaccel/sZDGgp/resource.1/resnet18-v2-7_saved_model/variables/variables.data-00000-of-00001
2025.07.19-20:55:13.50 - <debug> [tf][archive] Removed directory: /run/user/0/vaccel/sZDGgp/resource.1/resnet18-v2-7_saved_model/variables
2025.07.19-20:55:13.51 - <debug> [tf][archive] Removed file: /run/user/0/vaccel/sZDGgp/resource.1/resnet18-v2-7_saved_model/saved_model.pb
2025.07.19-20:55:13.51 - <debug> [tf][archive] Removed directory: /run/user/0/vaccel/sZDGgp/resource.1/resnet18-v2-7_saved_model/assets
2025.07.19-20:55:13.51 - <debug> [tf][archive] Removed directory: /run/user/0/vaccel/sZDGgp/resource.1/resnet18-v2-7_saved_model
Session delete status => code:0 message:
2025.07.19-20:55:13.51 - <debug> session:1 Unregistered resource 1
2025.07.19-20:55:13.51 - <debug> Released session 1
2025.07.19-20:55:13.51 - <debug> Removing file /run/user/0/vaccel/sZDGgp/resource.1/resnet18-v2-7_saved_model.tar.xz
2025.07.19-20:55:13.51 - <debug> Released resource 1
2025.07.19-20:55:13.51 - <debug> Cleaning up vAccel
2025.07.19-20:55:13.51 - <debug> Cleaning up sessions
2025.07.19-20:55:13.51 - <debug> Cleaning up resources
2025.07.19-20:55:13.51 - <debug> Cleaning up plugins
2025.07.19-20:55:13.51 - <debug> Unregistered plugin tf
```

You can also run a similar inference example using Tensorflow Lite with:

```console
$ tflite_inference \
      /usr/local/share/vaccel/images/example.jpg \
      https://s3.nbfc.io/models/tf/resnet18-v2-7_float32.tflite \
      /usr/local/share/vaccel/labels/imagenet.txt
2025.07.19-20:55:13.54 - <debug> Initializing vAccel
2025.07.19-20:55:13.54 - <info> vAccel 0.7.1-22-edced930
2025.07.19-20:55:13.54 - <debug> Config:
2025.07.19-20:55:13.54 - <debug>   plugins = libvaccel-tf.so
2025.07.19-20:55:13.54 - <debug>   log_level = debug
2025.07.19-20:55:13.54 - <debug>   log_file = (null)
2025.07.19-20:55:13.54 - <debug>   profiling_enabled = false
2025.07.19-20:55:13.54 - <debug>   version_ignore = false
2025.07.19-20:55:13.54 - <debug> Created top-level rundir: /run/user/0/vaccel/hsuZdP
2025-07-19 20:55:13.568854: I tensorflow/core/util/port.cc:153] oneDNN custom operations are on. You may see slightly different numerical results due to floating-point round-off errors from different computation orders. To turn them off, set the environment variable `TF_ENABLE_ONEDNN_OPTS=0`.
2025-07-19 20:55:13.595803: I tensorflow/core/util/port.cc:153] oneDNN custom operations are on. You may see slightly different numerical results due to floating-point round-off errors from different computation orders. To turn them off, set the environment variable `TF_ENABLE_ONEDNN_OPTS=0`.
2025.07.19-20:55:13.59 - <info> Registered plugin tf 0.2.0-4-4c18a4c1
2025.07.19-20:55:13.59 - <debug> Registered op tf_model_load from plugin tf
2025.07.19-20:55:13.59 - <debug> Registered op tf_model_unload from plugin tf
2025.07.19-20:55:13.59 - <debug> Registered op tf_model_run from plugin tf
2025.07.19-20:55:13.59 - <debug> Registered op tflite_model_load from plugin tf
2025.07.19-20:55:13.59 - <debug> Registered op tflite_model_unload from plugin tf
2025.07.19-20:55:13.59 - <debug> Registered op tflite_model_run from plugin tf
2025.07.19-20:55:13.59 - <debug> Loaded plugin tf from libvaccel-tf.so
2025.07.19-20:55:13.59 - <debug> Initialized resource 1
Initialized model resource 1
2025.07.19-20:55:13.59 - <debug> New rundir for session 1: /run/user/0/vaccel/hsuZdP/session.1
2025.07.19-20:55:13.59 - <debug> Initialized session 1
Initialized vAccel session 1
2025.07.19-20:55:13.59 - <debug> New rundir for resource 1: /run/user/0/vaccel/hsuZdP/resource.1
2025.07.19-20:55:13.59 - <debug> Downloading https://s3.nbfc.io/models/tf/resnet18-v2-7_float32.tflite
2025.07.19-20:55:14.72 - <debug> Downloaded: 44.6 MB of 44.6 MB (100.0%) | Speed: 39.69 MB/sec
2025.07.19-20:55:14.72 - <debug> Download completed successfully
2025.07.19-20:55:14.72 - <debug> session:1 Registered resource 1
2025.07.19-20:55:14.72 - <debug> session:1 Looking for plugin implementing op tflite_model_load
2025.07.19-20:55:14.72 - <debug> Returning func from hint plugin tf
2025.07.19-20:55:14.72 - <debug> Found implementation in tf plugin
2025.07.19-20:55:14.72 - <debug> [tf][tflite] Loading session from model
2025.07.19-20:55:14.72 - <debug> [tf][tflite] Model loaded correctly
2025.07.19-20:55:14.73 - <debug> session:1 Looking for plugin implementing op tflite_model_run
2025.07.19-20:55:14.73 - <debug> Returning func from hint plugin tf
2025.07.19-20:55:14.73 - <debug> Found implementation in tf plugin
2025.07.19-20:55:14.73 - <debug> [tf][tflite] Running session
2025.07.19-20:55:14.83 - <debug> [tf][tflite] Success
Session run status: 0
Success!
Output tensor => type:1 nr_dims:2 size:4000B
Prediction: banana
2025.07.19-20:55:14.83 - <debug> session:1 Looking for plugin implementing op tflite_model_unload
2025.07.19-20:55:14.83 - <debug> Returning func from hint plugin tf
2025.07.19-20:55:14.83 - <debug> Found implementation in tf plugin
2025.07.19-20:55:14.83 - <debug> session:1 Unregistered resource 1
2025.07.19-20:55:14.83 - <debug> Released session 1
2025.07.19-20:55:14.83 - <debug> Removing file /run/user/0/vaccel/hsuZdP/resource.1/resnet18-v2-7_float32.tflite
2025.07.19-20:55:14.83 - <debug> Released resource 1
2025.07.19-20:55:14.83 - <debug> Cleaning up vAccel
2025.07.19-20:55:14.83 - <debug> Cleaning up sessions
2025.07.19-20:55:14.83 - <debug> Cleaning up resources
2025.07.19-20:55:14.83 - <debug> Cleaning up plugins
2025.07.19-20:55:14.83 - <debug> Unregistered plugin tf
```

## Using the vAccel Tensorflow bindings

This plugin includes bindings that implement simple inference operations. The
bindings can be used to run native Tensorflow application with vAccel. You can
find more information in the
[relevant page](../../../framework-bindings/tensorflow-bindings.md).
