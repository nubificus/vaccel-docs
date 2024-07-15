# Build & install from source

To build the components of vAccel we need the vAccel core library and a
backend plugin that implements the operation we want to execute.

## Build vAccelRT

[This](https://github.com/cloudkernels/vaccel) repo includes the core runtime
system, the `exec` backend plugin and a debug plugin for testing (`noop`).

### 1. Cloning and preparing the build directory

In Ubuntu-based systems, you need to have the following packages to build `vaccel`:

- cmake
- build-essential
- meson
- ninja

You can install them using the following command:

```bash
apt-get install build-essential ninja-build pkg-config python3-pip 
pip install meson
```

Get the source code for **vaccelrt**:

```bash
git clone https://github.com/cloudkernels/vaccel --recursive
```

### 2. Building and isntalling the core runtime library

```bash
cd vaccel

# Configure the build directory with the default options and set build
# type to 'release'.
meson setup --buildtype=release build

# Compile the project
meson compile -C build

# Install the project
meson install -C build
```

### 3. Building the plugins

Building the plugins is disabled, by default. You can enable building one or
more plugins at configuration time of meson by replacing ```meson setup --buildtype=release build``` with the plugin alternative

For example:

```bash
meson setup --buildtype=release -Dplugin-noop=enabled build
```

will enable building the noop backend plugin.

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
