# Tensorflow Plugin

The Tensorflow plugin for vAccel implements basic
[Tensorflow](https://www.tensorflow.org/) and Tensorflow Lite support for vAccel
operations.

## Supported operations

- [TensorFlow session load](../../../api/api-reference/operations.md#tensorflow-session-load)
- [TensorFlow session run](../../../api/api-reference/operations.md#tensorflow-session-run)
- [TensorFlow session delete](../../../api/api-reference/operations.md#tensorflow-session-delete)
- [TensorFlow Lite session load](../../../api/api-reference/operations.md#tensorflow-lite-session-load)
- [TensorFlow Lite session run](../../../api/api-reference/operations.md#tensorflow-lite-session-run)
- [TensorFlow Lite session delete](../../../api/api-reference/operations.md#tensorflow-lite-session-delete)

## Installing Tensorflow and Tensorflow Lite C/C++ API files

You can find instructions on how to install the required files
[here](../../../useful-docs/build-and-install-tensorflow.md). The rest of this
guide assumes Tensorflow is installed at `/usr/local` and its' libraries are at
`/usr/local/lib`.

## Installing the plugin

You can get the latest Tensorflow plugin binary release from the
[Releases](https://github.com/nubificus/vaccel/releases) page of the vAccel
repository. Releases include binaries for x86_64/aarch64 Ubuntu-based systems.

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

Assuming vAccel is installed at `/usr/local`, you can run an inference with a
predefined example tensor using an LSTM model with:

```console
$ tf_inference /usr/local/share/vaccel/models/tf/lstm2
2025.03.25-21:34:23.66 - <debug> Initializing vAccel
2025.03.25-21:34:23.66 - <info> vAccel 0.6.1-194-19056528
2025.03.25-21:34:23.66 - <debug> Config:
2025.03.25-21:34:23.66 - <debug>   plugins = libvaccel-tf.so
2025.03.25-21:34:23.66 - <debug>   log_level = debug
2025.03.25-21:34:23.66 - <debug>   log_file = (null)
2025.03.25-21:34:23.66 - <debug>   profiling_enabled = false
2025.03.25-21:34:23.66 - <debug>   version_ignore = false
2025.03.25-21:34:23.66 - <debug> Created top-level rundir: /run/user/1002/vaccel/PtFMrH
2025.03.25-21:34:23.80 - <info> Registered plugin tf 0.1.0-19-4b4dc788
2025.03.25-21:34:23.80 - <debug> Registered op tf_session_load from plugin tf
2025.03.25-21:34:23.80 - <debug> Registered op tf_session_run from plugin tf
2025.03.25-21:34:23.80 - <debug> Registered op tf_session_delete from plugin tf
2025.03.25-21:34:23.80 - <debug> Registered op tflite_session_load from plugin tf
2025.03.25-21:34:23.80 - <debug> Registered op tflite_session_run from plugin tf
2025.03.25-21:34:23.80 - <debug> Registered op tflite_session_delete from plugin tf
2025.03.25-21:34:23.80 - <debug> Loaded plugin tf from libvaccel-tf.so
2025.03.25-21:34:23.80 - <warn> Path does not seem to have a `<prefix>://`
2025.03.25-21:34:23.80 - <warn> Assuming /usr/local/share/vaccel/models/tf/lstm2 is a local path
2025.03.25-21:34:23.80 - <debug> Initialized resource 1
Initialized model resource 1
2025.03.25-21:34:23.80 - <debug> New rundir for session 1: /run/user/1002/vaccel/PtFMrH/session.1
2025.03.25-21:34:23.80 - <debug> Initialized session 1
Initialized vAccel session 1
2025.03.25-21:34:23.80 - <debug> session:1 Registered resource 1
2025.03.25-21:34:23.80 - <debug> session:1 Looking for plugin implementing tf_session_load operation
2025.03.25-21:34:23.80 - <debug> Returning func from hint plugin tf
2025.03.25-21:34:23.80 - <debug> Found implementation in tf plugin
2025.03.25-21:34:23.80 - <debug> [tf] Loading session from SavedModel
2025-03-25 21:34:23.820031: I tensorflow/cc/saved_model/reader.cc:83] Reading SavedModel from: /usr/local/share/vaccel
/models/tf/lstm2
2025-03-25 21:34:23.867800: I tensorflow/cc/saved_model/reader.cc:52] Reading meta graph with tags { serve }
2025-03-25 21:34:23.867858: I tensorflow/cc/saved_model/reader.cc:147] Reading SavedModel debug info (if present) from
: /usr/local/share/vaccel/models/tf/lstm2
2025-03-25 21:34:23.867941: I tensorflow/core/platform/cpu_feature_guard.cc:210] This TensorFlow binary is optimized t
o use available CPU instructions in performance-critical operations.
To enable the following instructions: SSE3 SSE4.1 SSE4.2 AVX AVX2 FMA, in other operations, rebuild TensorFlow with th
e appropriate compiler flags.
2025-03-25 21:34:24.053927: I tensorflow/compiler/mlir/mlir_graph_optimization_pass.cc:388] MLIR V1 optimization pass
is not enabled
2025-03-25 21:34:24.105271: I tensorflow/cc/saved_model/loader.cc:236] Restoring SavedModel bundle.
2025-03-25 21:34:24.274470: I tensorflow/cc/saved_model/loader.cc:220] Running initialization op on SavedModel bundle
at path: /usr/local/share/vaccel/models/tf/lstm2
2025-03-25 21:34:24.420425: I tensorflow/cc/saved_model/loader.cc:462] SavedModel load for tags { serve }; Status: suc
cess: OK. Took 600418 microseconds.
2025.03.25-21:34:24.45 - <debug> Model from path loaded correctly
2025.03.25-21:34:24.51 - <debug> session:1 Looking for plugin implementing tf_session_run operation
2025.03.25-21:34:24.51 - <debug> Returning func from hint plugin tf
2025.03.25-21:34:24.51 - <debug> Found implementation in tf plugin
2025.03.25-21:34:24.51 - <debug> [tf] Running session
2025.03.25-21:34:25.15 - <debug> [tf] Success
Success!
Output tensor => type:1 nr_dims:3
dim[0]: 1
dim[1]: 30
dim[2]: 61
Result Tensor :
0.016328
0.016542
0.015824
0.016457
0.016535
0.016574
0.016449
0.016437
0.016353
0.016246
2025.03.25-21:34:25.15 - <debug> session:1 Looking for plugin implementing tf_session_delete operation
2025.03.25-21:34:25.15 - <debug> Returning func from hint plugin tf
2025.03.25-21:34:25.15 - <debug> Found implementation in tf plugin
2025.03.25-21:34:25.15 - <debug> [tf] Deleting session
2025.03.25-21:34:25.21 - <debug> session:1 Unregistered resource 1
2025.03.25-21:34:25.21 - <debug> Released session 1
2025.03.25-21:34:25.21 - <debug> Released resource 1
2025.03.25-21:34:25.21 - <debug> Cleaning up vAccel
2025.03.25-21:34:25.21 - <debug> Cleaning up sessions
2025.03.25-21:34:25.21 - <debug> Cleaning up resources
2025.03.25-21:34:25.21 - <debug> Cleaning up plugins
2025.03.25-21:34:25.21 - <debug> Unregistered plugin tf
```

You can also run a similar inference example using Tensorflow Lite with:

```console
$ tflite_inference /usr/local/share/vaccel/models/tf/lstm2.tflite
2025.03.25-21:34:25.26 - <debug> Initializing vAccel
2025.03.25-21:34:25.26 - <info> vAccel 0.6.1-194-19056528
2025.03.25-21:34:25.26 - <debug> Config:
2025.03.25-21:34:25.26 - <debug>   plugins = libvaccel-tf.so
2025.03.25-21:34:25.26 - <debug>   log_level = debug
2025.03.25-21:34:25.26 - <debug>   log_file = (null)
2025.03.25-21:34:25.26 - <debug>   profiling_enabled = false
2025.03.25-21:34:25.26 - <debug>   version_ignore = false
2025.03.25-21:34:25.26 - <debug> Created top-level rundir: /run/user/1002/vaccel/FTv8yO
2025.03.25-21:34:25.36 - <info> Registered plugin tf 0.1.0-19-4b4dc788
2025.03.25-21:34:25.36 - <debug> Registered op tf_session_load from plugin tf
2025.03.25-21:34:25.36 - <debug> Registered op tf_session_run from plugin tf
2025.03.25-21:34:25.36 - <debug> Registered op tf_session_delete from plugin tf
2025.03.25-21:34:25.36 - <debug> Registered op tflite_session_load from plugin tf
2025.03.25-21:34:25.36 - <debug> Registered op tflite_session_run from plugin tf
2025.03.25-21:34:25.36 - <debug> Registered op tflite_session_delete from plugin tf
2025.03.25-21:34:25.36 - <debug> Loaded plugin tf from libvaccel-tf.so
2025.03.25-21:34:25.36 - <warn> Path does not seem to have a `<prefix>://`
2025.03.25-21:34:25.36 - <warn> Assuming /usr/local/share/vaccel/models/tf/lstm2.tflite is a local path
2025.03.25-21:34:25.36 - <debug> Initialized resource 1
Initialized model resource 1
2025.03.25-21:34:25.36 - <debug> New rundir for session 1: /run/user/1002/vaccel/FTv8yO/session.1
2025.03.25-21:34:25.36 - <debug> Initialized session 1
Initialized vAccel session 1
2025.03.25-21:34:25.36 - <debug> New rundir for resource 1: /run/user/1002/vaccel/FTv8yO/resource.1
2025.03.25-21:34:25.36 - <debug> session:1 Registered resource 1
2025.03.25-21:34:25.36 - <debug> session:1 Looking for plugin implementing tflite_session_load operation
2025.03.25-21:34:25.36 - <debug> Returning func from hint plugin tf
2025.03.25-21:34:25.36 - <debug> Found implementation in tf plugin
2025.03.25-21:34:25.36 - <debug> [tf][tflite] Loading session from model
INFO: Created TensorFlow Lite delegate for select TF ops.
2025-03-25 21:34:25.389384: I tensorflow/core/platform/cpu_feature_guard.cc:210] This TensorFlow binary is optimized t
o use available CPU instructions in performance-critical operations.
To enable the following instructions: SSE3 SSE4.1 SSE4.2 AVX AVX2 FMA, in other operations, rebuild TensorFlow with th
e appropriate compiler flags.
INFO: TfLiteFlexDelegate delegate: 3 nodes delegated out of 22 nodes with 2 partitions.

