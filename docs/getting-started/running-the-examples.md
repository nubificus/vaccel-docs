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
2026.04.29-14:47:59.38 - <debug> Initializing vAccel
2026.04.29-14:47:59.38 - <info> vAccel 0.7.1-93-ebc23b1f
2026.04.29-14:47:59.38 - <debug> Config:
2026.04.29-14:47:59.38 - <debug>   plugins = libvaccel-noop.so
2026.04.29-14:47:59.38 - <debug>   log_level = debug
2026.04.29-14:47:59.38 - <debug>   log_file = (null)
2026.04.29-14:47:59.38 - <debug>   profiling_enabled = false
2026.04.29-14:47:59.38 - <debug>   version_ignore = false
2026.04.29-14:47:59.38 - <debug> Created top-level rundir: /run/user/0/vaccel/fPAGh6
2026.04.29-14:47:59.38 - <info> Registered plugin noop 0.7.1-93-ebc23b1f
2026.04.29-14:47:59.38 - <debug> Registered op noop from plugin noop
2026.04.29-14:47:59.38 - <debug> Registered op exec from plugin noop
2026.04.29-14:47:59.38 - <debug> Registered op exec_with_resource from plugin noop
2026.04.29-14:47:59.38 - <debug> Registered op image_classify from plugin noop
2026.04.29-14:47:59.38 - <debug> Registered op image_detect from plugin noop
2026.04.29-14:47:59.38 - <debug> Registered op image_segment from plugin noop
2026.04.29-14:47:59.38 - <debug> Registered op image_pose from plugin noop
2026.04.29-14:47:59.38 - <debug> Registered op image_depth from plugin noop
2026.04.29-14:47:59.38 - <debug> Registered op tf_model_load from plugin noop
2026.04.29-14:47:59.38 - <debug> Registered op tf_model_unload from plugin noop
2026.04.29-14:47:59.38 - <debug> Registered op tf_model_run from plugin noop
2026.04.29-14:47:59.38 - <debug> Registered op tflite_model_load from plugin noop
2026.04.29-14:47:59.38 - <debug> Registered op tflite_model_unload from plugin noop
2026.04.29-14:47:59.38 - <debug> Registered op tflite_model_run from plugin noop
2026.04.29-14:47:59.38 - <debug> Registered op torch_model_load from plugin noop
2026.04.29-14:47:59.38 - <debug> Registered op torch_model_run from plugin noop
2026.04.29-14:47:59.38 - <debug> Registered op torch_sgemm from plugin noop
2026.04.29-14:47:59.38 - <debug> Registered op blas_sgemm from plugin noop
2026.04.29-14:47:59.38 - <debug> Registered op fpga_arraycopy from plugin noop
2026.04.29-14:47:59.38 - <debug> Registered op fpga_vectoradd from plugin noop
2026.04.29-14:47:59.38 - <debug> Registered op fpga_parallel from plugin noop
2026.04.29-14:47:59.38 - <debug> Registered op fpga_mmult from plugin noop
2026.04.29-14:47:59.38 - <debug> Registered op minmax from plugin noop
2026.04.29-14:47:59.38 - <debug> Registered op opencv from plugin noop
2026.04.29-14:47:59.38 - <debug> Loaded plugin noop from libvaccel-noop.so
2026.04.29-14:47:59.38 - <debug> New rundir for session 1: /run/user/0/vaccel/fPAGh6/session.1
2026.04.29-14:47:59.38 - <debug> Initialized session 1 with plugin noop
Initialized session with id: 1
2026.04.29-14:47:59.38 - <debug> session:1 Looking for func implementing op image_classify
2026.04.29-14:47:59.38 - <debug> Returning func for op image_classify from plugin noop
2026.04.29-14:47:59.38 - <debug> [noop] Calling Image classification for session 1
2026.04.29-14:47:59.38 - <debug> [noop] Dumping arguments for Image classification:
2026.04.29-14:47:59.38 - <debug> [noop] model: (null)
2026.04.29-14:47:59.38 - <debug> [noop] len_img: 79281
2026.04.29-14:47:59.38 - <debug> [noop] len_out_text: 512
2026.04.29-14:47:59.38 - <debug> [noop] len_out_imgname: 512
2026.04.29-14:47:59.38 - <debug> [noop] will return a dummy result
2026.04.29-14:47:59.38 - <debug> [noop] will return a dummy result
classification tags: This is a dummy classification tag!
classification imagename: This is a dummy imgname!
2026.04.29-14:47:59.38 - <debug> Released session 1
2026.04.29-14:47:59.38 - <debug> Cleaning up vAccel
2026.04.29-14:47:59.38 - <debug> Cleaning up sessions
2026.04.29-14:47:59.38 - <debug> Cleaning up resources
2026.04.29-14:47:59.38 - <debug> Cleaning up plugins
2026.04.29-14:47:59.38 - <debug> Unregistered plugin noop
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
