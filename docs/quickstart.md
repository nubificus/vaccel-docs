# Quickstart

This is a quick start guide for running a simple vAccel application on a x86
machine with an Nvidia GPU. We will build the vAccel stack and run a simple
application both directly on a Linux host and inside a Firecracker VM.

## Building the vAccel stack

The [vAccel](https://github.com/cloudkernels/vaccel) is a meta repo which keeps
track of all the individual components needed for running a vAccel application.

```sh
git clone https://github.com/cloudkernels/vaccel
cd vaccel
```

The repo includes a build script which will build all the components:

1. The `vAccelRT` with the currently supported plugins
. The `virtio-accel` kernel module which acts as the transport layer when
running inside the Firecracker VM
1. The forked Firecracker VMM which is patched to handle virtio-accel requests
1. A rootfs and suitable vmlinux kernel image for booting the Firecracker VM
1. An example application for testing our setup

Building the Jetson inference plugin requires a working
[jetson-inference](https://github.com/dusty-nv/jetson-inference) installation
along with the corresponding CUDA environment on the machine. If you have it
you can just run:

```sh
./build.sh all
```

Note: while building the rootfs, this script will require your sudo password.

If a jetson-inference setup is not available you can use our `nubificus/vaccel-deps`
container image to build the necessary components, by running:

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
subsequent executions

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

