# Running the examples

vAccel comes with a set of examples for common acceleration operations like
image classification, matrix multiplication etc. Besides providing common
acceleration functionality, the examples are meant as a demonstration of how to
use the different operations of the [vAccel API](../api/index.md).

The bare minimum you have to configure in order to run the examples - or any
vAccel application - is the backend plugin that will be used. You can do this by
setting the `VACCEL_PLUGINS` environment variable:

```sh
export VACCEL_PLUGINS=libvaccel-noop.so
```

This will select the `NoOp` dummy plugin as a backend.

You are now ready to run any example.

For example, assuming vAccel is installed in `/usr/local`, you can run an image
classification operation with:

```console
$ classify /usr/local/share/vaccel/images/example.jpg 1
Initialized session with id: 1
classification tags: This is a dummy classification tag!
classification imagename: This is a dummy imgname!
```

By enabling debug level logging, you can get more details on what is happening
in the background:

```sh
export VACCEL_LOG_LEVEL=4
```

The output will now be:

<!-- markdownlint-disable no-empty-links -->

[](){#classify-noop-debug}

<!-- markdownlint-restore -->

```console
$ classify /usr/local/share/vaccel/images/example.jpg 1
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

You can find sample invocation commands for all the examples in the
[run-examples](https://github.com/nubificus/vaccel/blob/main/scripts/run-examples.sh)
script. You can also clone the repo and run the script yourself with:

```sh
git clone https://github.com/nubificus/vaccel
cd vaccel
# Replace '/usr/local' with the vAccel installation prefix
./scripts/run-examples.sh /usr/local
```

If you have already built vAccel from source, simply run:

```sh
# Replace 'build' with your build directory
ninja run-examples -C build
```

in your `vaccel` directory.

<!-- markdownlint-disable code-block-style -->

!!! info

    You can find more information on the environment variables you can use to
    configure vAccel in the [Configuration](../configuration.md) page.

<!-- markdownlint-restore -->
