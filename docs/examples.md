
## vAccel on Google Coral Edge TPU

Running compute-intensive workloads on low-power/Edge devices is a challenging
task, especially when multiple factors are being considered, such as security,
isolation, performance etc.

To this end, one of our initial goals in developing the vAccel framework is to
facilitate the acceleration of ML inference operations when executing on
low-power devices such as an NVIDIA Jetson Nano. Below we walk through the
process of running a simple image classification operation from an Amazon
Firecracker VM, using the Maxwell GPU present in the Jetson compute module.

### Building a vaccel application

We will use an example of image classification which can be found under the
[examples](https://github.com/cloudkernels/vaccelrt/tree/master/examples) folder
of the vAccel runtime [repo](https://github.com/cloudkernels/vaccelrt).

You can build the example using the CMake of the repo:
```bash
$ mkdir build
$ cd build
$ cmake -DBUILD_EXAMPLES=ON ..
$ make
$ ls examples
classify  CMakeFiles  cmake_install.cmake  Makefile
```

If, instead, you want to build by hand you need to define the include and library paths (if they are not
in your respective default search paths) and also link with `dl`:

```
$ cd ../examples
$ gcc -Wall -Wextra -I${HOME}/.local/include -L${HOME}/.local/lib classification.c -o classify -lvaccel -ldl
$ ls
classification.c  classify  CMakeLists.txt  images
```

### Running the example

Having built our `classify` example, we need to prepare the vaccel environment for it to run:

1. Define the path to `libvaccel.so` (if not in the default search path):

```bash
export LD_LIBRARY_PATH=${HOME}/.local/lib
```

2. Define the backend plugin to use for our application.

In this example, we will use the Google Coral plugin which implements the image
classification operation using libedgetpu and tflite. You can get more info on
building this plugin in the [relevant section](/coral) of the currect
documentation.

```bash
export VACCEL_BACKENDS=${HOME}/.local/lib/libvaccel-coral.so
```

Finally, the classification application needs the mobilenet model file & labels in the current working path.

```
wget https://github.com/google-coral/test_data/raw/c21de4450f88a20ac5968628d375787745932a5a/mobilenet_v1_1.0_224_quant_edgetpu.tflite
wget https://raw.githubusercontent.com/google-coral/test_data/c21de4450f88a20ac5968628d375787745932a5a/imagenet_labels.txt
```

```bash
$ ls 
classify resized_cat.bmp mobilenet_v1_1.0_224_quant_edgetpu.tflite imagenet_labels.txt 
$ ./classify resized_cat.bmp 1
Initialized session with id: 1
Image size: 150666B
classification tags:  286  Egyptian cat
```

### Running the same example on an AWS Firecracker VM

As mentioned, with vAccel we are able to use the [virtio-accel](/virtio)
backend while in a VM, to forward specific acceleration operations to the Host
OS which, in turn, will execute them on real hardware. Below, we summarize the
process to use the Google Coral Edge TPU image classification hardware
acceleration functionality from a Firecracker VM.

First, we need to have a basic set of binaries to boot a VM and use the
virtio-accel backend of vAccelRT. In short, the process to follow is given
below:

#### Prepare the system to boot a Firecracker VM

##### Build Firecracker

To build the vAccel Firecracker port, we do the following on our aarch64 host:

```
git clone https://github.com/cloudkernels/firecracker -b vaccel-v0.23
cd firecracker/tools/devctr
docker build -t nubificus/fcuvm:v0.23 -f Dockerfile.aarch64
cd ../../
tools/devtool build --release -l gnu
```

That should output a binary at
`build/cargo_target/aarch64-unknown-linux-gnu/release/firecracker` relative to
the firecracker source tree.

##### Building the kernel & rootfs

To facilitate the process of building a kernel image and rootfs for vAccel, you
can follow the instructions on the [aarch64 tools
repo](https://github.com/nubificus/fc-aarch64-guest-build):

```
git clone https://github.com/nubificus/fc-aarch64-guest-build
cd fc-aarch64-guest-build
bash build.sh
```

If all went well, there should be an output folder with the following files:

```
# ls output
Image
rootfs.img
config_vaccel.json
```

##### Boot the Firecracker VM

Then, using the binaries from the previous steps we spawn a Firecracker VM:

```
export LD_LIBRARY_PATH=${HOME}/.local/lib
export VACCEL_BACKENDS=${HOME}/.local/lib/libvaccel-coral.so
firecracker --api-sock /tmp/fc.sock --config-file config_vaccel.json --seccomp-level 0
```

The output of the above command should be something like the following:
```
./firecracker --api-sock /tmp/fc.sock --config-file config_vaccel.json --seccomp-level 0
[    0.000000] Booting Linux on physical CPU 0x0000000000 [0x410fd034]
[    0.000000] Linux version 4.20.0 (root@buildkitsandbox) (gcc version 8.3.0 (Debian 8.3.0-6)) #1 SMP Thu Dec 3 23:58:32 UTC 2020
[    0.000000] Machine model: linux,dummy-virt
[    0.000000] earlycon: uart0 at MMIO 0x0000000040003000 (options '')
[    0.000000] printk: bootconsole [uart0] enabled
[    0.000000] efi: Getting EFI parameters from FDT:
[    0.000000] efi: UEFI not found.
[    0.000000] NUMA: No NUMA configuration found
[    0.000000] NUMA: Faking a node at [mem 0x0000000080000000-0x000000008fffffff]
[    0.000000] NUMA: NODE_DATA [mem 0x8fedbf00-0x8fef4fff]
[    0.000000] Zone ranges:
[    0.000000]   DMA32    [mem 0x0000000080000000-0x000000008fffffff]
[    0.000000]   Normal   empty
[    0.000000] Movable zone start for each node
[    0.000000] Early memory node ranges
[    0.000000]   node   0: [mem 0x0000000080000000-0x000000008fffffff]
[    0.000000] Initmem setup node 0 [mem 0x0000000080000000-0x000000008fffffff]
[snipped]
[  OK  ] Reached target Multi-User System.
[  OK  ] Reached target Graphical Interface.
         Starting Update UTMP about System Runlevel Changes...
[  OK  ] Finished Update UTMP about System Runlevel Changes.

Ubuntu 20.04.1 LTS localhost.localdomain ttyS0

localhost login: 
```

##### Perform the operation

Go ahead and login as root and execute the classification command:

```
localhost login: root
Welcome to Ubuntu 20.04.1 LTS (GNU/Linux 4.20.0 aarch64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.
Last login: Sat Feb  6 10:00:59 UTC 2021 on ttyS0
root@localhost:~# ./classify resized_cat.bmp 1
Initialized session with id: 1
Image size: 150666B
classification tags:  286  Egyptian cat
root@localhost:~# 
```

There you go! Using the Google Coral Edge TPU hardware from a Firecracker VM we
were able to perform ML inference!
