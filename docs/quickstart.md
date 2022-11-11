# Quickstart

This is a quick start guide for running a simple vAccel application. 

- [Build from Source](#build-from-source) or [get the binary packages](#binary-packages) [currently only for Debian/Ubuntu variants]
- Run a [simple example](#simple-example) [using the `noop` plugin]
- Run the same example [in a VM](#vm-example) [same code in a VM]
- Run a more [elaborate example](#jetson-example) [same scenario, using the `jetson-inference` plugin]

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

## VM example

To run our code in a VM, we will have to use a virtual plugin that will handle
the forwarding of the function call from the VM to the Host system. That said,
we still need vAccel in the Host system to execute the forwarded call. A visual
representation of the execution flow is shown in Figure 1.

<figure>
  <img src="/img/vaccel-vm-flow.png" width="800" align=left />
  <figcaption>Figure 1. VM application execution flow</figcaption>
</figure>

To enable this functionality, we will use the `VSOCK` plugin in the guest, and,
still, the `NOOP` plugin in the Host.

First, let's bootstrap the VM.

### VM setup

To bootstrap a simple VM we will use AWS firecracker and an example kernel &
rootfs. In [Run a vAccel application in a VM](vm-example.md) we provide more
examples of the various hypervisors/VMMs we have tested and support. You can
get the binaries using the commands below:

```bash
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

## Jetson example


