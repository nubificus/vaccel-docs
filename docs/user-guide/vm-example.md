# Run a vAccel application in a VM

## Overview

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
as previously, the `NOOP` plugin in the Host. To intercept requests originating
from the guest, we use the vAccel Agent, running on the Host. Section
[Running the agent](#running-the-vaccel-agent) describes the process to run the
agent.

First, let's bootstrap the VM.

## Bootstrap the VM

To bootstrap a simple VM we have the option of using any hypervisor/VMM that
supports the `virtio-vsock` device. We have tried:
[AWS Firecracker](#firecracker), [QEMU](#qemu),
[Cloud Hypervisor](#cloud-hypervisor), and [Dragonball](#dragonball).

First, we will need an example kernel & rootfs. All `rust-vmm` based VMMs can
use the same artifacts. For QEMU we will use a different kernel, but the same
rootfs.

Each section below describes the steps for the respective VMM.

The common file for all cases is the `rootfs` image. You can get it using the
following command:

```bash
wget https://s3.nbfc.io/nbfc-assets/github/vaccelrt/vm-example/x86_64/rootfs.img
```

### Firecracker

You can get the binaries needed for booting a Firecracker VM using the commands
below:

```bash
wget https://s3.nbfc.io/nbfc-assets/github/vaccelrt/vm-example/x86_64/fc/firecracker
wget https://s3.nbfc.io/nbfc-assets/github/vaccelrt/vm-example/x86_64/fc/config_vsock.json
wget https://s3.nbfc.io/nbfc-assets/github/vaccelrt/vm-example/x86_64/rust-vmm/vmlinux
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

To launch the VM, all we have to do is run the following command (make sure you
run as `root`):

```bash
chmod +x firecracker

./firecracker --api-sock fc.sock --config-file config_vsock.json
```

**Note** You have to make sure that `./fc.sock` and `/tmp/vaccel.sock` are
cleaned up before launching the VM, as firecracker will fail with the following
errors:

```console
[anonymous-instance:fc_api:ERROR:src/firecracker/src/api_server_adapter.rs:163] Failed to open the API socket at: fc.sock. Check that it is not already used.
```

or

```console
[anonymous-instance:main:ERROR:src/firecracker/src/main.rs:496] Configuration for VMM from one single json failed: Vsock device error: Cannot create backend for vsock device: UnixBind(Os { code: 98, kind: AddrInUse, message: "Address in use" })
```

So make sure before launching to rm these files:
`rm fc.sock ; rm /tmp/vaccel.sock`

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

launch a new terminal and go to
[Running the application](#running-the-application)

### Cloud hypervisor

For Cloud Hypervisor, the process is almost identical to Firecracker
(`rust-vmm`-based). You can get the binaries needed for booting a Cloud
Hypervisor VM using the commands below:

```bash
wget https://s3.nbfc.io/nbfc-assets/github/vaccelrt/vm-example/x86_64/clh/cloud-hypervisor
wget https://s3.nbfc.io/nbfc-assets/github/vaccelrt/vm-example/x86_64/rust-vmm/vmlinux
```

We should have the following files available:

```console
# tree .
.
├── cloud-hypervisor
├── rootfs.img
└── vmlinux

0 directories, 3 files
```

We need to make the VMM binary file executable:

```bash
chmod +x cloud-hypervisor
```

To launch the VM, all we have to do is run the following command:

```bash
./cloud-hypervisor --kernel vmlinux --disk path=rootfs.img \
                     --memory size=1024M --cpus boot=1 \
                   --cmdline "console=hvc0 root=/dev/vda rw" \
                   --vsock cid=42,socket=/tmp/vaccel.sock \
                   --console tty
```

We should be presented with a login prompt:

```console
[    0.000000] Linux version 6.0.0 (ananos@dell00) (gcc (Ubuntu 9.4.0-1ubuntu1~20.04.1) 9.4.0, GNU ld (GNU Binutils for Ubuntu) 2.34) #14 SMP PREEMPT_DYNAMIC Mon Nov 14 15:52:14 UTC 2022
[    0.000000] Command line: console=hvc0 root=/dev/vda rw
[...]
[    0.448586] systemd[1]: systemd 245.4-4ubuntu3.11 running in system mode. (+PAM +AUDIT +SELINUX +IMA +APPARMOR +SMACK +SYSVINIT +UTMP +LIBCRYPTSETUP +GCRYPT +GNUTLS +ACL +XZ +LZ4 +SECCOMP +BLKID +ELFUTILS +KMOD +IDN2 -IDN +PCRE2 default-hierarchy=hybrid)
[    0.448851] systemd[1]: Detected virtualization kvm.
[    0.448901] systemd[1]: Detected architecture x86-64.

Welcome to Ubuntu 20.04.2 LTS!

[    0.450357] systemd[1]: Set hostname to <vaccel-guest.nubificus.co.uk>.
[    0.478414] systemd-fstab-g (79) used greatest stack depth: 14152 bytes left
[    0.508385] systemd-sysv-ge (86) used greatest stack depth: 13976 bytes left
[    0.540187] systemd[1]: system-getty.slice: unit configures an IP firewall, but the local system does not support BPF/cgroup firewalling.
[...]
[  OK  ] Started OpenBSD Secure Shell server.
[  OK  ] Started Login Service.
[  OK  ] Started Dispatcher daemon for systemd-networkd.
[  OK  ] Reached target Multi-User System.
[  OK  ] Finished Remove Stale Onli…ext4 Metadata Check Snapshots.
[  OK  ] Reached target Graphical Interface.
         Starting Update UTMP about System Runlevel Changes...
[  OK  ] Finished Update UTMP about System Runlevel Changes.

Ubuntu 20.04.2 LTS vaccel-guest.nubificus.co.uk hvc0

vaccel-guest login:
```

Go ahead and log in (user: `root`, no password).

launch a new terminal and go to
[Running the application](#running-the-application)

### QEMU

You need the following files to bootstrap a QEMU VM:

```bash
# Get the latest release
mkdir vm-artifacts
cd vm-artifacts
wget https://s3.nbfc.io/nbfc-assets/github/vaccel/plugins/virtio/rev/main/x86_64/debug/vaccel-virtio-latest-vm.tar.xz
tar xvf vaccel-virtio-latest-vm.tar.xz
for file in virtio-accel-*.tar.xz; do tar -xvf "$file"; done
```

The directory structure should be like the following:

```console
# tree
.
├── bzImage-6.1.128-amd64
├── linux-6.1.128-amd64-fc.config
├── linux-6.1.128-amd64.config
├── rootfs.img
├── vaccel-virtio-latest-vm.tar.xz
├── virtio-accel-0.1.0-16-f87c69ec-fc-linux-image.tar.xz
├── virtio-accel-0.1.0-16-f87c69ec-linux-image.tar.xz
└── vmlinux-6.1.128-amd64-fc

0 directories, 8 files
```
The folder must contain a rootf.img and a compressed Linux kernel image (bzImage\*) with the virtio-accel module, VirtIO plugin and vAccel pre-installed.
We will use these images to emulate an entire system with QEMU.

To spawn a QEMU VM, we provide a Docker image with QEMU pre-installed.
```bash
sudo docker pull harbor.nbfc.io/nubificus/qemu-vaccel:x86_64
```

To run the qemu docker image:
```bash
cd ..
sudo docker run  -it --privileged  --rm --mount type=bind,source="$(pwd)",destination=/data \
	harbor.nbfc.io/nubificus/qemu-vaccel:x86_64 \
	-r vm-artifacts/rootfs.img -k $(ls vm-artifacts/bzImage*) \
	--drive-cache -M pc --vcpus $(nproc) \
	--cpu max -s qemu-$(date +"%Y%m%d-%H%M%S")
```

The result of the above command is to create a VM under a docker container with pre-installed QEMU:

```console
2025.03.24-13:22:16.16 - <debug> Initializing vAccel
2025.03.24-13:22:16.16 - <info> vAccel 0.6.1-194-19056528
2025.03.24-13:22:16.16 - <debug> Config:
2025.03.24-13:22:16.16 - <debug>   plugins = libvaccel-noop.so
2025.03.24-13:22:16.16 - <debug>   log_level = debug
2025.03.24-13:22:16.16 - <debug>   log_file = (null)
2025.03.24-13:22:16.16 - <debug>   profiling_enabled = false
2025.03.24-13:22:16.16 - <debug>   version_ignore = false
2025.03.24-13:22:16.16 - <debug> Created top-level rundir: /run/user/0/vaccel/x5HdKV
2025.03.24-13:22:16.16 - <info> Registered plugin noop 0.6.1-194-19056528
2025.03.24-13:22:16.16 - <debug> Registered op noop from plugin noop
2025.03.24-13:22:16.16 - <debug> Registered op blas_sgemm from plugin noop
2025.03.24-13:22:16.16 - <debug> Registered op image_classify from plugin noop
2025.03.24-13:22:16.16 - <debug> Registered op image_detect from plugin noop
2025.03.24-13:22:16.16 - <debug> Registered op image_segment from plugin noop
2025.03.24-13:22:16.16 - <debug> Registered op image_pose from plugin noop
2025.03.24-13:22:16.16 - <debug> Registered op image_depth from plugin noop
2025.03.24-13:22:16.16 - <debug> Registered op exec from plugin noop
2025.03.24-13:22:16.16 - <debug> Registered op tf_session_load from plugin noop
2025.03.24-13:22:16.16 - <debug> Registered op tf_session_run from plugin noop
2025.03.24-13:22:16.16 - <debug> Registered op tf_session_delete from plugin noop
2025.03.24-13:22:16.16 - <debug> Registered op minmax from plugin noop
2025.03.24-13:22:16.16 - <debug> Registered op fpga_arraycopy from plugin noop
2025.03.24-13:22:16.16 - <debug> Registered op fpga_vectoradd from plugin noop
2025.03.24-13:22:16.16 - <debug> Registered op fpga_parallel from plugin noop
2025.03.24-13:22:16.16 - <debug> Registered op fpga_mmult from plugin noop
2025.03.24-13:22:16.16 - <debug> Registered op exec_with_resource from plugin noop
2025.03.24-13:22:16.16 - <debug> Registered op torch_jitload_forward from plugin noo
2025.03.24-13:22:16.16 - <debug> Registered op torch_sgemm from plugin noop
2025.03.24-13:22:16.16 - <debug> Registered op opencv from plugin noop
2025.03.24-13:22:16.16 - <debug> Registered op tflite_session_load from plugin noop
2025.03.24-13:22:16.16 - <debug> Registered op tflite_session_run from plugin noop
2025.03.24-13:22:16.16 - <debug> Registered op tflite_session_delete from plugin noo
2025.03.24-13:22:16.16 - <debug> Loaded plugin noop from libvaccel-noop.so
```
The noop plugin is pre-exported. To use a different plugin, ensure you export it before running the application.

#### Run an application on guest
To run a vAccel example, we first need to connect to the VM by executing the already running Docker container.
Open a terminal and copy the \<CONTAINER ID\> the following command returns:
```bash
docker ps
```

Run a bash shell inside the container by replacing \<CONTAINER ID\> with the ID the previous command return.
```bash
docker exec -it <CONTAINER ID> /bin/bash
```

Connect to the VM:
```bash
ssh localhost -p 60022
```

Let's try one of the vAccel examples, for instance image classification: `classify`.
This small program gets an image as an input and the number of
iterations and returns the classification tag for this image. We run the
following:

```bash
classify /usr/local/share/vaccel/images/example.jpg 1
```

We see that the operation was successful and we got a the following expected output on guest:

```bash
Initialized session with id: 1
classification tags: This is a dummy classification tag!
```

While on host we see the following output:
```bash
2025.03.24-13:26:37.24 - <debug> New rundir for session 1: /run/user/0/vaccel/x5HdKV
2025.03.24-13:26:37.24 - <debug> Initialized session 1
2025.03.24-13:26:37.24 - <debug> session:1 Looking for plugin implementing VACCEL_OP
2025.03.24-13:26:37.24 - <debug> Returning func from hint plugin noop
2025.03.24-13:26:37.24 - <debug> Found implementation in noop plugin
2025.03.24-13:26:37.24 - <debug> [noop] Calling Image classification for session 1
2025.03.24-13:26:37.24 - <debug> [noop] Dumping arguments for Image classification:
2025.03.24-13:26:37.24 - <debug> [noop] model: (null)
2025.03.24-13:26:37.24 - <debug> [noop] len_img: 79281
2025.03.24-13:26:37.24 - <debug> [noop] len_out_text: 512
2025.03.24-13:26:37.24 - <debug> [noop] len_out_imgname: 512
2025.03.24-13:26:37.24 - <debug> [noop] will return a dummy result
2025.03.24-13:26:37.24 - <debug> [noop] will return a dummy result
2025.03.24-13:26:37.24 - <debug> Released session 1

```

### DragonBall

To launch a Dragonball VM, we will use a nifty
[tool](https://github.com/openanolis/dbs-cli) developed by the OpenAnolis
people, `dbs-cli`. This tool provides a CLI to launch the Dragonball hypervisor
and interact with it.

The files we need are:

```bash
wget https://s3.nbfc.io/nbfc-assets/github/vaccelrt/vm-example/x86_64/dbs/dbs-cli
wget https://s3.nbfc.io/nbfc-assets/github/vaccelrt/vm-example/x86_64/rust-vmm/vmlinux
```

We should have the following directory structure:

```console
# tree
.
├── dbs-cli
├── rootfs.img
└── vmlinux

0 directories, 3 files
```

The command to spawn a Dragonball VM is shown below:

```bash
# make the VMM binary executable
chmod +x dbs-cli

# launch the VM
./dbs-cli --kernel-path vmlinux --rootfs rootfs.img \
          --boot-args "console=ttyS0 pci=off root=/dev/vda rw" \
          --vsock /tmp/vaccel.sock
```

The logs of the VM are similar to the above cases:

```console
[    0.000000] Linux version 6.0.0 (ananos@dell00) (gcc (Ubuntu 9.4.0-1ubuntu1~20.04.1) 9.4.0, GNU ld (GNU Binutils for Ubuntu) 2.34) #14 SMP PREEMPT_DYNAMIC Mon Nov 14 15:52:14 UTC 2022
[    0.000000] Command line: console=ttyS0 tty0 reboot=k debug panic=1 pci=off root=/dev/vda virtio_mmio.device=8K@0xc0000000:5 virtio_mmio.device=8K@0xc0002000:5
[...]
[    1.977652] systemd[1]: Mounting cgroup to /sys/fs/cgroup/cpu,cpuacct of type cgroup with options cpu,cpuacct.
[    1.978731] systemd[1]: Mounting cgroup to /sys/fs/cgroup/pids of type cgroup with options pids.
[    1.979455] systemd[1]: Mounting cgroup to /sys/fs/cgroup/memory of type cgroup with options memory.
[    1.980219] systemd[1]: Mounting cgroup to /sys/fs/cgroup/cpuset of type cgroup with options cpuset.

Welcome to Ubuntu 20.04.2 LTS!

[    2.000846] systemd[1]: Set hostname to <vaccel-guest.nubificus.co.uk>.
[    2.002803] systemd[1]: Successfully added address 127.0.0.1 to loopback interface
[    2.004233] systemd[1]: Successfully added address ::1 to loopback interface
[    2.005430] systemd[1]: Successfully brought loopback interface up
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

vaccel-guest login:
```

Again, as with the previous hypervisors, we log in using the root user (user:
`root`, no password).

launch a new terminal and go to
[Running the application](#running-the-application)

### Running the application

To run the application we first need to provide the backend where the vAccel API
operations will be handled. This is done in the guest via the `VSOCK` plugin and
in the Host via the `vaccel-agent`. We have setup the guest part above for each
of the hypervisors supported. Let's now move to the agent part.

#### Running the vAccel agent

The `vaccel-agent` is just another vAccel application. It consumes the vAccel
API like any other app, with the additional value of being able to receive
commands via `ttrpc`. So we need to include the path to `libvaccel.so` in the
`LD_LIBRARY_PATH` variable, and specify the plugin we want to use via the
`VACCEL_BACKENDS` variable. The agent currently supports three socket types:
`UNIX`, `VSOCK`, and `TCP`.

##### Installing the vAccel agent

If you haven't already installed the vaccel-agent binary, follow the
instructions in the [relevant section](binaries.md#install-vaccel-agent).

In short, for `x86_64`:

```sh
wget https://s3.nbfc.io/nbfc-assets/github/vaccelrt/agent/main/x86_64/Release-deb/vaccelrt-agent-0.3.7-Linux.deb
dpkg -i vaccelrt-agent-0.3.7-Linux.deb
```

To run the agent we need to set the plugin using the `VACCEL_BACKENDS` variable
and the endpoint. Use the following commands:

```bash
export VACCEL_BACKENDS=/usr/local/lib/libvaccel-noop.so
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
export VACCEL_AGENT_ENDPOINT=vsock://42:2048
./vaccel-agent -a $VACCEL_AGENT_ENDPOINT
```

You should be presented with the following output:

```console
# ./vaccel-agent -a $VACCEL_AGENT_ENDPOINT
vaccel ttRPC server started. address: vsock://40:2048
Server is running, press Ctrl + C to exit
```

You could also enable `debug` by setting the env variable `VACCEL_DEBUG=4`.

**Note**: _Depending on which VM case you consider, you might need to edit
`$VACCEL_AGENT_ENDPOINT`. For example, for the all `rust-vmm` clones
(Firecracker, Cloud hypervisor, Dragonball, etc.), the `VACCEL_AGENT_ENDPOINT`
variable corresponds to the `vsock` socket file specified in the definition of
the vsock device in `config.json`. In our example this is `/tmp/vaccel.sock`.
Since the `vsock` implementation of these VMMs assumes the `vsock` port as a
postfix to the socket file, the value of the variable is:_

```bash
VACCEL_AGENT_ENDPOINT=unix:///tmp/vaccel.sock_2048
```

We have prepared the Host to receive vAccel API operations via `VSOCK`. Let's
move to the guest console terminal.

#### Running the application in the guest

In the guest, we will be running a vAccel application; so we need to specify the
path to `libvaccel.so` and the plugin to be used. In the pre-built rootfs we
have included the `VSOCK` plugin, at `/opt/vaccel/lib/libvaccel-vsock.so`. All
the env vars are set, except for the `VACCEL_VSOCK` parameter, which specifies
the endpoint of the agent. Its default value is `vsock://2:2048`. Since we've
setup the agent to listen to port `2048`, we're good to go.

**Note**: _The Host's default `vsock_id` is `2`, that's why the guest only needs
to set up the port (`2048`)._

The vAccel examples are already in the `rootfs` image, installed at
`/opt/vaccel/bin`. So the only thing needed is to execute the example:

```console
# /opt/vaccel/bin/classify /opt/vaccel/share/images/dog_1.jpg 1
Initialized session with id: 1
Image size: 54372B
classification tags: This is a dummy classification tag!
```

We got the same output as with the
[native execution case](build-run-app.md#running-a-vaccel-application). Well,
almost the same; what we missed is the plugin output. See the native execution
case below:

```console
$ /opt/vaccel/bin/classify images/example.jpg 1
Initialized session with id: 1
Image size: 79281B
[noop] Calling Image classification for session 1
[noop] Dumping arguments for Image classification:
[noop] len_img: 79281
[noop] will return a dummy result
classification tags: This is a dummy classification tag!
```

The `[noop]` lines are not present when running from the VM. This is because the
plugin is executing in the host. We only get the `classification tags:` result
back. If you look at the other terminal, where the agent is running, you should
see the following:

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

Aha! the plugin output is there (which is expected, since the plugin is running
on the Host).
