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
wget https://github.com/nubificus/vaccel/releases/download/v[[ versions.vaccel ]]/vaccel-tf_[[ versions.plugins.tf ]]_x86_64.tar.gz
# Replace '/usr/local' below with the desired installation prefix
tar xfv vaccel-tf_[[ versions.plugins.tf ]]_x86_64.tar.gz --strip-components=2 -C /usr/local
# Update pkg-config files with the correct prefix
find /usr/local -name "vaccel-tf.pc" -exec sed -i 's:^\(prefix=\).*:\1/usr/local:g' {} \;
```

///

/// tab | ARM (64-bit)

```sh
wget https://github.com/nubificus/vaccel/releases/download/v[[ versions.vaccel ]]/vaccel-tf_[[ versions.plugins.tf ]]_aarch64.tar.gz
# Replace '/usr/local' below with the desired installation prefix
tar xfv vaccel-tf_[[ versions.plugins.tf ]]_aarch64.tar.gz --strip-components=2 -C /usr/local
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
https://s3.nbfc.io/nbfc-assets/github/vaccel/plugins/tf/rev/main/x86_64/release/vaccel-tf_latest_x86_64.tar.gz
```

///

/// tab | ARM (64-bit)

```sh
# TAR
https://s3.nbfc.io/nbfc-assets/github/vaccel/plugins/tf/rev/main/aarch64/release/vaccel-tf_latest_aarch64.tar.gz
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
2026-04-29 15:13:10.336778: I tensorflow/core/util/port.cc:153] oneDNN custom operations are on. You may see slightly different numerical results due to floating-point round-off errors from different computation orders. To turn them off, set the environment variable `TF_ENABLE_ONEDNN_OPTS=0`.
2026-04-29 15:13:10.358481: I tensorflow/core/util/port.cc:153] oneDNN custom operations are on. You may see slightly different numerical results due to floating-point round-off errors from different computation orders. To turn them off, set the environment variable `TF_ENABLE_ONEDNN_OPTS=0`.
2026.04.29-15:13:10.26 - <debug> Initializing vAccel
2026.04.29-15:13:10.26 - <info> vAccel 0.7.1-93-ebc23b1f
2026.04.29-15:13:10.26 - <debug> Config:
2026.04.29-15:13:10.26 - <debug>   plugins = libvaccel-tf.so
2026.04.29-15:13:10.26 - <debug>   log_level = debug
2026.04.29-15:13:10.26 - <debug>   log_file = (null)
2026.04.29-15:13:10.26 - <debug>   profiling_enabled = false
2026.04.29-15:13:10.26 - <debug>   version_ignore = false
2026.04.29-15:13:10.26 - <debug> Created top-level rundir: /run/user/0/vaccel/9QDV7g
2026.04.29-15:13:10.36 - <info> Registered plugin tf 0.2.0-22-b9061d01
2026.04.29-15:13:10.36 - <debug> Registered op tf_model_load from plugin tf
2026.04.29-15:13:10.36 - <debug> Registered op tf_model_unload from plugin tf
2026.04.29-15:13:10.36 - <debug> Registered op tf_model_run from plugin tf
2026.04.29-15:13:10.36 - <debug> Registered op tflite_model_load from plugin tf
2026.04.29-15:13:10.36 - <debug> Registered op tflite_model_unload from plugin tf
2026.04.29-15:13:10.36 - <debug> Registered op tflite_model_run from plugin tf
2026.04.29-15:13:10.36 - <debug> Loaded plugin tf from libvaccel-tf.so
2026.04.29-15:13:10.36 - <debug> Initialized resource 1
Initialized model resource 1
2026.04.29-15:13:10.36 - <debug> New rundir for session 1: /run/user/0/vaccel/9QDV7g/session.1
2026.04.29-15:13:10.36 - <debug> Initialized session 1 with plugin tf
Initialized vAccel session 1
2026.04.29-15:13:10.36 - <debug> New rundir for resource 1: /run/user/0/vaccel/9QDV7g/resource.1
2026.04.29-15:13:10.36 - <debug> Downloading https://s3.nbfc.io/models/tf/resnet18-v2-7_saved_model.tar.xz
2026.04.29-15:13:11.40 - <debug> Downloaded: 41.0 MB of 41.0 MB (100.0%) | Speed: 39.37 MB/sec
2026.04.29-15:13:11.40 - <debug> Download completed successfully
2026.04.29-15:13:11.40 - <debug> session:1 Registered resource 1
2026.04.29-15:13:11.40 - <debug> session:1 Looking for func implementing op tf_model_load
2026.04.29-15:13:11.40 - <debug> Returning func for op tf_model_load from plugin tf
2026.04.29-15:13:13.52 - <debug> [tf] Loading session from SavedModel
2026.04.29-15:13:13.53 - <debug> [tf] Extracting: /run/user/0/vaccel/9QDV7g/resource.1/resnet18-v2-7_saved_model/
2026.04.29-15:13:13.53 - <debug> [tf] Extracting: /run/user/0/vaccel/9QDV7g/resource.1/resnet18-v2-7_saved_model/assets/
2026.04.29-15:13:13.53 - <debug> [tf] Extracting: /run/user/0/vaccel/9QDV7g/resource.1/resnet18-v2-7_saved_model/fingerprint.pb
2026.04.29-15:13:13.53 - <debug> [tf] Extracting: /run/user/0/vaccel/9QDV7g/resource.1/resnet18-v2-7_saved_model/saved_model.pb
2026.04.29-15:13:15.66 - <debug> [tf] Extracting: /run/user/0/vaccel/9QDV7g/resource.1/resnet18-v2-7_saved_model/variables/
2026.04.29-15:13:15.66 - <debug> [tf] Extracting: /run/user/0/vaccel/9QDV7g/resource.1/resnet18-v2-7_saved_model/variables/variables.data-00000-of-00001
2026.04.29-15:13:15.66 - <debug> [tf] Extracting: /run/user/0/vaccel/9QDV7g/resource.1/resnet18-v2-7_saved_model/variables/variables.index
2026-04-29 15:13:15.669831: I tensorflow/cc/saved_model/reader.cc:83] Reading SavedModel from: /run/user/0/vaccel/9QDV7g/resource.1/resnet18-v2-7_saved_model
2026-04-29 15:13:15.690971: I tensorflow/cc/saved_model/reader.cc:52] Reading meta graph with tags { serve }
2026-04-29 15:13:15.691028: I tensorflow/cc/saved_model/reader.cc:147] Reading SavedModel debug info (if present) from: /run/user/0/vaccel/9QDV7g/resource.1/resnet18-v2-7_saved_model
2026-04-29 15:13:15.691160: I tensorflow/core/platform/cpu_feature_guard.cc:210] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.
To enable the following instructions: SSE3 SSE4.1 SSE4.2 AVX AVX2 AVX_VNNI FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.
2026-04-29 15:13:15.777876: I tensorflow/compiler/mlir/mlir_graph_optimization_pass.cc:388] MLIR V1 optimization pass is not enabled
2026-04-29 15:13:15.778679: I tensorflow/cc/saved_model/loader.cc:236] Restoring SavedModel bundle.
2026-04-29 15:13:15.815605: I tensorflow/cc/saved_model/loader.cc:220] Running initialization op on SavedModel bundle at path: /run/user/0/vaccel/9QDV7g/resource.1/resnet18-v2-7_saved_model
2026-04-29 15:13:15.849330: I tensorflow/cc/saved_model/loader.cc:462] SavedModel load for tags { serve }; Status: success: OK. Took 179498 microseconds.
2026.04.29-15:13:15.90 - <debug> [tf] Model loaded correctly
Session load status => code:0 message:
2026.04.29-15:13:15.91 - <debug> session:1 Looking for func implementing op tf_model_run
2026.04.29-15:13:15.91 - <debug> Returning func for op tf_model_run from plugin tf
2026.04.29-15:13:15.91 - <debug> [tf] Running session
2026.04.29-15:13:16.65 - <debug> [tf] Success
Session run status => code:0 message:
Success!
Output tensor => type:1 nr_dims:2 size:4000B
Prediction: banana
2026.04.29-15:13:16.65 - <debug> session:1 Looking for func implementing op tf_model_unload
2026.04.29-15:13:16.65 - <debug> Returning func for op tf_model_unload from plugin tf
2026.04.29-15:13:16.65 - <debug> [tf] Deleting session
2026.04.29-15:13:16.66 - <debug> [tf] Removed file: /run/user/0/vaccel/9QDV7g/resource.1/resnet18-v2-7_saved_model/fingerprint.pb
2026.04.29-15:13:16.66 - <debug> [tf] Removed file: /run/user/0/vaccel/9QDV7g/resource.1/resnet18-v2-7_saved_model/variables/variables.index
2026.04.29-15:13:16.66 - <debug> [tf] Removed file: /run/user/0/vaccel/9QDV7g/resource.1/resnet18-v2-7_saved_model/variables/variables.data-00000-of-00001
2026.04.29-15:13:16.66 - <debug> [tf] Removed directory: /run/user/0/vaccel/9QDV7g/resource.1/resnet18-v2-7_saved_model/variables
2026.04.29-15:13:16.66 - <debug> [tf] Removed file: /run/user/0/vaccel/9QDV7g/resource.1/resnet18-v2-7_saved_model/saved_model.pb
2026.04.29-15:13:16.66 - <debug> [tf] Removed directory: /run/user/0/vaccel/9QDV7g/resource.1/resnet18-v2-7_saved_model/assets
2026.04.29-15:13:16.66 - <debug> [tf] Removed directory: /run/user/0/vaccel/9QDV7g/resource.1/resnet18-v2-7_saved_model
Session delete status => code:0 message:
2026.04.29-15:13:16.66 - <debug> session:1 Unregistered resource 1
2026.04.29-15:13:16.66 - <debug> Released session 1
2026.04.29-15:13:16.66 - <debug> Removing file /run/user/0/vaccel/9QDV7g/resource.1/resnet18-v2-7_saved_model.tar.xz
2026.04.29-15:13:16.67 - <debug> Released resource 1
2026.04.29-15:13:16.67 - <debug> Cleaning up vAccel
2026.04.29-15:13:16.67 - <debug> Cleaning up sessions
2026.04.29-15:13:16.67 - <debug> Cleaning up resources
2026.04.29-15:13:16.67 - <debug> Cleaning up plugins
2026.04.29-15:13:16.67 - <debug> Unregistered plugin tf
```

You can also run a similar inference example using Tensorflow Lite with:

```console
$ tflite_inference \
      /usr/local/share/vaccel/images/example.jpg \
      https://s3.nbfc.io/models/tf/resnet18-v2-7_float32.tflite \
      /usr/local/share/vaccel/labels/imagenet.txt
