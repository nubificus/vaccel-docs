# Quickstart

This is a quick start guide for running a simple vAccel application. 

- [Build from Source](#build-from-source) or [get the binary packages](#binary-packages) [currently only for Debian/Ubuntu variants]
- Run a [simple example](#simple-example) [using the `noop` plugin]
- Run a more [elaborate example](#jetson-example) [using the `jetson-inference` plugin]

<hr>
## Binary packages

We provide release debs of the vAccelRT library, along with an example, debug
plugin (`noop`), and a hardware plugin (`jetson-inference`).

### Get vAccelRT

You can install vAccelRT (in `/usr/local`) using the following commands:

```
wget https://s3.nbfc.io/nbfc-assets/github/vaccelrt/master/x86_64/Release-deb/vaccel-0.5.0-Linux.deb
sudo dpkg -i vaccel-0.5.0-Linux.deb
```

### Get the `jetson-inference` plugin

You can install the `jetson-inference` plugin using the following commands:

```
wget https://s3.nbfc.io/nbfc-assets/github/vaccelrt/plugins/jetson_inference/master/x86_64/vaccelrt-plugin-jetson-0.1-Linux.deb
dpkg -i vaccelrt-plugin-jetson-0.1-Linux.deb
```

You can now go ahead and run a [simple example](#simple-example) using the `noop` plugin.

<hr>

## Build from Source

### Prerequisites

In Ubuntu-based systems, you need to have the following packages to build `vaccelrt`:

- cmake
- build-essential

You can install them using the following command:

```bash
sudo apt-get install -y cmake build-essential
```


### Get the source code

Get the source code for **vaccelrt**:

```bash
git clone https://github.com/cloudkernels/vaccelrt --recursive
```

### Build and install vaccelrt

Build vaccelrt and install it in `/usr/local`:

```bash
cd vaccelrt
mkdir build
cd build
cmake ../ -DCMAKE_INSTALL_PREFIX=/usr/local -DBUILD_PLUGIN_NOOP=ON -DBUILD_EXAMPLES=ON -DCMAKE_BUILD_TYPE=Release
make
make install
```

<hr>

## Simple Example

Donwload an adorable kitten photo:

```bash
wget https://i.imgur.com/aSuOWgU.jpeg -O cat.jpeg
```


Try one of our examples, available at `/usr/local/bin/classify` or `/usr/local/bin/classify_generic`:

```bash
# set some env variables to specify where to find libvaccel.so
# and the backend plugin (noop)
export VACCEL_BACKENDS=/usr/local/lib/libvaccel-noop.so
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

# execute the operation
/usr/local/bin/classify_generic cat.jpeg 1
```

The output should be something like the following:

```
# /usr/local/bin/classify_generic cat.jpeg 1
Initialized session with id: 1
Image size: 54372B
[noop] Calling Image classification for session 1
[noop] Dumping arguments for Image classification:
[noop] len_img: 54372
[noop] will return a dummy result
classification tags: This is a dummy classification tag!
```












Building the Jetson inference plugin requires a working
[jetson-inference](https://github.com/dusty-nv/jetson-inference) installation
along with the corresponding CUDA environment on the machine. If you have it
you can just run:

```sh
./build.sh all
```

Note: while building the rootfs, this script will require your sudo password.

If a jetson-inference setup is not available you can either follow [this
guide](/jetson) to build the vAccel jetson plugin and install the prerequisites
on your host machine, or use our `nubificus/vaccel-deps` container image to
build the necessary components, by running:

```sh
./build.sh -c all
```

## Running the application

The above build process create two directories: `build` includes intermediate
files of the building process and `output` includes the build artifacts we will
need to run our example:

```sh
cd output/debug
ls
bin  include  lib  share
```

### Native execution

#### Running on the host

In case you have the jetson-inference framework installed on your host, we
simply can execute:

```sh
# export the library path
export LD_LIBRARY_PATH=$(pwd)/lib

# Tell vAccelRT to use the jetson plugin
export VACCEL_BACKENDS=./lib/libvaccel-jetson.so

# Tell the Jetson plugin where to find the pre-trained models
export VACCEL_IMAGENET_NETWORKS=./share/networks

# Run the image classification example
./bin/classify ./share/images/dog_0.jpg 1
```

You should some logging from the jetson-inference framework and in the end of
it you should get the classification tags of the image:

```
imagenet: 60.49805% class #249 (malamute, malemute, Alaskan malamute)
imagenet: attempting to save output image
imagenet: completed saving
imagenet: shutting down...
classification tags: 60.498% malamute, malemute, Alaskan malamute
```

**Note**: The first time your run a classification with a model jetson-inference
is performing some JIT steps to optimize the classification result, so you can
expect increased execution time. The output of this operation is cached for
subsequent executions.

#### Running in a Firecracker VM 

`build.sh` created for us a rootfs image and a vmlinux kernel for booting a
Firecracker VM. The rootfs has pre-installed the `vAccel` libraries, the example
application the images and models.

Additionally, it installed for us the following Firecracker configuration for
booting the VM.

In similar fashion as before, we launch the VM:

```sh
# export the library path
export LD_LIBRARY_PATH=$(pwd)/lib

# Tell vAccelRT to use the jetson plugin
export VACCEL_BACKENDS=./lib/libvaccel-jetson.so

# Tell the Jetson plugin where to find the pre-trained models
export VACCEL_IMAGENET_NETWORKS=./share/networks

# Launch the Firecracker VM
./bin/firecracker --api-sock fc.sock --config-file share/config_virtio_accel.json --seccomp-level 0
```

This will launch the Firecracker VM and it will result in a login prompt in the
VM, to which we can login using the `root` user without a password.

```sh
Ubuntu 20.04.1 LTS vaccel-guest.nubificus.co.uk ttyS0

vaccel-guest login: root
Welcome to Ubuntu 20.04.1 LTS (GNU/Linux 4.20.0 x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.
Last login: Fri Feb  5 17:32:12 UTC 2021 on ttyS0
root@vaccel-guest:~# 
```

Once, in the prompt of the guest we setup the environment and run the example:

```sh
# export the library path
export LD_LIBRARY_PATH=/opt/vaccel/lib

# Tell vAccelRT to use the VirtIO plugin
export VACCEL_BACKENDS=/opt/vaccel/lib/libvaccel-virtio.so

# Launch the Firecracker VM
/opt/vaccel/bin/classify images/dog_0.jpg 1
```

**Note**: In this case, we use the VirtIO plugin since we are inside the VM
and we do not need to define the path to the pre-trained model. The latter is
necessary only on the host where we use the jetson plugin.

The result of the classification should be the same as before:

```sh
imagenet: 60.49805% class #249 (malamute, malemute, Alaskan malamute)
imagenet: attempting to save output image
imagenet: completed saving
imagenet: shutting down...
classification tags: 60.498% malamute, malemute, Alaskan malamute
```

### Docker execution

If you don't have a Jetson-inference installation available on your machine, you
can use our `nubificus/vaccel-deps` Docker image to run a vAccel application.

You need to install the Nvidia container runtime following the instructions
[here](https://github.com/NVIDIA/nvidia-container-runtime), which allows you
to use NVIDIA GPU devices inside Docker containers.

Once, you're all setup with the nvidia runtime you can run the application:

```sh
docker run --runtime=nvidia --rm --gpus all -v $(pwd):$(pwd) -w $(pwd) \
  -e LD_LIBRARY_PATH=$(pwd)/lib \
  -e VACCEL_BACKENDS=./lib/libvaccel-jetson.so \
  -e VACCEL_IMAGENET_NETWORKS=$(pwd)/share/networks \
  nubificus/vaccel-deps:latest \
  ./bin/classify share/images/dog_0.jpg 1 
```

Similarly, we can launch a Firecracker VM inside the container. In this case,
we need to add the `--privileged` flag to allow launching VMs inside the
container and `-it` to be able to use the VM's console.

```sh
docker run --runtime=nvidia --rm --gpus all -v $(pwd):$(pwd) -w $(pwd) \
  --privileged \
  -it \
  -e LD_LIBRARY_PATH=$(pwd)/lib \
  -e VACCEL_BACKENDS=./lib/libvaccel-jetson.so \
  -e VACCEL_IMAGENET_NETWORKS=$(pwd)/share/networks \
  nubificus/vaccel-deps:latest \
  ./bin/firecracker --api-sock fc.sock --config-file ./share/config_virtio_accel.json --seccomp-level 0
```

which we'll give us a console inside the VM, from which we can run our application
the same way as we did before:

```sh
# export the library path
export LD_LIBRARY_PATH=/opt/vaccel/lib

# Tell vAccelRT to use the VirtIO plugin
export VACCEL_BACKENDS=/opt/vaccel/lib/libvaccel-virtio.so

# Launch the Firecracker VM
/opt/vaccel/bin/classify images/dog_0.jpg 1
```

