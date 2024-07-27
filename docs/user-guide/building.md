# Build & Install from source

To build the components of vAccel we need the vAccel core library and a
backend plugin that implements the operation we want to execute.

## Build vAccel

[This](https://github.com/nubificus/vaccel) repo includes the core runtime
system, the `exec` backend plugin and a debug plugin for testing (`noop`).

### 1. Cloning and preparing the build directory

In Ubuntu-based systems, you need to have the following packages to build `vaccel`:

- build-essential
- ninja-build
- pkg-config
- meson

You can install them using the following command:

```bash
apt-get install build-essential ninja-build pkg-config python3-pip 
pip install meson
```

Get the source code for **vaccel**:

```bash
git clone https://github.com/nubificus/vaccel --recursive
```

### 2. Building and installing the core runtime library

```bash
cd vaccel

# Configure the build directory with the default options and set build
# type to 'release'.
meson setup --buildtype=release build

# Compile the project
meson compile -C build

# Install the project to default directory (/usr/local)
meson install -C build
```

### 3. Building the plugins

Building the plugins is disabled, by default. You can enable building one or
more plugins at configuration time by setting the corresponding options.

For example, replacing:
```bash
meson setup --buildtype=release build
```

with:
```bash
meson setup --buildtype=release -Dplugin-noop=enabled build
```

in the previous code snippet, will build and install both the core library and
the noop backend plugin.

You can also configure a plugin after the initial configuration of your build
directory by using:
```bash
meson setup --reconfigure -Dplugin-noop=enabled build
```

To view all available plugins and options/values you an run:
```bash
meson setup --buildtype=release build
meson configure build
```

vAccel specific options can be found in the `Project Options` section.

## Building a vAccel application

We will use an example of image classification which can be found under the
[examples](https://github.com/nubificus/vaccel/tree/main/examples) folder of this project.

You can build the example using:
```bash
meson setup --reconfigure -Dexamples=enabled build
meson compile -C build
```

A number of example binaries have been built:
```console
$ ls examples
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

## Running a vAccel application

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