2026-04-29 15:14:03.525122: I tensorflow/core/util/port.cc:153] oneDNN custom operations are on. You may see slightly different numerical results due to floating-point round-off errors from different computation orders. To turn them off, set the environment variable `TF_ENABLE_ONEDNN_OPTS=0`.
2026-04-29 15:14:03.546097: I tensorflow/core/util/port.cc:153] oneDNN custom operations are on. You may see slightly different numerical results due to floating-point round-off errors from different computation orders. To turn them off, set the environment variable `TF_ENABLE_ONEDNN_OPTS=0`.
2026.04.29-15:14:03.49 - <debug> Initializing vAccel
2026.04.29-15:14:03.49 - <info> vAccel 0.7.1-93-ebc23b1f
2026.04.29-15:14:03.49 - <debug> Config:
2026.04.29-15:14:03.49 - <debug>   plugins = libvaccel-tf.so
2026.04.29-15:14:03.49 - <debug>   log_level = debug
2026.04.29-15:14:03.49 - <debug>   log_file = (null)
2026.04.29-15:14:03.49 - <debug>   profiling_enabled = false
2026.04.29-15:14:03.49 - <debug>   version_ignore = false
2026.04.29-15:14:03.49 - <debug> Created top-level rundir: /run/user/0/vaccel/NFiJEK
2026.04.29-15:14:03.54 - <info> Registered plugin tf 0.2.0-22-b9061d01
2026.04.29-15:14:03.54 - <debug> Registered op tf_model_load from plugin tf
2026.04.29-15:14:03.54 - <debug> Registered op tf_model_unload from plugin tf
2026.04.29-15:14:03.54 - <debug> Registered op tf_model_run from plugin tf
2026.04.29-15:14:03.54 - <debug> Registered op tflite_model_load from plugin tf
2026.04.29-15:14:03.54 - <debug> Registered op tflite_model_unload from plugin tf
2026.04.29-15:14:03.54 - <debug> Registered op tflite_model_run from plugin tf
2026.04.29-15:14:03.54 - <debug> Loaded plugin tf from libvaccel-tf.so
2026.04.29-15:14:03.54 - <debug> Initialized resource 1
Initialized model resource 1
2026.04.29-15:14:03.54 - <debug> New rundir for session 1: /run/user/0/vaccel/NFiJEK/session.1
2026.04.29-15:14:03.54 - <debug> Initialized session 1 with plugin tf
Initialized vAccel session 1
2026.04.29-15:14:03.54 - <debug> New rundir for resource 1: /run/user/0/vaccel/NFiJEK/resource.1
2026.04.29-15:14:03.54 - <debug> Downloading https://s3.nbfc.io/models/tf/resnet18-v2-7_float32.tflite
2026.04.29-15:14:04.73 - <debug> Downloaded: 44.6 MB of 44.6 MB (100.0%) | Speed: 37.63 MB/sec
2026.04.29-15:14:04.73 - <debug> Download completed successfully
2026.04.29-15:14:04.73 - <debug> session:1 Registered resource 1
2026.04.29-15:14:04.73 - <debug> session:1 Looking for func implementing op tflite_model_load
2026.04.29-15:14:04.73 - <debug> Returning func for op tflite_model_load from plugin tf
2026.04.29-15:14:04.73 - <debug> [tf][tflite] Loading session from model
2026.04.29-15:14:04.73 - <debug> [tf][tflite] Model loaded correctly
2026.04.29-15:14:04.74 - <debug> session:1 Looking for func implementing op tflite_model_run
2026.04.29-15:14:04.74 - <debug> Returning func for op tflite_model_run from plugin tf
2026.04.29-15:14:04.74 - <debug> [tf][tflite] Running session
2026.04.29-15:14:04.84 - <debug> [tf][tflite] Success
Session run status: 0
Success!
Output tensor => type:1 nr_dims:2 size:4000B
Prediction: banana
2026.04.29-15:14:04.84 - <debug> session:1 Looking for func implementing op tflite_model_unload
2026.04.29-15:14:04.84 - <debug> Returning func for op tflite_model_unload from plugin tf
2026.04.29-15:14:04.84 - <debug> session:1 Unregistered resource 1
2026.04.29-15:14:04.84 - <debug> Released session 1
2026.04.29-15:14:04.84 - <debug> Removing file /run/user/0/vaccel/NFiJEK/resource.1/resnet18-v2-7_float32.tflite
2026.04.29-15:14:04.85 - <debug> Released resource 1
2026.04.29-15:14:04.85 - <debug> Cleaning up vAccel
2026.04.29-15:14:04.85 - <debug> Cleaning up sessions
2026.04.29-15:14:04.85 - <debug> Cleaning up resources
2026.04.29-15:14:04.85 - <debug> Cleaning up plugins
2026.04.29-15:14:04.85 - <debug> Unregistered plugin tf
```

## Using the vAccel Tensorflow bindings

This plugin includes bindings that implement simple inference operations. The
bindings can be used to run native Tensorflow application with vAccel. You can
find more information in the
[relevant page](../../../framework-bindings/tensorflow-bindings.md).
