# Virtio Accel

Virtio Accel was inspired by the [Virtio Crypto](https://github.com/gongleiarei/virtio)
paravirtual device for enabling accelerated crypto operations inside a Virtual
Machine.

We extended the idea of accelerated crypto operations to any acceleratable
operation, which resulted in the `virtio-accel` module and the corresponding
`vAccel` plugin that uses it to allow vAccel applications to use accelerated
operations from within a Virtual Machine. Currently we support the AWS
Firecracker and QEMU hypervisors. 

## Building the kernel module

We first need to build the virtio-accel module that will be used inside our
VM. We will need the source of the kernel module and a kernel tree.

### Firecracker

For Firecracker we use Linux kernel version `4.20`, because that is consistent
with the configuration the AWS Firecracker team is shipping but the module itself
should be able to build with newer kernel versions, as well. For example, for
our [k8s](/k8s/kata) deployment of vAccel we use Linux Kernel version `5.4.60`

Let's fetch and build the kernel

```sh
# Fetch the Linux kernel tree
git clone --depth=1 -b v4.20 https://github.com/torvalds/linux.git

cd linux

# Fetch the Firecracker config
wget https://raw.githubusercontent.com/firecracker-microvm/firecracker/master/resources/microvm-kernel-x86_64.config -O arch/x86/configs/microvm.config

touch .config
make microvm.config
make vmlinux

cd ..
ls linux/vmlinux
linux/vmlinux
```

You should now have a newly built kernel image under `linux/vmlinux`, which
you can use to boot with your Firecracker VM.

And now we can build the module: 

```sh
git clone https://github.com/cloudkernels/virtio-accel
make -C virtio-accel KDIR=$(pwd)/linux ZC=0
ls virtio-accel/virtio_accel.ko
virtio-accel/virtio_accel.ko
```

This should build the module under `virtio-accel/virtio_accel.ko`.

**Note**: The virtio-accel module supports zero-copy operations. This functionality
has not been implemented yet in Firecracker, so we disabled the feature passing
`ZC=0` to the `Makefile`.

### QEMU

TBD

## Building the vAccel plugin

The `vAccel` runtime ships with a virtio plugin which *speaks* the virtio-accel
module's ioctl language to offload computation from a VM guest to the host.

```sh
# Fetch the vAccel repo
git clone --recursive https://github.com/nubificus/vaccel
cd vaccel

mkdir build
cd build
cmake .. -DBUILD_PLUGIN_VIRTIO=ON -DVIRTIO_ACCEL_ROOT=../../virtio-accel
make

cd ../../
ls vaccelrt/build/plugins/virtio/libvaccel-virtio.so
vaccelrt/build/plugins/virtio/libvaccel-virtio.so
```

This builds the plugin and places it under `vaccelrt/build/plugins/virtio/libvaccel-virtio.so`.
You can now insert the plugin to your VMs rootfs and run a vAccel application.
