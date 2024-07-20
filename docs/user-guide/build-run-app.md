# Build and run a vAccel application

Assuming we have an installation of vAccel, either by [building from
source](building.md) or by installing the [binary packages](binaries.md), we
will walk through the process of running a simple vAccel application

## Building a vaccel application

We will use an example of image classification which can be found under the
[examples](https://github.com/nubificus/vaccel/tree/main/examples) folder of this project.

If you haven't already done so, get the code and change to the cloned directory:
```bash
git clone https://github.com/nubificus/vaccel
cd vaccel
```

You can then build the example using:
```bash
meson setup -Dexamples=enabled build
meson compile -C build
```

A number of example binaries have been built:
```console
$ ls build/examples
classify          detect          exec_generic     minmax          pose             pynq_parallel    segment_generic  tf_inference
classify_generic  depth           detect_generic   minmax_generic  pose_generic     pynq_vector_add  sgemm            tf_model
depth_generic     exec            Makefile         noop            pynq_array_copy  segment          sgemm_generic    tf_saved_model
```

Alternatively, to build the example manually you can use the provided pkg-config
specification - make sure vAccel is installed globally or set the
`PKG_CONFIG_PATH`environment variable.

```console
$ # install vaccel to build/install
$ meson setup --reconfigure --prefix=<absolute/path/to/>build/install build
$ meson install -C build
$ # set path to the pkgconfig dir (so pkg-config will find vaccel.pc)
$ export PKG_CONFIG_PATH=<absolute/path/to/>build/install/lib/<multirarch-triplet>/pkgconfig
$
$ cd examples
$ gcc classify.c -o classify -Wall -Wextra $(pkg-config --cflags --libs vaccel)
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
