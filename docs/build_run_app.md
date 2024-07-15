# Build and run a vAccel application

Assuming we have an installation of vAccel, either by [building from
source](building.md) or by installing the [binary packages](binaries.md), we
will walk through the process of running a simple vAccel application

## Building a vaccel application

We will use an example of image classification which can be found under the
[examples](https://github.com/cloudkernels/vaccel/tree/master/examples) folder of this project.

You can build the example using the following reconfiguration in the meson build:

```bash
meson setup --reconfigure -Dexamples=enabled build
```

A number of example binaries have been built:
```console
# ls examples
classify          detect          exec_generic     minmax          pose             pynq_parallel    segment_generic  tf_inference
classify_generic  depth           detect_generic   minmax_generic  pose_generic     pynq_vector_add  sgemm            tf_model
depth_generic     exec            Makefile         noop            pynq_array_copy  segment          sgemm_generic    tf_saved_model
```

If, instead, you want to build by hand you need to define the include and
library paths (if they are not in your respective default search paths) and
also link with `dl`:

```console
$ cd ../examples
$ gcc -Wall -Wextra -I/usr/local/include -L/usr/local/lib classify.c -o classify -lvaccel -ldl
$ ls classify.c classify
classify.c  classify  
```

## Running a vaccel application

Having built our `classify` example, we need to prepare the vaccel environment for it to run:

1. Define the path to `libvaccel.so` (if not in the default search path):

```bash
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
```

2. Define the backend plugin to use for our application.

In this example, we will use the noop plugin:

```bash
export VACCEL_BACKENDS=/usr/local/lib/libvaccel-noop.so
```

3. Finally, you can do:

```bash
./classify images/example.jpg 1
```

which should dump the following output:

```console
$ ./classify images/example.jpg 1
Initialized session with id: 1
Image size: 79281B
[noop] Calling Image classification for session 1
[noop] Dumping arguments for Image classification:
[noop] len_img: 79281
[noop] will return a dummy result
classification tags: This is a dummy classification tag!
```
Alternatively from the build directory:

```console
$ cd ../build
$ ./examples/classify ../examples/images/example.jpg 1
Initialized session with id: 1
Image size: 79281B
[noop] Calling Image classification for session 1
[noop] Dumping arguments for Image classification:
[noop] len_img: 79281
[noop] will return a dummy result
classification tags: This is a dummy classification tag!
```

For debug level output:
```
export VACCEL_DEBUG_LEVEL=4
```
