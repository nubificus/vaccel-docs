# Quickstart

This is a quick start guide for running a simple vAccel application.

- [Build from Source](#build-from-source) or
  [get the binary packages](#binary-packages) [currently only for Debian/Ubuntu
  variants]
- Run a [simple example](#simple-example) [using the `noop` plugin]
- Run the same example [in a VM](#vm-example) [same code in a VM]
- Run a more [elaborate example](#jetson-example) [same scenario, using the
  `jetson-inference` plugin]
- For the legacy version of instructions using CMake, follow [here](legacy.md)

<hr>

## Binary packages

We provide release debs of the vAccel library, along with an example, debug
plugin (`noop`), and a hardware plugin (`jetson-inference`).

### Get vAccel

You can install vAccel (in `/usr/local`) using the following commands:

```bash
wget https://s3.nbfc.io/nbfc-assets/github/vaccel/main/x86_64/release-deb/vaccel-0.6.0-Linux.deb
sudo dpkg -i vaccel-0.6.0-Linux.deb
```

### Get the `jetson-inference` plugin

You can install the `jetson-inference` plugin using the following commands:

```bash
wget https://s3.nbfc.io/nbfc-assets/github/vaccelrt/plugins/jetson_inference/master/x86_64/vaccelrt-plugin-jetson-0.1-Linux.deb
dpkg -i vaccelrt-plugin-jetson-0.1-Linux.deb
```

You can now go ahead and run a [simple example](#simple-example) using the
`noop` plugin.

<hr>

## Build from Source

### Prerequisites

In Ubuntu-based systems, you need to have the following packages to build
`vaccel`:

- build-essential
- meson
- ninja-build

You can install them using the following command:

```bash
apt-get install build-essential ninja-build pkg-config python3-pip
pip install meson
```

### Get the source code

Get the source code for **vaccel**:

```bash
git clone https://github.com/nubificus/vaccel --recursive
```

### Build and install vaccel

Build vaccel and install

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

<hr>

## Simple Example

Download an adorable kitten photo:

```bash
wget https://i.imgur.com/aSuOWgU.jpeg -O cat.jpeg
```

Try one of our examples, available at `/usr/local/bin/classify` or
`/usr/local/bin/classify_generic`:

```bash
# set some env variables to specify where to find libvaccel.so
# and the backend plugin (noop)
export VACCEL_BACKENDS=/usr/local/lib/libvaccel-noop.so
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

# execute the operation
/usr/local/bin/classify_generic cat.jpeg 1
```

The output should be something like the following:

```bash
# /usr/local/bin/classify_generic cat.jpeg 1
Initialized session with id: 1
Image size: 54372B
[noop] Calling Image classification for session 1
[noop] Dumping arguments for Image classification:
[noop] len_img: 54372
[noop] will return a dummy result
classification tags: This is a dummy classification tag!
```

## VM example

To run our code in a VM, we will have to use a virtual plugin that will handle
the forwarding of the function call from the VM to the Host system. That said,
we still need vAccel in the Host system to execute the forwarded call. A visual
representation of the execution flow is shown in Figure 1.

<figure>
  <img src="/img/vaccel-vm-flow.png" width="800" align=left
    alt="VM application execution flow" />
  <figcaption>Figure 1. VM application execution flow</figcaption>
</figure>

To enable this functionality, we will use the `VSOCK` plugin in the guest, and,
still, the `NOOP` plugin in the Host.

First, let's bootstrap the VM.

### VM setup

To bootstrap a simple VM we will use AWS firecracker and an example kernel &
rootfs. In [Run a vAccel application in a VM](user-guide/vm-example.md) we
provide more examples of the various hypervisors/VMMs we have tested and
support. You can get the binaries using the commands below:

```bash
wget https://s3.nbfc.io/nbfc-assets/github/vaccelrt/vm-example/x86_64/fc/firecracker
wget https://s3.nbfc.io/nbfc-assets/github/vaccelrt/vm-example/x86_64/fc/config.json
wget https://s3.nbfc.io/nbfc-assets/github/vaccelrt/vm-example/x86_64/fc/config_vsock.json
wget https://s3.nbfc.io/nbfc-assets/github/vaccelrt/vm-example/x86_64/rust-vmm/vmlinux
wget https://s3.nbfc.io/nbfc-assets/github/vaccelrt/vm-example/x86_64/rootfs.img
```

We should have the following files available:

```console
# tree .
.
├── config_vsock.json
├── firecracker
├── rootfs.img
└── vmlinux

0 directories, 4 files
```

To launch the VM, all we have to do is run the following command:

```bash
# make the firecracker binary executable
chmod +x firecracker

# launch the VM
./firecracker --api-sock fc.sock --config-file config_vsock.json
```

We should be presented with a login prompt:

```console
# ./firecracker --api-sock fc.sock --config-file config_vsock.json
[    0.000000] Linux version 5.10.0 (runner@gh-cloud-pod-t4rjg) (gcc (Ubuntu 8.4.0-3ubuntu2) 8.4.0, GNU ld (GNU Binutils for Ubuntu) 2.34) #1 SMP Tue Mar 22 20:07:37 UTC 2022
[    0.000000] Command line: console=ttyS0 reboot=k panic=1 pci=off loglevel=8 root=/dev/vda ip=172.42.0.2::172.42.0.1:255.255.255.0::eth0:off random.trust_cpu=on root=/dev/vda rw virtio_mmio.device=4K@0xd0000000:5 virtio_mmio.device=4K@0xd0001000:6 virtio_mmio.device=4K@0xd0002000:7
[...]
[    1.113425] EXT4-fs (vda): mounted filesystem with ordered data mode. Opts: (null)
[    1.114644] VFS: Mounted root (ext4 filesystem) on device 254:0.
[    1.115459] devtmpfs: mounted
[    1.116096] Freeing unused decrypted memory: 2036K
[    1.116945] Freeing unused kernel image (initmem) memory: 1420K
[    1.128668] Write protecting the kernel read-only data: 14336k
[    1.131705] Freeing unused kernel image (text/rodata gap) memory: 2044K
[    1.133465] Freeing unused kernel image (rodata/data gap) memory: 144K
[    1.134869] Run /sbin/init as init process
[    1.135755]   with arguments:
[    1.136400]     /sbin/init
[    1.137017]   with environment:
[    1.137712]     HOME=/
[    1.138225]     TERM=linux
[    1.159918] systemd[1]: Failed to find module 'autofs4'
[    1.163986] systemd[1]: systemd 245.4-4ubuntu3.11 running in system mode. (+PAM +AUDIT +SELINUX +IMA +APPARMOR +SMACK +SYSVINIT +UTMP +LIBCRYPTSETUP +GCRYPT +GNUTLS +ACL +XZ +LZ4 +SECCOMP +BLKID +ELFUTILS +KMOD +IDN2 -IDN +PCRE2 default-hierarchy=hybrid)
[    1.166524] systemd[1]: Detected virtualization kvm.
[    1.167101] systemd[1]: Detected architecture x86-64.

Welcome to Ubuntu 20.04.2 LTS!

[...]
[  OK  ] Finished Permit User Sessions.
[  OK  ] Started Getty on tty1.
[  OK  ] Started Serial Getty on ttyS0.
[  OK  ] Reached target Login Prompts.
[  OK  ] Started Network Name Resolution.
[  OK  ] Finished Remove Stale Onli…ext4 Metadata Check Snapshots.
[  OK  ] Reached target Host and Network Name Lookups.
[  OK  ] Started OpenBSD Secure Shell server.
[  OK  ] Started Login Service.
[  OK  ] Started Dispatcher daemon for systemd-networkd.
[  OK  ] Reached target Multi-User System.
[  OK  ] Reached target Graphical Interface.
         Starting Update UTMP about System Runlevel Changes...
[  OK  ] Finished Update UTMP about System Runlevel Changes.

Ubuntu 20.04.2 LTS vaccel-guest.nubificus.co.uk ttyS0

vaccel-guest login:
```

Go ahead and log in (user: `root`, no password).

Now, open another terminal to run the vAccel Agent. A detailed walkthrough of
the execution flow with the agent is shown in
[Running the vAccel Agent](user-guide/vm-example.md#running-the-vaccel-agent).

First get the binary:

```bash
wget https://s3.nbfc.io/nbfc-assets/github/vaccelrt/agent/main/x86_64/release/vaccel-agent
chmod +x vaccel-agent
```

Then, go ahead and run the binary with the `noop` plugin:

```bash
export VACCEL_BACKENDS=/usr/local/lib/libvaccel-noop.so
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
### Listen to port 2048 on the socket exposed by the
### VM (specified in config_vsock.json)
export VACCEL_AGENT_ENDPOINT=unix:///tmp/vaccel.sock_2048
./vaccel-agent -a $VACCEL_AGENT_ENDPOINT
```

You should be presented with the following output:

```console
# ./vaccel-agent -a $VACCEL_AGENT_ENDPOINT
vaccel ttRPC server started. address: unix:///tmp/vaccel.sock_2048
Server is running, press Ctrl + C to exit
```

Now, on the VM terminal, go ahead and run the example application:

```console
Ubuntu 20.04.2 LTS vaccel-guest.nubificus.co.uk ttyS0

vaccel-guest login: root

# /opt/vaccel/bin/classify /opt/vaccel/share/images/dog_1.jpg 1
Initialized session with id: 1
Image size: 54372B
classification tags: This is a dummy classification tag!
```

and the terminal that the agent is running should produce the following output:

```console
Created session 1
session:VaccelId { inner: Some(1) } Image classification
[noop] Calling Image classification for session 1
[noop] Dumping arguments for Image classification:
[noop] len_img: 54372
[noop] will return a dummy result
Destroying session VaccelId { inner: Some(1) }
Destroyed session 1
```

## Jetson example

Running with the Jetson inference plugin requires a working
[jetson-inference](https://github.com/dusty-nv/jetson-inference) installation
along with the corresponding CUDA environment on the machine. If all is set up
correctly you can just skip to
[Running a Jetson-inference example](#running-a-jetson-inference-example). If
not, you can follow the steps below to get a working environment.

If a jetson-inference setup is not available you can either follow
[this guide](jetson.md) to build the vAccel jetson plugin and install the
prerequisites on your host machine, or you can use a container image, provided
you can expose an NVIDIA GPU in the container.

### Running a Jetson-inference example

A simple jetson-inference operation is image classification using `imagenet`.
You can simply run:

```console
$ imagenet-console cat.jpeg
[video]  created imageLoader from cat.jpeg
------------------------------------------------
imageLoader video options:
------------------------------------------------
  -- URI: cat.jpeg
     - protocol:  file
     - location:  cat.jpeg
     - extension: jpeg
  -- deviceType: file
  -- ioType:     input
[...]

imageNet -- loading classification network model from:
         -- prototxt     networks/googlenet.prototxt
         -- model        networks/bvlc_googlenet.caffemodel
         -- class_labels networks/ilsvrc12_synset_words.txt
         -- input_blob   'data'
         -- output_blob  'prob'
         -- batch_size   1

[TRT]    TensorRT version 8.5.1
[...]
[TRT]    [MemUsageChange] TensorRT-managed allocation in IExecutionContext creation: CPU +0, GPU +4, now: CPU 0, GPU 17 (MiB)
[...]
[TRT]
[TRT]    CUDA engine context initialized on device GPU:
[TRT]       -- layers       74
[TRT]       -- maxBatchSize 1
[TRT]       -- deviceMemory 3619328
[TRT]       -- bindings     2
[TRT]       binding 0
                -- index   0
                -- name    'data'
                -- type    FP32
                -- in/out  INPUT
                -- # dims  3
                -- dim #0  3
                -- dim #1  224
                -- dim #2  224
[TRT]       binding 1
                -- index   1
                -- name    'prob'
                -- type    FP32
                -- in/out  OUTPUT
                -- # dims  3
                -- dim #0  1000
                -- dim #1  1
                -- dim #2  1
[TRT]
[TRT]    binding to input 0 data  binding index:  0
[TRT]    binding to input 0 data  dims (b=1 c=3 h=224 w=224) size=602112
[TRT]    binding to output 0 prob  binding index:  1
[TRT]    binding to output 0 prob  dims (b=1 c=1000 h=1 w=1) size=4000
[TRT]

[...]
[TRT]    device GPU, networks/bvlc_googlenet.caffemodel initialized.
[TRT]    imageNet -- loaded 1000 class info entries
[TRT]    imageNet -- networks/bvlc_googlenet.caffemodel initialized.
[image]  loaded 'cat.jpeg'  (640x427, 3 channels)
class 0281 - 0.220981  (tabby, tabby cat)
class 0282 - 0.062819  (tiger cat)
class 0283 - 0.017998  (Persian cat)
class 0284 - 0.017858  (Siamese cat, Siamese)
class 0285 - 0.482666  (Egyptian cat)
class 0287 - 0.180359  (lynx, catamount)
imagenet:  48.26662% class #285 (Egyptian cat)

[TRT]    ------------------------------------------------
[TRT]    Timing Report networks/bvlc_googlenet.caffemodel
[TRT]    ------------------------------------------------
[TRT]    Pre-Process   CPU   0.02268ms  CUDA   0.22272ms
[TRT]    Network       CPU   1.79966ms  CUDA   1.60173ms
[TRT]    Post-Process  CPU   0.02573ms  CUDA   0.02646ms
[TRT]    Total         CPU   1.84807ms  CUDA   1.85091ms
[TRT]    ------------------------------------------------

[...]
[image]  imageLoader -- End of Stream (EOS) has been reached, stream has been closed
imagenet:  shutting down...
imagenet:  shutdown complete.
```

and you can get the classification tag:
`imagenet:  48.26662% class #285 (Egyptian cat)`.

What we've built using the `jetson-inference` plugin, and the vAccel image
classification API operation, is a mechanism to run this over vAccel.

#### Native execution (Running on the Host)

To run the above example using vAccel we can simply execute:

```sh
export LD_LIBRARY_PATH=/usr/local/lib
export VACCEL_BACKENDS=/usr/local/lib/libvaccel-jetson.so
export VACCEL_IMAGENET_NETWORKS=/usr/local/share/networks
/usr/local/bin/classify cat.jpeg 1
```

The output should be something like the following:

```console
classify cat.jpeg 1
Initialized session with id: 1
Image size: 54372B

imageNet -- loading classification network model from:
         -- prototxt     networks/googlenet.prototxt
         -- model        data/networks/bvlc_googlenet.caffemodel
         -- class_labels networks/ilsvrc12_synset_words.txt
         -- input_blob   'data'
         -- output_blob  'prob'
         -- batch_size   1

[TRT]    TensorRT version 8.5.1
[TRT]    loading NVIDIA plugins...
[...]
[TRT]    detected model format - caffe  (extension '.caffemodel')
[TRT]    desired precision specified for GPU: FASTEST
[TRT]    requested fasted precision for device GPU without providing valid calibrator, disabling INT8
[TRT]    [MemUsageChange] Init CUDA: CPU +307, GPU +0, now: CPU 318, GPU 223 (MiB)
[TRT]    Trying to load shared library libnvinfer_builder_resource.so.8.5.1
[TRT]    Loaded shared library libnvinfer_builder_resource.so.8.5.1
[TRT]    [MemUsageChange] Init builder kernel library: CPU +261, GPU +74, now: CPU 634, GPU 297 (MiB)
[...]
[TRT]    [MemUsageChange] TensorRT-managed allocation in engine deserialization: CPU +0, GPU +13, now: CPU 0, GPU 13 (MiB)
[...]
[TRT]    [MemUsageChange] TensorRT-managed allocation in IExecutionContext creation: CPU +0, GPU +4, now: CPU 0, GPU 17 (MiB)
[...]
[TRT]    CUDA engine context initialized on device GPU:
[TRT]       -- layers       78
[TRT]       -- maxBatchSize 1
[TRT]       -- deviceMemory 3619840
[TRT]       -- bindings     2
[TRT]       binding 0
                -- index   0
                -- name    'data'
                -- type    FP32
                -- in/out  INPUT
                -- # dims  3
                -- dim #0  3
                -- dim #1  224
                -- dim #2  224
[TRT]       binding 1
                -- index   1
                -- name    'prob'
                -- type    FP32
                -- in/out  OUTPUT
                -- # dims  3
                -- dim #0  1000
                -- dim #1  1
                -- dim #2  1
[...]
[TRT]    device GPU, networks/bvlc_googlenet.caffemodel initialized.
[TRT]    imageNet -- loaded 1000 class info entries
[TRT]    imageNet -- networks/bvlc_googlenet.caffemodel initialized.
class 0281 - 0.219007  (tabby, tabby cat)
class 0282 - 0.062747  (tiger cat)
class 0283 - 0.017977  (Persian cat)
class 0284 - 0.017837  (Siamese cat, Siamese)
class 0285 - 0.482107  (Egyptian cat)
class 0287 - 0.182987  (lynx, catamount)
imagenet: 48.21070% class #285 (Egyptian cat)
imagenet: attempting to save output image
imagenet: completed saving
imagenet: shutting down...
classification tags: 48.211% Egyptian cat
```

The first two and the last line are output from the classify example (the vAccel
application), whereas the rest is similar (if not identical) to the native
jetson execution, since we run on the Host.

**Note**: The first time your run a classification with a model jetson-inference
is performing some JIT steps to optimize the classification result, so you can
expect increased execution time. The output of this operation is cached for
subsequent executions in the networks folder.

#### Running in a Firecracker VM

In similar fashion as before, we launch the VM & the agent:

```bash
# Launch the Firecracker VM
./firecracker --api-sock fc.sock --config-file config_vsock.json
```

```bash
### Run the Agent on a separate terminal
export VACCEL_BACKENDS=/usr/local/lib/libvaccel-jetson.so
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
### Listen to port 2048 on the socket exposed by the
### VM (specified in config_vsock.json)
export VACCEL_AGENT_ENDPOINT=unix:///tmp/vaccel.sock_2048
./vaccel-agent -a $VACCEL_AGENT_ENDPOINT
```

Similarly, we login as root (no password).

```console
# ./firecracker --api-sock fc.sock --config-file config_vsock.json
[    0.000000] Linux version 6.0.0 (ananos@dell00) (gcc (Ubuntu 9.4.0-1ubuntu1~20.04.1) 9.4.0, GNU ld (GNU Binutils for Ubuntu) 2.34) #14 SMP PREEMPT_DYNAMIC Mon Nov 14 15:52:14 UTC 2022
[    0.000000] Command line: console=ttyS0 reboot=k panic=1 pci=off loglevel=8 root=/dev/vda random.trust_cpu=on root=/dev/vda rw virtio_mmio.device=4K@0xd0000000:5 virtio_mmio.device=4K@0xd0001000:6
[...]
[    2.842908] systemd[1]: Detected virtualization kvm.
[    2.843885] systemd[1]: Detected architecture x86-64.

Welcome to Ubuntu 20.04.2 LTS!

[    2.860233] systemd[1]: Set hostname to <vaccel-guest.nubificus.co.uk>.
[    2.948752] systemd-fstab-g (77) used greatest stack depth: 14152 bytes left
[    2.964256] systemd-sysv-ge (84) used greatest stack depth: 13976 bytes left
[...]
[  OK  ] Started Login Service.
[  OK  ] Started OpenBSD Secure Shell server.
[  OK  ] Finished Remove Stale Onli…ext4 Metadata Check Snapshots.
[  OK  ] Started Dispatcher daemon for systemd-networkd.
[  OK  ] Reached target Multi-User System.
[  OK  ] Reached target Graphical Interface.
         Starting Update UTMP about System Runlevel Changes...
[  OK  ] Finished Update UTMP about System Runlevel Changes.

Ubuntu 20.04.2 LTS vaccel-guest.nubificus.co.uk ttyS0

vaccel-guest login: root
Welcome to Ubuntu 20.04.2 LTS (GNU/Linux 6.0.0 x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.
Last login: Mon Nov 14 19:00:02 UTC 2022 on ttyS0
root@vaccel-guest:~#
```

Once, in the prompt of the guest we check if the environment is set up
correctly:

```console
root@vaccel-guest:~# env |grep -i vaccel
VACCEL_DEBUG_LEVEL=0
VACCEL_BACKENDS=/opt/vaccel/lib/libvaccel-vsock.so
```

and we make sure the agent is running on the separate terminal:

```console
# /opt/vaccel-v0.4.0/bin/vaccel-agent -a $VACCEL_AGENT_ENDPOINT
vaccel ttRPC server started. address: unix:///tmp/vaccel.sock_2048
Server is running, press Ctrl + C to exit
```

On the VM terminal, we run the classification operation:

```console
root@vaccel-guest:~# /opt/vaccel/bin/classify cat.jpeg 1
Initialized session with id: 1
Image size: 54372B
classification tags: 48.211% Egyptian cat
```

We see that the classification tag is accurate (at least in par with the native
execution). And we see the output we expect in the agent terminal:\

```console
Created session 1
session:VaccelId { inner: Some(1) } Image classification

imageNet -- loading classification network model from:
         -- prototxt     networks/googlenet.prototxt
         -- model        networks/bvlc_googlenet.caffemodel
         -- class_labels networks/ilsvrc12_synset_words.txt
         -- input_blob   'data'
         -- output_blob  'prob'
         -- batch_size   1

[TRT]    TensorRT version 8.5.1
[TRT]    loading NVIDIA plugins...
[...]
[TRT]    requested fasted precision for device GPU without providing valid calibrator, disabling INT8
[TRT]    [MemUsageChange] Init CUDA: CPU +306, GPU +0, now: CPU 318, GPU 223 (MiB)
[TRT]    Trying to load shared library libnvinfer_builder_resource.so.8.5.1
[TRT]    Loaded shared library libnvinfer_builder_resource.so.8.5.1
[TRT]    [MemUsageChange] Init builder kernel library: CPU +262, GPU +74, now: CPU 635, GPU 297 (MiB)
[...]
[TRT]    CUDA engine context initialized on device GPU:
[TRT]       -- layers       78
[TRT]       -- maxBatchSize 1
[TRT]       -- deviceMemory 3619840
[TRT]       -- bindings     2
[TRT]       binding 0
                -- index   0
                -- name    'data'
                -- type    FP32
                -- in/out  INPUT
                -- # dims  3
                -- dim #0  3
                -- dim #1  224
                -- dim #2  224
[TRT]       binding 1
                -- index   1
                -- name    'prob'
                -- type    FP32
                -- in/out  OUTPUT
                -- # dims  3
                -- dim #0  1000
                -- dim #1  1
                -- dim #2  1
[TRT]
[TRT]    binding to input 0 data  binding index:  0
[TRT]    binding to input 0 data  dims (b=1 c=3 h=224 w=224) size=602112
[TRT]    binding to output 0 prob  binding index:  1
[TRT]    binding to output 0 prob  dims (b=1 c=1000 h=1 w=1) size=4000
[TRT]
[TRT]    device GPU, data/networks/bvlc_googlenet.caffemodel initialized.
[TRT]    imageNet -- loaded 1000 class info entries
[TRT]    imageNet -- networks/bvlc_googlenet.caffemodel initialized.
class 0281 - 0.219007  (tabby, tabby cat)
class 0282 - 0.062747  (tiger cat)
class 0283 - 0.017977  (Persian cat)
class 0284 - 0.017837  (Siamese cat, Siamese)
class 0285 - 0.482107  (Egyptian cat)
class 0287 - 0.182987  (lynx, catamount)
imagenet: 48.21070% class #285 (Egyptian cat)
imagenet: attempting to save output image
imagenet: completed saving
imagenet: shutting down...
Destroying session VaccelId { inner: Some(1) }
Destroyed session 1
```
