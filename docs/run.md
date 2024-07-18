# Running a simple example

## Building a vaccel application

We will use an example of image classification which can be found under the
[examples](https://github.com/cloudkernels/vaccel/tree/master/examples) folder
of the vAccel runtime [repo](https://github.com/cloudkernels/vaccel).

You can build the example using the Meson/CMake of the repo:

Using Meson:

```bash
meson setup --reconfigure -Dexamples=enabled build
meson compile -C build
meson install -C build
```

Alternatively, we can also use CMake to build our exmaples:

```bash
mkdir build
cd build
cmake -DBUILD_EXAMPLES=ON ..
make
ls examples
classify  CMakeFiles  cmake_install.cmake  Makefile
```

If, instead, you want to build by hand you need to define the include and library paths (if they are not
in your respective default search paths) and also link with `dl`:

```
cd ../examples
gcc -Wall -Wextra -I${HOME}/.local/include -L${HOME}/.local/lib classification.c -o classify -lvaccel -ldl
ls
classification.c  classify  CMakeLists.txt  images
```

## Running the example

Having built our `classify` example, we need to prepare the vaccel environment for it to run:

1. Define the path to `libvaccel.so` (if not in the default search path):

```bash
export LD_LIBRARY_PATH=${HOME}/.local/lib
```

2. Define the backend plugin to use for our application.

In this example, we will use the jetson plugin which implements the image classification operation using the Jetson Inference
framework which uses TensorRT.

```bash
export VACCEL_BACKENDS=${HOME}/.local/lib/libvaccel-jetson.so
```

Finally, the classification application needs the imagent models in the current working path.
(TODO: Find link to download those). Once you have these, you can do:

```bash
ls 
classify  images  networks

VACCEL_IMAGENET_NETWORKS=$(pwd) ./classify images/banana_0.jpg 1
Initialized session with id: 1
Image size: 79281B
classification tags: 99.902% banana
```
