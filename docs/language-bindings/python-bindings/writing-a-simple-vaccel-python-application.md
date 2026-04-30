# Writing a simple vAccel Python application

For a simple example of using the `vaccel` package, you can replicate in Python
the image classification example from
[Running the examples](../../getting-started/running-the-examples.md).

Create a new Python file called `classify.py` with the following content:

```python title="classify.py"
#!/usr/bin/python3

import sys
from pathlib import Path

from vaccel.session import Session


def main():
    with Path(sys.argv[1]).open("rb") as f:
        image = f.read()

    sess = Session()
    print(f"Session id is {sess.id}")
    res = sess.classify(image)
    print(res)


if __name__ == "__main__":
    main()
```

As with the original `classify` example, to execute `classify.py` you need to
configure vAccel:

```sh
export VACCEL_PLUGINS=libvaccel-noop.so
```

Assuming vAccel in installed at `/usr/local`, running the Python classification
should give you:

```console
$ python3 classify.py /usr/local/share/vaccel/images/example.jpg
Session id is 1
('This is a dummy classification tag!', 'This is a dummy imgname!')
```

By adding debug level logging:

```sh
export VACCEL_LOG_LEVEL=4
```

you can get the verbose version of the output:

```console
$ python3 classify.py /usr/local/share/vaccel/images/example.jpg
2026.04.29-15:07:13.91 - <debug> Initializing vAccel
2026.04.29-15:07:13.91 - <info> vAccel 0.7.1-93-ebc23b1f
2026.04.29-15:07:13.91 - <debug> Config:
2026.04.29-15:07:13.91 - <debug>   plugins = libvaccel-noop.so
2026.04.29-15:07:13.91 - <debug>   log_level = debug
2026.04.29-15:07:13.91 - <debug>   log_file = (null)
2026.04.29-15:07:13.91 - <debug>   profiling_enabled = false
2026.04.29-15:07:13.91 - <debug>   version_ignore = false
2026.04.29-15:07:13.91 - <debug> Created top-level rundir: /run/user/0/vaccel/SlmFzq
2026.04.29-15:07:13.91 - <info> Registered plugin noop 0.7.1-93-ebc23b1f
2026.04.29-15:07:13.91 - <debug> Registered op noop from plugin noop
2026.04.29-15:07:13.91 - <debug> Registered op exec from plugin noop
2026.04.29-15:07:13.91 - <debug> Registered op exec_with_resource from plugin noop
2026.04.29-15:07:13.91 - <debug> Registered op image_classify from plugin noop
2026.04.29-15:07:13.91 - <debug> Registered op image_detect from plugin noop
2026.04.29-15:07:13.91 - <debug> Registered op image_segment from plugin noop
2026.04.29-15:07:13.91 - <debug> Registered op image_pose from plugin noop
2026.04.29-15:07:13.91 - <debug> Registered op image_depth from plugin noop
2026.04.29-15:07:13.91 - <debug> Registered op tf_model_load from plugin noop
2026.04.29-15:07:13.91 - <debug> Registered op tf_model_unload from plugin noop
2026.04.29-15:07:13.91 - <debug> Registered op tf_model_run from plugin noop
2026.04.29-15:07:13.91 - <debug> Registered op tflite_model_load from plugin noop
2026.04.29-15:07:13.91 - <debug> Registered op tflite_model_unload from plugin noop
2026.04.29-15:07:13.91 - <debug> Registered op tflite_model_run from plugin noop
2026.04.29-15:07:13.91 - <debug> Registered op torch_model_load from plugin noop
2026.04.29-15:07:13.91 - <debug> Registered op torch_model_run from plugin noop
2026.04.29-15:07:13.91 - <debug> Registered op torch_sgemm from plugin noop
2026.04.29-15:07:13.91 - <debug> Registered op blas_sgemm from plugin noop
2026.04.29-15:07:13.91 - <debug> Registered op fpga_arraycopy from plugin noop
2026.04.29-15:07:13.91 - <debug> Registered op fpga_vectoradd from plugin noop
2026.04.29-15:07:13.91 - <debug> Registered op fpga_parallel from plugin noop
2026.04.29-15:07:13.91 - <debug> Registered op fpga_mmult from plugin noop
2026.04.29-15:07:13.91 - <debug> Registered op minmax from plugin noop
2026.04.29-15:07:13.91 - <debug> Registered op opencv from plugin noop
2026.04.29-15:07:13.91 - <debug> Loaded plugin noop from libvaccel-noop.so
2026.04.29-15:07:13.91 - <debug> New rundir for session 1: /run/user/0/vaccel/SlmFzq/session.1
2026.04.29-15:07:13.91 - <debug> Initialized session 1 with plugin noop
2026.04.29-15:07:13.91 - <debug> session:1 Looking for func implementing op image_classify
2026.04.29-15:07:13.91 - <debug> Returning func for op image_classify from plugin noop
2026.04.29-15:07:13.91 - <debug> [noop] Calling Image classification for session 1
2026.04.29-15:07:13.91 - <debug> [noop] Dumping arguments for Image classification:
2026.04.29-15:07:13.91 - <debug> [noop] model: (null)
2026.04.29-15:07:13.91 - <debug> [noop] len_img: 79281
2026.04.29-15:07:13.91 - <debug> [noop] len_out_text: 512
2026.04.29-15:07:13.91 - <debug> [noop] len_out_imgname: 512
2026.04.29-15:07:13.91 - <debug> [noop] will return a dummy result
2026.04.29-15:07:13.91 - <debug> [noop] will return a dummy result
2026.04.29-15:07:13.91 - <debug> Released session 1
Session id is 1
('This is a dummy classification tag!', 'This is a dummy imgname!')
2026.04.29-15:07:13.91 - <debug> Cleaning up vAccel
2026.04.29-15:07:13.91 - <debug> Cleaning up sessions
2026.04.29-15:07:13.91 - <debug> Cleaning up resources
2026.04.29-15:07:13.91 - <debug> Cleaning up plugins
2026.04.29-15:07:13.91 - <debug> Unregistered plugin noop
```

The vAccel output of
[`classify`](../../getting-started/running-the-examples.md#classify-noop-debug)
and `classify.py` should be almost identical.

<!-- markdownlint-disable code-block-style -->

!!! info

    For a full example with near identical functionality to the C `classify` you can
    look at the
    [image classification example](https://github.com/nubificus/vaccel-python/blob/main/examples/classify.py)
    of the `vaccel-python` repository,

<!-- markdownlint-restore -->
