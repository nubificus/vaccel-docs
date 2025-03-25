# vAccel Tensorflow Bindings

To take advantage of vAccel's plugin system, we provide Tensorflow bindings for
simple inference operations. With the use of bindings, native Tensorflow
applications can leverage vAccel to run inference without modifications to the
original code.

vAccel Tensorflow bindings are part of the vAccel Tensorflow plugin
distribution. You can find information on how to install the plugin at the
[relevant page](plugins/acceleration/tf.md).

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
2025-03-25 22:13:43.955282: I tensorflow/cc/saved_model/reader.cc:52] Reading meta graph with tags { serve }
2025-03-25 22:13:43.955340: I tensorflow/cc/saved_model/reader.cc:147] Reading SavedModel debug info (if present) from: lstm2/
2025-03-25 22:13:43.955394: I tensorflow/core/platform/cpu_feature_guard.cc:210] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.
To enable the following instructions: SSE3 SSE4.1 SSE4.2 AVX AVX2 FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.
2025-03-25 22:13:44.161071: I tensorflow/compiler/mlir/mlir_graph_optimization_pass.cc:388] MLIR V1 optimization pass is not enabled
2025-03-25 22:13:44.203364: I tensorflow/cc/saved_model/loader.cc:236] Restoring SavedModel bundle.
2025-03-25 22:13:44.365220: I tensorflow/cc/saved_model/loader.cc:220] Running initialization op on SavedModel bundle at path: lstm2/
2025-03-25 22:13:44.499266: I tensorflow/cc/saved_model/loader.cc:462] SavedModel load for tags { serve }; Status: success: OK. Took 593575 microseconds.
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
2025.03.25-22:27:30.34 - <debug> Initializing vAccel
2025.03.25-22:27:30.34 - <info> vAccel 0.6.1-194-19056528
2025.03.25-22:27:30.34 - <debug> Config:
2025.03.25-22:27:30.34 - <debug>   plugins = libvaccel-tf.so
2025.03.25-22:27:30.34 - <debug>   log_level = debug
2025.03.25-22:27:30.34 - <debug>   log_file = (null)
2025.03.25-22:27:30.34 - <debug>   profiling_enabled = false
2025.03.25-22:27:30.34 - <debug>   version_ignore = false
2025.03.25-22:27:30.34 - <debug> Created top-level rundir: /run/user/1002/vaccel/8IBBqO
2025.03.25-22:27:30.44 - <info> Registered plugin tf 0.1.0-21-3cb5453e
2025.03.25-22:27:30.44 - <debug> Registered op tf_session_load from plugin tf
2025.03.25-22:27:30.44 - <debug> Registered op tf_session_run from plugin tf
2025.03.25-22:27:30.44 - <debug> Registered op tf_session_delete from plugin tf
2025.03.25-22:27:30.44 - <debug> Registered op tflite_session_load from plugin tf
2025.03.25-22:27:30.44 - <debug> Registered op tflite_session_run from plugin tf
2025.03.25-22:27:30.44 - <debug> Registered op tflite_session_delete from plugin tf
2025.03.25-22:27:30.44 - <debug> Loaded plugin tf from libvaccel-tf.so
2025.03.25-22:27:30.45 - <debug> New rundir for session 1: /run/user/1002/vaccel/8IBBqO/session.1
2025.03.25-22:27:30.45 - <debug> Initialized session 1
2025.03.25-22:27:30.45 - <warn> Path does not seem to have a `<prefix>://`
2025.03.25-22:27:30.45 - <warn> Assuming lstm2/ is a local path
2025.03.25-22:27:30.45 - <debug> Initialized resource 1
2025.03.25-22:27:30.45 - <debug> session:1 Registered resource 1
2025.03.25-22:27:30.45 - <debug> session:1 Looking for plugin implementing tf_session_load operation
2025.03.25-22:27:30.45 - <debug> Returning func from hint plugin tf
2025.03.25-22:27:30.45 - <debug> Found implementation in tf plugin
2025.03.25-22:27:30.45 - <debug> [tf] Loading session from SavedModel
2025-03-25 22:27:30.459234: I tensorflow/cc/saved_model/reader.cc:83] Reading SavedModel from: lstm2/
2025-03-25 22:27:30.502324: I tensorflow/cc/saved_model/reader.cc:52] Reading meta graph with tags { serve }
2025-03-25 22:27:30.502381: I tensorflow/cc/saved_model/reader.cc:147] Reading SavedModel debug info (if present) from: lstm2/
2025-03-25 22:27:30.502437: I tensorflow/core/platform/cpu_feature_guard.cc:210] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.
To enable the following instructions: SSE3 SSE4.1 SSE4.2 AVX AVX2 FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.
2025-03-25 22:27:30.694945: I tensorflow/compiler/mlir/mlir_graph_optimization_pass.cc:388] MLIR V1 optimization pass is not enabled
2025-03-25 22:27:30.751997: I tensorflow/cc/saved_model/loader.cc:236] Restoring SavedModel bundle.
2025-03-25 22:27:30.924794: I tensorflow/cc/saved_model/loader.cc:220] Running initialization op on SavedModel bundle at path: lstm2/
2025-03-25 22:27:31.080011: I tensorflow/cc/saved_model/loader.cc:462] SavedModel load for tags { serve }; Status: success: OK. Took 620801 microseconds.
2025.03.25-22:27:31.11 - <debug> Model from path loaded correctly
2025-03-25 22:27:31.188347: I tensorflow/cc/saved_model/reader.cc:83] Reading SavedModel from: lstm2/
2025-03-25 22:27:31.236284: I tensorflow/cc/saved_model/reader.cc:52] Reading meta graph with tags { serve }
2025-03-25 22:27:31.236342: I tensorflow/cc/saved_model/reader.cc:147] Reading SavedModel debug info (if present) from: lstm2/
2025-03-25 22:27:31.466623: I tensorflow/cc/saved_model/loader.cc:236] Restoring SavedModel bundle.
2025-03-25 22:27:31.621523: I tensorflow/cc/saved_model/loader.cc:220] Running initialization op on SavedModel bundle at path: lstm2/
2025-03-25 22:27:31.777220: I tensorflow/cc/saved_model/loader.cc:462] SavedModel load for tags { serve }; Status: success: OK. Took 588881 microseconds.
TF_LoadSessionFromSavedModel OK
TF_GraphOperationByName serving_default_input_1 is OK
TF_GraphOperationByName StatefulPartitionedCall is OK
TF_NewTensor is OK
2025.03.25-22:27:31.81 - <debug> session:1 Looking for plugin implementing tf_session_run operation
2025.03.25-22:27:31.81 - <debug> Returning func from hint plugin tf
2025.03.25-22:27:31.81 - <debug> Found implementation in tf plugin
2025.03.25-22:27:31.81 - <debug> [tf] Running session
2025.03.25-22:27:32.49 - <debug> [tf] Success
Session is OK
2025.03.25-22:27:32.49 - <debug> session:1 Looking for plugin implementing tf_session_delete operation
2025.03.25-22:27:32.49 - <debug> Returning func from hint plugin tf
2025.03.25-22:27:32.49 - <debug> Found implementation in tf plugin
2025.03.25-22:27:32.49 - <debug> [tf] Deleting session
2025.03.25-22:27:32.59 - <debug> session:1 Unregistered resource 1
2025.03.25-22:27:32.59 - <debug> Released resource 1
2025.03.25-22:27:32.69 - <debug> Released session 1
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
2025.03.25-22:27:32.69 - <debug> Cleaning up vAccel
2025.03.25-22:27:32.69 - <debug> Cleaning up sessions
2025.03.25-22:27:32.69 - <debug> Cleaning up resources
2025.03.25-22:27:32.69 - <debug> Cleaning up plugins
2025.03.25-22:27:32.69 - <debug> Unregistered plugin tf
```
