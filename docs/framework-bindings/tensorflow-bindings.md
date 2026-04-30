# Tensorflow bindings

To take advantage of vAccel's plugin system, we provide Tensorflow bindings for
simple inference operations. With the use of bindings, native Tensorflow
applications can leverage vAccel to run inference without modifications to the
original code.

vAccel Tensorflow bindings are part of the vAccel Tensorflow plugin
distribution. You can find information on how to install the plugin at the
[relevant page](../plugins/available-plugins/acceleration-plugins/tf-plugin.md).

The next section assumes that you have installed vAccel and the Tensorflow
plugin following the plugin's documentation.

## Running a sample Tensorflow application with vAccel

Download a sample Tensorflow application:

```sh
git clone https://github.com/AmirulOm/tensorflow_capi_sample
cd tensorflow_capi_sample
```

and build it with:

```sh
gcc -I/usr/local/include -L/usr/local/lib main.c -ltensorflow -o tf_sample
```

Link the LSTM model provided with vAccel to the current dir, so the application
can find it:

```sh
ln -s /usr/local/share/vaccel/models/tf/lstm2 .
```

The application should run successfully with:

```console
$ ./tf_sample
2026-04-29 15:17:17.349003: I tensorflow/core/util/port.cc:153] oneDNN custom operations are on. You may see slightly different numerical results due to floating-point round-off errors from different computation orders. To turn them off, set the environment variable `TF_ENABLE_ONEDNN_OPTS=0`.
2026-04-29 15:17:17.361455: I tensorflow/cc/saved_model/reader.cc:83] Reading SavedModel from: lstm2/
2026-04-29 15:17:17.381109: I tensorflow/cc/saved_model/reader.cc:52] Reading meta graph with tags { serve }
2026-04-29 15:17:17.381161: I tensorflow/cc/saved_model/reader.cc:147] Reading SavedModel debug info (if present) from: lstm2/
2026-04-29 15:17:17.381236: I tensorflow/core/platform/cpu_feature_guard.cc:210] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.
To enable the following instructions: SSE3 SSE4.1 SSE4.2 AVX AVX2 AVX_VNNI FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.
2026-04-29 15:17:17.481898: I tensorflow/compiler/mlir/mlir_graph_optimization_pass.cc:388] MLIR V1 optimization pass is not enabled
2026-04-29 15:17:17.506970: I tensorflow/cc/saved_model/loader.cc:236] Restoring SavedModel bundle.
2026-04-29 15:17:17.598031: I tensorflow/cc/saved_model/loader.cc:220] Running initialization op on SavedModel bundle at path: lstm2/
2026-04-29 15:17:17.684118: I tensorflow/cc/saved_model/loader.cc:462] SavedModel load for tags { serve }; Status: success: OK. Took 322669 microseconds.
TF_LoadSessionFromSavedModel OK
TF_GraphOperationByName serving_default_input_1 is OK
TF_GraphOperationByName StatefulPartitionedCall is OK
TF_NewTensor is OK
Session is OK
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
```

After successfully executing the native application, you are ready to use it
with vAccel.

To execute the same binary with vAccel you need to first setup the plugin as
described in the relevant guide:

```sh
export VACCEL_PLUGINS=libvaccel-tf.so
export VACCEL_LOG_LEVEL=4
```

You can then use the bindings with `LD_PRELOAD`:

```console
$ LD_PRELOAD=/usr/local/lib/x86_64-linux-gnu/libvaccel-tf-bindings.so ./tf_sample
2026-04-29 15:17:41.476687: I tensorflow/core/util/port.cc:153] oneDNN custom operations are on. You may see slightly different numerical results due to floating-point round-off errors from different computation orders. To turn them off, set the environment variable `TF_ENABLE_ONEDNN_OPTS=0`.
2026-04-29 15:17:41.497650: I tensorflow/core/util/port.cc:153] oneDNN custom operations are on. You may see slightly different numerical results due to floating-point round-off errors from different computation orders. To turn them off, set the environment variable `TF_ENABLE_ONEDNN_OPTS=0`.
2026.04.29-15:17:41.45 - <debug> Initializing vAccel
2026.04.29-15:17:41.45 - <info> vAccel 0.7.1-93-ebc23b1f
2026.04.29-15:17:41.45 - <debug> Config:
2026.04.29-15:17:41.45 - <debug>   plugins = libvaccel-tf.so
2026.04.29-15:17:41.45 - <debug>   log_level = debug
2026.04.29-15:17:41.45 - <debug>   log_file = (null)
2026.04.29-15:17:41.45 - <debug>   profiling_enabled = false
2026.04.29-15:17:41.45 - <debug>   version_ignore = false
2026.04.29-15:17:41.45 - <debug> Created top-level rundir: /run/user/0/vaccel/LcX7hW
2026.04.29-15:17:41.50 - <info> Registered plugin tf 0.2.0-22-b9061d01
2026.04.29-15:17:41.50 - <debug> Registered op tf_model_load from plugin tf
2026.04.29-15:17:41.50 - <debug> Registered op tf_model_unload from plugin tf
2026.04.29-15:17:41.50 - <debug> Registered op tf_model_run from plugin tf
2026.04.29-15:17:41.50 - <debug> Registered op tflite_model_load from plugin tf
2026.04.29-15:17:41.50 - <debug> Registered op tflite_model_unload from plugin tf
2026.04.29-15:17:41.50 - <debug> Registered op tflite_model_run from plugin tf
2026.04.29-15:17:41.50 - <debug> Loaded plugin tf from libvaccel-tf.so
2026.04.29-15:17:41.50 - <debug> New rundir for session 1: /run/user/0/vaccel/LcX7hW/session.1
2026.04.29-15:17:41.50 - <debug> Initialized session 1 with plugin tf
2026.04.29-15:17:41.50 - <warn> Path does not seem to have a `<prefix>://`
2026.04.29-15:17:41.50 - <warn> Assuming lstm2/ is a local path
2026.04.29-15:17:41.50 - <debug> Initialized resource 1
2026.04.29-15:17:41.50 - <debug> session:1 Registered resource 1
2026.04.29-15:17:41.50 - <debug> session:1 Looking for func implementing op tf_model_load
2026.04.29-15:17:41.50 - <debug> Returning func for op tf_model_load from plugin tf
2026.04.29-15:17:41.50 - <debug> [tf] Loading session from SavedModel
2026-04-29 15:17:41.509281: I tensorflow/cc/saved_model/reader.cc:83] Reading SavedModel from: lstm2/
2026-04-29 15:17:41.528615: I tensorflow/cc/saved_model/reader.cc:52] Reading meta graph with tags { serve }
2026-04-29 15:17:41.528668: I tensorflow/cc/saved_model/reader.cc:147] Reading SavedModel debug info (if present) from: lstm2/
2026-04-29 15:17:41.528730: I tensorflow/core/platform/cpu_feature_guard.cc:210] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.
To enable the following instructions: SSE3 SSE4.1 SSE4.2 AVX AVX2 AVX_VNNI FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.
2026-04-29 15:17:41.620620: I tensorflow/compiler/mlir/mlir_graph_optimization_pass.cc:388] MLIR V1 optimization pass is not enabled
2026-04-29 15:17:41.646083: I tensorflow/cc/saved_model/loader.cc:236] Restoring SavedModel bundle.
2026-04-29 15:17:41.732098: I tensorflow/cc/saved_model/loader.cc:220] Running initialization op on SavedModel bundle at path: lstm2/
2026-04-29 15:17:41.815607: I tensorflow/cc/saved_model/loader.cc:462] SavedModel load for tags { serve }; Status: success: OK. Took 306330 microseconds.
2026.04.29-15:17:41.87 - <debug> [tf] Model loaded correctly
2026-04-29 15:17:41.873345: I tensorflow/cc/saved_model/reader.cc:83] Reading SavedModel from: lstm2/
2026-04-29 15:17:41.893528: I tensorflow/cc/saved_model/reader.cc:52] Reading meta graph with tags { serve }
2026-04-29 15:17:41.893586: I tensorflow/cc/saved_model/reader.cc:147] Reading SavedModel debug info (if present) from: lstm2/
2026-04-29 15:17:41.997364: I tensorflow/cc/saved_model/loader.cc:236] Restoring SavedModel bundle.
2026-04-29 15:17:42.075262: I tensorflow/cc/saved_model/loader.cc:220] Running initialization op on SavedModel bundle at path: lstm2/
2026-04-29 15:17:42.156119: I tensorflow/cc/saved_model/loader.cc:462] SavedModel load for tags { serve }; Status: success: OK. Took 282782 microseconds.
TF_LoadSessionFromSavedModel OK
TF_GraphOperationByName serving_default_input_1 is OK
TF_GraphOperationByName StatefulPartitionedCall is OK
TF_NewTensor is OK
2026.04.29-15:17:42.17 - <debug> session:1 Looking for func implementing op tf_model_run
2026.04.29-15:17:42.17 - <debug> Returning func for op tf_model_run from plugin tf
2026.04.29-15:17:42.17 - <debug> [tf] Running session
2026.04.29-15:17:42.58 - <debug> [tf] Success
Session is OK
2026.04.29-15:17:42.58 - <debug> session:1 Looking for func implementing op tf_model_unload
2026.04.29-15:17:42.58 - <debug> Returning func for op tf_model_unload from plugin tf
2026.04.29-15:17:42.58 - <debug> [tf] Deleting session
2026.04.29-15:17:42.61 - <debug> session:1 Unregistered resource 1
2026.04.29-15:17:42.61 - <debug> Released resource 1
2026.04.29-15:17:42.64 - <debug> Released session 1
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
2026.04.29-15:17:42.64 - <debug> Cleaning up vAccel
2026.04.29-15:17:42.64 - <debug> Cleaning up sessions
2026.04.29-15:17:42.64 - <debug> Cleaning up resources
2026.04.29-15:17:42.64 - <debug> Cleaning up plugins
2026.04.29-15:17:42.64 - <debug> Unregistered plugin tf
```