2025-03-25 21:34:25.414751: E tensorflow/core/framework/node_def_util.cc:676] NodeDef mentions attribute use_inter_op_
parallelism which is not in the op definition: Op<name=TensorListReserve; signature=element_shape:shape_type, num_elem
ents:int32 -> handle:variant; attr=element_dtype:type; attr=shape_type:type,allowed=[DT_INT32, DT_INT64]> This may be
expected if your graph generating binary is newer  than this binary. Unknown attributes will be ignored. NodeDef: {{no
de TensorListReserve}}
2025.03.25-21:34:25.41 - <debug> [tf][tflite] Model from path loaded correctly
2025.03.25-21:34:25.41 - <debug> session:1 Looking for plugin implementing tflite_session_run operation
2025.03.25-21:34:25.41 - <debug> Returning func from hint plugin tf
2025.03.25-21:34:25.41 - <debug> Found implementation in tf plugin
2025.03.25-21:34:25.41 - <debug> [tf][tflite] Running session
2025.03.25-21:34:25.41 - <debug> [tf][tflite] Success
Success!
Output tensor => type:1 nr_dims:3
dim[0]: 1
dim[1]: 30
dim[2]: 61
Result Tensor :
0.016326
0.016310
0.016321
0.016421
0.016605
0.016541
0.016572
0.016317
0.016377
0.016299
2025.03.25-21:34:25.41 - <debug> session:1 Looking for plugin implementing tflite_session_delete operation
2025.03.25-21:34:25.41 - <debug> Returning func from hint plugin tf
2025.03.25-21:34:25.41 - <debug> Found implementation in tf plugin
2025.03.25-21:34:25.42 - <debug> session:1 Unregistered resource 1
2025.03.25-21:34:25.42 - <debug> Released session 1
2025.03.25-21:34:25.42 - <debug> Released resource 1
2025.03.25-21:34:25.42 - <debug> Cleaning up vAccel
2025.03.25-21:34:25.42 - <debug> Cleaning up sessions
2025.03.25-21:34:25.42 - <debug> Cleaning up resources
2025.03.25-21:34:25.42 - <debug> Cleaning up plugins
2025.03.25-21:34:25.42 - <debug> Unregistered plugin tf
```

## Using the vAccel Tensorflow bindings

This plugin includes bindings that implement simple inference operations. The
bindings can be used to run native Tensorflow application with vAccel. You can
find more information in the
[relevant page](../../../framework-bindings/tensorflow-bindings.md).
