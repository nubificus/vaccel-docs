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

- [TensorFlow session load](../../../api/api-reference/operations.md#tensorflow-session-load)
- [TensorFlow session run](../../../api/api-reference/operations.md#tensorflow-session-run)
- [TensorFlow session delete](../../../api/api-reference/operations.md#tensorflow-session-delete)
- [TensorFlow Lite session load](../../../api/api-reference/operations.md#tensorflow-lite-session-load)
- [TensorFlow Lite session run](../../../api/api-reference/operations.md#tensorflow-lite-session-run)
- [TensorFlow Lite session delete](../../../api/api-reference/operations.md#tensorflow-lite-session-delete)

- [JIT loading and forwarding](../../../api/api-reference/operations.md#jit-loading-and-forwarding)
- [Matrix-to-matrix multiplication](../../../api/api-reference/operations.md#matrix-to-matrix-multiplication_1)

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
$ classify /usr/local/share/vaccel/images/example.jpg
2025.04.03-15:44:04.61 - <debug> Initializing vAccel
2025.04.03-15:44:04.61 - <info> vAccel 0.6.1-194-19056528
2025.04.03-15:44:04.61 - <debug> Config:
2025.04.03-15:44:04.61 - <debug>   plugins = libvaccel-noop.so
2025.04.03-15:44:04.61 - <debug>   log_level = debug
2025.04.03-15:44:04.61 - <debug>   log_file = (null)
2025.04.03-15:44:04.61 - <debug>   profiling_enabled = false
2025.04.03-15:44:04.61 - <debug>   version_ignore = false
2025.04.03-15:44:04.61 - <debug> Created top-level rundir: /run/user/1002/vaccel/VC0Gxz
2025.04.03-15:44:04.61 - <info> Registered plugin noop 0.6.1-194-19056528
2025.04.03-15:44:04.61 - <debug> Registered op noop from plugin noop
2025.04.03-15:44:04.61 - <debug> Registered op blas_sgemm from plugin noop
2025.04.03-15:44:04.61 - <debug> Registered op image_classify from plugin noop
2025.04.03-15:44:04.61 - <debug> Registered op image_detect from plugin noop
2025.04.03-15:44:04.61 - <debug> Registered op image_segment from plugin noop
2025.04.03-15:44:04.61 - <debug> Registered op image_pose from plugin noop
2025.04.03-15:44:04.61 - <debug> Registered op image_depth from plugin noop
2025.04.03-15:44:04.61 - <debug> Registered op exec from plugin noop
2025.04.03-15:44:04.61 - <debug> Registered op tf_session_load from plugin noop
2025.04.03-15:44:04.61 - <debug> Registered op tf_session_run from plugin noop
2025.04.03-15:44:04.61 - <debug> Registered op tf_session_delete from plugin noop
2025.04.03-15:44:04.61 - <debug> Registered op minmax from plugin noop
2025.04.03-15:44:04.61 - <debug> Registered op fpga_arraycopy from plugin noop
2025.04.03-15:44:04.61 - <debug> Registered op fpga_vectoradd from plugin noop
2025.04.03-15:44:04.61 - <debug> Registered op fpga_parallel from plugin noop
2025.04.03-15:44:04.61 - <debug> Registered op fpga_mmult from plugin noop
2025.04.03-15:44:04.61 - <debug> Registered op exec_with_resource from plugin noop
2025.04.03-15:44:04.61 - <debug> Registered op torch_jitload_forward from plugin noop
2025.04.03-15:44:04.61 - <debug> Registered op torch_sgemm from plugin noop
2025.04.03-15:44:04.61 - <debug> Registered op opencv from plugin noop
2025.04.03-15:44:04.61 - <debug> Registered op tflite_session_load from plugin noop
2025.04.03-15:44:04.61 - <debug> Registered op tflite_session_run from plugin noop
2025.04.03-15:44:04.61 - <debug> Registered op tflite_session_delete from plugin noop
2025.04.03-15:44:04.61 - <debug> Loaded plugin noop from libvaccel-noop.so
2025.04.03-15:44:04.62 - <debug> New rundir for session 1: /run/user/1002/vaccel/VC0Gxz/session.1
2025.04.03-15:44:04.62 - <debug> Initialized session 1
Initialized session with id: 1
2025.04.03-15:44:04.62 - <debug> session:1 Looking for plugin implementing VACCEL_OP_IMAGE_CLASSIFY
2025.04.03-15:44:04.62 - <debug> Returning func from hint plugin noop
2025.04.03-15:44:04.62 - <debug> Found implementation in noop plugin
2025.04.03-15:44:04.62 - <debug> [noop] Calling Image classification for session 1
2025.04.03-15:44:04.62 - <debug> [noop] Dumping arguments for Image classification:
2025.04.03-15:44:04.62 - <debug> [noop] model: (null)
2025.04.03-15:44:04.62 - <debug> [noop] len_img: 79281
2025.04.03-15:44:04.62 - <debug> [noop] len_out_text: 512
2025.04.03-15:44:04.62 - <debug> [noop] len_out_imgname: 512
2025.04.03-15:44:04.62 - <debug> [noop] will return a dummy result
2025.04.03-15:44:04.62 - <debug> [noop] will return a dummy result
classification tags: This is a dummy classification tag!
classification imagename: This is a dummy imgname!
2025.04.03-15:44:04.62 - <debug> Released session 1
2025.04.03-15:44:04.62 - <debug> Cleaning up vAccel
2025.04.03-15:44:04.62 - <debug> Cleaning up sessions
2025.04.03-15:44:04.62 - <debug> Cleaning up resources
2025.04.03-15:44:04.62 - <debug> Cleaning up plugins
2025.04.03-15:44:04.62 - <debug> Unregistered plugin noop
```
