# NoOp Plugin

The NoOp plugin for vAccel provides dummy implementations for vAccel operations.
It is meant a way to verify vAccel setups and operation usage.

## Supported operations

- [Image classification](../../../api/api-reference/operations.md#image-classification)
- [Image segmentation](../../../api/api-reference/operations.md#image-segmentation)
- [Object detection](../../../api/api-reference/operations.md#object-detection)
- [Pose estimation](../../../api/api-reference/operations.md#pose-estimation)
- [Monocular depth](../../../api/api-reference/operations.md#monocular-depth)

- [Matrix-to-matrix multiplication](../../../api/api-reference/operations.md#matrix-to-matrix-multiplication)
- [Array copy](../../../api/api-reference/operations.md#array-copy)
- [Matrix-to-matrix multiplication simple](../../../api/api-reference/operations.md#matrix-to-matrix-multiplication-simple)
- [Matrix-to-matrix multiplication and addition simple](../../../api/api-reference/operations.md#matrix-to-matrix-multiplication-and-addition-simple-wip)
- [Vector add](../../../api/api-reference/operations.md#vector-add)

- [Exec](../../../api/api-reference/operations.md#exec)
- [Exec with resource](../../../api/api-reference/operations.md#exec-with-resource)

- [TensorFlow model load](../../../api/api-reference/operations.md#tensorflow-model-load)
- [TensorFlow model unload](../../../api/api-reference/operations.md#tensorflow-model-unload)
- [TensorFlow model run](../../../api/api-reference/operations.md#tensorflow-model-run)
- [TensorFlow Lite model load](../../../api/api-reference/operations.md#tensorflow-lite-model-load)
- [TensorFlow Lite model unload](../../../api/api-reference/operations.md#tensorflow-lite-model-unload)
- [TensorFlow Lite model run](../../../api/api-reference/operations.md#tensorflow-lite-model-run)

- [Torch model load](../../../api/api-reference/operations.md#torch-model-load)
- [Torch model run](../../../api/api-reference/operations.md#torch-model-run)
- [Torch matrix-to-matrix multiplication](../../../api/api-reference/operations.md#torch-matrix-to-matrix-multiplication)

- [MinMax](../../../api/api-reference/operations.md#minmax)
- [Generic operation](../../../api/api-reference/operations.md#generic-operation)
- [Debug operation](../../../api/api-reference/operations.md#debug-operation)

## Installing the plugin

The plugin comes bundled with the core vAccel installation. Find out more on how
to install vAccel at the
[Installation](../../../getting-started/installation.md) page.

## Usage

To specify NoOp plugin as the selected plugin for vAccel execution:

```sh
export VACCEL_PLUGINS=libvaccel-noop.so
```

Ensure vAccel and the NoOp plugin libraries are in the library search paths
before trying to use the plugin.

## Running an example

Export the necessary variables for the plugin:

```sh
export VACCEL_PLUGINS=libvaccel-noop.so
# Optionally, for verbose output
export VACCEL_LOG_LEVEL=4
```

Assuming vAccel is installed at `/usr/local`, you can run a dummy image
classification with:

```console
$ VACCEL_PLUGINS=libvaccel-noop.so VACCEL_LOG_LEVEL=4 classify /usr/local/share/vaccel/images/example.jpg
2026.04.29-00:55:09.96 - <debug> Initializing vAccel
2026.04.29-00:55:09.96 - <info> vAccel 0.7.1-93-ebc23b1f
2026.04.29-00:55:09.96 - <debug> Config:
2026.04.29-00:55:09.96 - <debug>   plugins = libvaccel-noop.so
2026.04.29-00:55:09.96 - <debug>   log_level = debug
2026.04.29-00:55:09.96 - <debug>   log_file = (null)
2026.04.29-00:55:09.96 - <debug>   profiling_enabled = false
2026.04.29-00:55:09.96 - <debug>   version_ignore = false
2026.04.29-00:55:09.96 - <debug> Created top-level rundir: /run/user/0/vaccel/b1vi3E
2026.04.29-00:55:09.96 - <info> Registered plugin noop 0.7.1-93-ebc23b1f
2026.04.29-00:55:09.96 - <debug> Registered op noop from plugin noop
2026.04.29-00:55:09.96 - <debug> Registered op exec from plugin noop
2026.04.29-00:55:09.96 - <debug> Registered op exec_with_resource from plugin noop
2026.04.29-00:55:09.96 - <debug> Registered op image_classify from plugin noop
2026.04.29-00:55:09.96 - <debug> Registered op image_detect from plugin noop
2026.04.29-00:55:09.96 - <debug> Registered op image_segment from plugin noop
2026.04.29-00:55:09.96 - <debug> Registered op image_pose from plugin noop
2026.04.29-00:55:09.96 - <debug> Registered op image_depth from plugin noop
2026.04.29-00:55:09.96 - <debug> Registered op tf_model_load from plugin noop
2026.04.29-00:55:09.96 - <debug> Registered op tf_model_unload from plugin noop
2026.04.29-00:55:09.96 - <debug> Registered op tf_model_run from plugin noop
2026.04.29-00:55:09.96 - <debug> Registered op tflite_model_load from plugin noop
2026.04.29-00:55:09.96 - <debug> Registered op tflite_model_unload from plugin noop
2026.04.29-00:55:09.96 - <debug> Registered op tflite_model_run from plugin noop
2026.04.29-00:55:09.96 - <debug> Registered op torch_model_load from plugin noop
2026.04.29-00:55:09.96 - <debug> Registered op torch_model_run from plugin noop
2026.04.29-00:55:09.96 - <debug> Registered op torch_sgemm from plugin noop
2026.04.29-00:55:09.96 - <debug> Registered op blas_sgemm from plugin noop
2026.04.29-00:55:09.96 - <debug> Registered op fpga_arraycopy from plugin noop
2026.04.29-00:55:09.96 - <debug> Registered op fpga_vectoradd from plugin noop
2026.04.29-00:55:09.96 - <debug> Registered op fpga_parallel from plugin noop
2026.04.29-00:55:09.96 - <debug> Registered op fpga_mmult from plugin noop
2026.04.29-00:55:09.96 - <debug> Registered op minmax from plugin noop
2026.04.29-00:55:09.96 - <debug> Registered op opencv from plugin noop
2026.04.29-00:55:09.96 - <debug> Loaded plugin noop from libvaccel-noop.so
2026.04.29-00:55:09.96 - <debug> New rundir for session 1: /run/user/0/vaccel/b1vi3E/session.1
2026.04.29-00:55:09.96 - <debug> Initialized session 1 with plugin noop
Initialized session with id: 1
2026.04.29-00:55:09.96 - <debug> session:1 Looking for func implementing op image_classify
2026.04.29-00:55:09.96 - <debug> Returning func for op image_classify from plugin noop
2026.04.29-00:55:09.96 - <debug> [noop] Calling Image classification for session 1
2026.04.29-00:55:09.96 - <debug> [noop] Dumping arguments for Image classification:
2026.04.29-00:55:09.96 - <debug> [noop] model: (null)
2026.04.29-00:55:09.96 - <debug> [noop] len_img: 79281
2026.04.29-00:55:09.96 - <debug> [noop] len_out_text: 512
2026.04.29-00:55:09.96 - <debug> [noop] len_out_imgname: 512
2026.04.29-00:55:09.96 - <debug> [noop] will return a dummy result
2026.04.29-00:55:09.96 - <debug> [noop] will return a dummy result
classification tags: This is a dummy classification tag!
classification imagename: This is a dummy imgname!
2026.04.29-00:55:09.96 - <debug> Released session 1
2026.04.29-00:55:09.96 - <debug> Cleaning up vAccel
2026.04.29-00:55:09.96 - <debug> Cleaning up sessions
2026.04.29-00:55:09.96 - <debug> Cleaning up resources
2026.04.29-00:55:09.96 - <debug> Cleaning up plugins
2026.04.29-00:55:09.96 - <debug> Unregistered plugin noop
```
