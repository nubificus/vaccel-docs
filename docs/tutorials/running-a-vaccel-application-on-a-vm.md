# Running a vAccel application on a VM

## Overview

To run a vAccel application on a VM you have to use a suitable transport plugin.
The plugin components will handle the forwarding of the function call from the
guest (VM) to the host system. Since a transport plugin will essentially forward
a vAccel function call from one vAccel instance to another, a valid vAccel
installation is required for both the guest **and** the host system. A visual
representation of the execution flow is shown in Figure 1.

![vAccel VM execution flow](/assets/images/vaccel-vm-light.svg#only-light){width="800"}
![vAccel VM execution flow](/assets/images/vaccel-vm-dark.svg#only-dark){width="800"}

/// caption  
Figure 1. vAccel VM execution flow  
///

The easiest way to run a vAccel application on a VM is to use the `RPC` plugin.
This plugin leverages the VirtIO vSock device for guest-host communication
without requiring any kernel customization. Guest-host communication over vSock
is handled by the the vAccel `RPC` plugin (guest) and the vAccel RPC agent
(host). In order to use the `RPC` plugin the following components must be in
place:

1. _Host:_ The vAccel RPC agent + vAccel + an acceleration plugin, to handle the
   forwarded calls and perform the actual acceleration
2. _Guest:_ vAccel + the `RPC` plugin, to forward the application calls

## Preparing the host

If you have not already installed vAccel,
[install it](../getting-started/installation.md) from binaries or from source.
The rest of this guide assumes vAccel libraries exist in the standard library
search paths.

### Installing vAccel RPC agent

vAccel RPC agent will handle the RPC requests and forward calls to the host
vAccel instance. You can find more information on how to install the
`vaccel-rpc-agent` binary at the
[relevant section](../plugins/available-plugins/transport-plugins/rpc-plugin.md#installing-the-rpc-agent).

## Preparing the VM artifacts

To boot a working VM you will need at least a kernel and rootfs image. The
`VirtIO` plugin artifacts are a good starting point for running a basic
vAccel-enabled VM. You can get them with:

```sh
mkdir downloads

# Download the artifacts.
# You can replace `x86_64` with `aarch64` below for aarch64 VM artifacts
wget -P downloads \
    https://s3.nbfc.io/nbfc-assets/github/vaccel/plugins/virtio/rev/main/x86_64/debug/vaccel-virtio-latest-vm.tar.xz

# Extract all of them in the current directory
tar xfv downloads/vaccel-virtio-latest-vm.tar.xz
find -name "virtio-accel*.tar.xz" -exec tar xfv {} \;
rm virtio-accel*.tar.xz

# Optionally, rename files for simplicity in the next steps
for file in linux-*.config bzImage-* vmlinux-*; do
    new_name=$(echo "$file" | sed -E 's/-[0-9]+\.[0-9]+\.[0-9]+-/-/')
    mv "$file" "$new_name"
done
mv vmlinux-amd64-fc vmlinux
mv bzImage-amd64 bzImage
```

This should leave you with 3 sets of files in the current directory:

- A `rootfs.img` containing Ubuntu with a vAccel installation
- A `vmlinux` and a `linux-amd64-fc.config` that correspond to a basic
  (uncompressed) Linux kernel image meant to be used with Firecracker
- A `bzImage` and a `linux-amd64.config` that correspond to a basic (compressed)
  Linux kernel image meant to be used with other VMMs

To use the `rootfs.img` you will need to install the `RPC` plugin:

```sh
# Mount the image
mkdir temp
sudo mount rootfs.img temp

# Download and install the `RPC` plugin binaries.
# You can replace `x86_64` with `aarch64` below if you used the aarch64 VM
# artifacts
wget -P downloads \
    https://s3.nbfc.io/nbfc-assets/github/vaccel/plugins/rpc/rev/main/x86_64/release/vaccel-rpc-latest-bin.tar.gz
sudo tar xfv downloads/vaccel-rpc-latest-bin.tar.gz \
    --strip-components=2 -C ./temp/usr/local

# Comment out unnecessary fstab entries
sudo sed -i '/9p/s/^/#/' ./temp/etc/fstab

sudo umount temp
rm -r temp
```

Your current directory should look something like:

```console
$ tree -L 1
.
├── bzImage
├── downloads
├── linux-amd64-fc.config
├── linux-amd64.config
├── rootfs.img
└── vmlinux

1 directory, 5 files
```

## Booting a vAccel-enabled VM

With the required artifacts in place, you can run any of the VMMs we have
tested: [Firecracker](#firecracker), [Cloud Hypervisor](#cloud-hypervisor) or
[QEMU](#qemu). You will need access to `/dev/kvm` so make sure that your user is
a member of the `kvm` group or launch the VM as the `root` user.

### Firecracker

You can get the latest [Firecracker](https://firecracker-microvm.github.io/)
release from the
[official repo](https://github.com/firecracker-microvm/firecracker/releases/latest).
Ie. to download and extract Firecracker v1.11.0 for amd64:

```sh
wget -P downloads \
    https://github.com/firecracker-microvm/firecracker/releases/download/v1.11.0/firecracker-v1.11.0-x86_64.tgz
mkdir firecracker
tar xfv downloads/firecracker-v1.11.0-x86_64.tgz \
    --strip-components=1 -C firecracker

# Optionally, link to a common filename to simplify next steps
ln -s firecracker/firecracker-v1.11.0-x86_64 firecracker/firecracker
```

A json config is needed to boot a VM. You can download a sample config with:

```sh
wget https://s3.nbfc.io/nbfc-assets/github/vaccelrt/vm-example/x86_64/fc/config_vsock.json
```

The updated current directory should look like:

```console
$ tree -L 1
.
├── bzImage
├── config_vsock.json
├── downloads
├── firecracker
├── linux-amd64-fc.config
├── linux-amd64.config
├── rootfs.img
└── vmlinux

2 directories, 6 files
```

<!-- markdownlint-disable code -->

???+ note

    If you have already run `firecracker` or these files exist for some
    reason, ensure that `./fc.sock` and `/tmp/vaccel.sock` are cleaned up before
    trying to launch the VM:

    ```sh
    rm fc.sock /tmp/vaccel.sock
    ```

    If you do not, `firecracker` will fail with errors like:

    ```console
    2025-03-30T17:56:21.871223256 [anonymous-instance:main] Running Firecracker v1.11.0
    2025-03-30T17:56:21.871393598 [anonymous-instance:main] RunWithApiError error: Failed to open the API socket at: fc.sock. Check that it is not already used.
    Error: RunWithApi(FailedToBindSocket("fc.sock"))
    2025-03-30T17:56:21.871438293 [anonymous-instance:main] Firecracker exiting with error. exit_code=1
    ```

    or

    ```console
    2025-03-30T17:55:39.607508767 [anonymous-instance:main] Running Firecracker v1.11.0
    2025-03-30T17:55:39.608446159 [anonymous-instance:main] RunWithApiError error: Failed to build MicroVM from Json: Configuration for VMM from one single json failed: Vsock device error: Cannot create backend for vsock device: Error binding to the host-side Unix socket: Address in use (os error 98)
    Error: RunWithApi(BuildFromJson(ParseFromJson(VsockDevice(CreateVsockBackend(UnixBind(Os { code: 98, kind: AddrInUse, message: "Address in use" }))))))
    2025-03-30T17:55:39.608572227 [anonymous-instance:main] Firecracker exiting with error. exit_code=1
    ```

<!-- markdownlint-restore -->

Finally, to launch the VM use:

```console
$ ./firecracker/firecracker --api-sock fc.sock --config-file config_vsock.json
2025-03-30T18:14:06.845979099 [anonymous-instance:main] Running Firecracker v1.11.0
2025-03-30T18:14:06.866599137 [anonymous-instance:main] Artificially kick devices.
2025-03-30T18:14:06.866685961 [anonymous-instance:fc_vcpu 0] Received a VcpuEvent::Resume message with immediate_exit enabled. immediate_exit was disabled before proceeding
2025-03-30T18:14:06.866735354 [anonymous-instance:fc_vcpu 1] Received a VcpuEvent::Resume message with immediate_exit enabled. immediate_exit was disabled before proceeding
2025-03-30T18:14:06.866773907 [anonymous-instance:main] Successfully started microvm that was configured from one single json
[    0.000000] Linux version 6.1.132 (root@buildkitsandbox) (gcc (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0, GNU ld (GNU Binutils for Ubuntu) 2.42) #1 SMP PREEMPT_DYNAMIC Sun Mar 30 00:13:16 UTC 2025
[    0.000000] Command line: console=ttyS0 reboot=k panic=1 pci=off loglevel=8 root=/dev/vda random.trust_cpu=on root=/dev/vda rw virtio_mmio.device=4K@0xd0000000:5 virtio_mmio.device=4K@0xd0001000:6
[...]
[    0.448265] EXT4-fs (vda): mounted filesystem with ordered data mode. Quota mode: none.
[    0.449018] VFS: Mounted root (ext4 filesystem) on device 254:0.
[    0.450006] devtmpfs: mounted
[    0.450969] Freeing unused kernel image (initmem) memory: 2476K
[    0.451506] Write protecting the kernel read-only data: 18432k
[    0.453970] Freeing unused kernel image (text/rodata gap) memory: 2044K
[    0.457003] Freeing unused kernel image (rodata/data gap) memory: 1564K
[    0.457615] Run /sbin/init as init process
[    0.458012]   with arguments:
[    0.458293]     /sbin/init
[    0.458548]   with environment:
[    0.458845]     HOME=/
[    0.459071]     TERM=linux
SELinux:  Could not open policy file <= /etc/selinux/targeted/policy/policy.33:  No such file or directory
[    0.496211] systemd[1]: systemd 255.4-1ubuntu8.5 running in system mode (+PAM +AUDIT +SELINUX +APPARMOR +IMA +SMACK +SECCOMP +GCRYPT -GNUTLS +OPENSSL +ACL +BLKID +CURL +ELFUTILS +FIDO2 +IDN2 -IDN +IPTC +KMOD +LIBCRYPTSETUP +LIBFDISK +PCRE2 -PWQUALITY +P11KIT +QRENCODE +TPM2 +BZIP2 +LZ4 +XZ +ZLIB +ZSTD -BPF_FRAMEWORK -XKBCOMMON +UTMP +SYSVINIT default-hierarchy=unified)
[    0.499091] systemd[1]: Detected virtualization kvm.
[    0.499603] systemd[1]: Detected architecture x86-64.

Welcome to Ubuntu 24.04.1 LTS!

[...]
[  OK  ] Started getty@tty1.service - Getty on tty1.
[  OK  ] Started getty@tty2.service - Getty on tty2.
[  OK  ] Started getty@tty3.service - Getty on tty3.
[  OK  ] Started getty@tty4.service - Getty on tty4.
[  OK  ] Started getty@tty5.service - Getty on tty5.
[  OK  ] Started getty@tty6.service - Getty on tty6.
[  OK  ] Started serial-getty@ttyS0.service - Serial Getty on ttyS0.
[  OK  ] Reached target getty.target - Login Prompts.
[  OK  ] Reached target multi-user.target - Multi-User System.
[  OK  ] Reached target graphical.target - Graphical Interface.
         Starting systemd-update-utmp-runle…- Record Runlevel Change in UTMP...
[  OK  ] Finished systemd-update-utmp-runle…e - Record Runlevel Change in UTMP.

Ubuntu 24.04.1 LTS localhost.localdomain ttyS0

localhost login:
```

To continue proceed to [Logging In](#logging-in).

### Cloud hypervisor

You can get the latest [Cloud Hypervisor](https://www.cloudhypervisor.org/)
release from the
[official repo](https://github.com/cloud-hypervisor/cloud-hypervisor/releases/latest).
Ie. to download v44.0 for amd64:

```sh
wget -O cloud-hypervisor \
    https://github.com/cloud-hypervisor/cloud-hypervisor/releases/download/v44.0/cloud-hypervisor-static
chmod u+x cloud-hypervisor
```

The updated current directory should look like:

```console
$ tree -L 1
.
├── bzImage
├── cloud-hypervisor
├── downloads
├── linux-amd64-fc.config
├── linux-amd64.config
├── rootfs.img
└── vmlinux

1 directory, 6 files
```

To launch the VM you can use:

```console
$ ./cloud-hypervisor --kernel bzImage --disk path=rootfs.img \
      --cpus boot=2 --memory size=4096M \
      --cmdline "console=ttyS0 root=/dev/vda rw" \
      --console off --serial tty \
      --vsock cid=42,socket=/tmp/vaccel.sock
[    0.000000] Linux version 6.1.132 (root@buildkitsandbox) (gcc (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0, GNU ld (GNU Binutils for Ubuntu) 2.42) #1 SMP PREEMPT_DYNAMIC Sun Mar 30 00:13:19 UTC 2025
[    0.000000] Command line: console=ttyS0 root=/dev/vda rw
[...]
[    0.582493] EXT4-fs (vda): mounted filesystem with ordered data mode. Quota mode: none.
[    0.583313] VFS: Mounted root (ext4 filesystem) on device 254:0.
[    0.584241] devtmpfs: mounted
[    0.585398] Freeing unused kernel image (initmem) memory: 2484K
[    0.586013] Write protecting the kernel read-only data: 20480k
[    0.588863] Freeing unused kernel image (text/rodata gap) memory: 2044K
[    0.591116] Freeing unused kernel image (rodata/data gap) memory: 1524K
[    0.591787] Run /sbin/init as init process
SELinux:  Could not open policy file <= /etc/selinux/targeted/policy/policy.33:  No such file or directory
[    0.623287] systemd[1]: systemd 255.4-1ubuntu8.5 running in system mode (+PAM +AUDIT +SELINUX +APPARMOR +IMA +SMACK +SECCOMP +GCRYPT -GNUTLS +OPENSSL +ACL +BLKID +CURL +ELFUTILS +FIDO2 +IDN2 -IDN +IPTC +KMOD +LIBCRYPTSETUP +LIBFDISK +PCRE2 -PWQUALITY +P11KIT +QRENCODE +TPM2 +BZIP2 +LZ4 +XZ +ZLIB +ZSTD -BPF_FRAMEWORK -XKBCOMMON +UTMP +SYSVINIT default-hierarchy=unified)
[    0.626523] systemd[1]: Detected virtualization kvm.
[    0.627092] systemd[1]: Detected architecture x86-64.

Welcome to Ubuntu 24.04.1 LTS!

[...]
[  OK  ] Started getty@tty1.service - Getty on tty1.
[  OK  ] Started getty@tty2.service - Getty on tty2.
[  OK  ] Started getty@tty3.service - Getty on tty3.
[  OK  ] Started getty@tty4.service - Getty on tty4.
[  OK  ] Started getty@tty5.service - Getty on tty5.
[  OK  ] Started getty@tty6.service - Getty on tty6.
[  OK  ] Started serial-getty@ttyS0.service - Serial Getty on ttyS0.
[  OK  ] Reached target getty.target - Login Prompts.
[  OK  ] Reached target multi-user.target - Multi-User System.
[  OK  ] Reached target graphical.target - Graphical Interface.
         Starting systemd-update-utmp-runle…- Record Runlevel Change in UTMP...
[  OK  ] Finished systemd-update-utmp-runle…e - Record Runlevel Change in UTMP.

Ubuntu 24.04.1 LTS localhost.localdomain ttyS0

localhost login:
```

To continue proceed to [Logging In](#logging-in).

### QEMU

To install [QEMU](https://www.qemu.org/) you can use your distribution's package
manager:

```sh
sudo apt install qemu
```

QEMU can emulate different machines. We will show how to boot with two common
machine options.

#### QEMU with PCI support

If no machine is provided, QEMU will emulate the default machine depending on
the platform architecture. For x86_64 this is a machine with PCI support.

To launch a QEMU VM with PCI support use:

```console
$ qemu-system-x86_64 -M pc,accel=kvm -cpu host \
      -nographic -vga none -nic none \
      -smp 2 -m 4096 \
      -kernel bzImage \
      -append "console=ttyS0 earlyprintk=ttyS0 root=/dev/vda rw " \
      -drive if=none,id=rootfs,file=rootfs.img,format=raw,cache=none \
      -device virtio-blk,drive=rootfs \
      -device vhost-vsock-pci,id=vhost-vsock-pci0,guest-cid=42
SeaBIOS (version rel-1.16.3-0-ga6ed6b701f0a-prebuilt.qemu.org)
Booting from ROM..
early console in extract_kernel
input_data: 0x00000000024c52c4
input_len: 0x00000000007949f9
output: 0x0000000001000000
output_len: 0x0000000001c1ceb8
kernel_total_size: 0x0000000001a2c000
needed_size: 0x0000000001e00000
trampoline_32bit: 0x0000000000000000
Physical KASLR using RDRAND RDTSC...
Virtual KASLR using RDRAND RDTSC...

Decompressing Linux... Parsing ELF... Performing relocations... done.
Booting the kernel (entry_offset: 0x0000000000000000).
[    0.000000] Linux version 6.1.132 (root@buildkitsandbox) (gcc (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0, GNU ld (GNU Binutils for Ubuntu) 2.42) #1 SMP PREEMPT_DYNAMIC Sun Mar 30 00:13:19 UTC 2025
[    0.000000] Command line: console=ttyS0 root=/dev/vda rw
[...]
[    0.582493] EXT4-fs (vda): mounted filesystem with ordered data mode. Quota mode: none.
[    0.583313] VFS: Mounted root (ext4 filesystem) on device 254:0.
[    0.584241] devtmpfs: mounted
[    0.585398] Freeing unused kernel image (initmem) memory: 2484K
[    0.586013] Write protecting the kernel read-only data: 20480k
[    0.588863] Freeing unused kernel image (text/rodata gap) memory: 2044K
[    0.591116] Freeing unused kernel image (rodata/data gap) memory: 1524K
[    0.591787] Run /sbin/init as init process
SELinux:  Could not open policy file <= /etc/selinux/targeted/policy/policy.33:  No such file or directory
[    0.623287] systemd[1]: systemd 255.4-1ubuntu8.5 running in system mode (+PAM +AUDIT +SELINUX +APPARMOR +IMA +SMACK +SECCOMP +GCRYPT -GNUTLS +OPENSSL +ACL +BLKID +CURL +ELFUTILS +FIDO2 +IDN2 -IDN +IPTC +KMOD +LIBCRYPTSETUP +LIBFDISK +PCRE2 -PWQUALITY +P11KIT +QRENCODE +TPM2 +BZIP2 +LZ4 +XZ +ZLIB +ZSTD -BPF_FRAMEWORK -XKBCOMMON +UTMP +SYSVINIT default-hierarchy=unified)
[    0.626523] systemd[1]: Detected virtualization kvm.
[    0.627092] systemd[1]: Detected architecture x86-64.

Welcome to Ubuntu 24.04.1 LTS!

[...]
[  OK  ] Started getty@tty1.service - Getty on tty1.
[  OK  ] Started getty@tty2.service - Getty on tty2.
[  OK  ] Started getty@tty3.service - Getty on tty3.
[  OK  ] Started getty@tty4.service - Getty on tty4.
[  OK  ] Started getty@tty5.service - Getty on tty5.
[  OK  ] Started getty@tty6.service - Getty on tty6.
[  OK  ] Started serial-getty@ttyS0.service - Serial Getty on ttyS0.
[  OK  ] Reached target getty.target - Login Prompts.
[  OK  ] Reached target multi-user.target - Multi-User System.
[  OK  ] Reached target graphical.target - Graphical Interface.
         Starting systemd-update-utmp-runle…- Record Runlevel Change in UTMP...
[  OK  ] Finished systemd-update-utmp-runle…e - Record Runlevel Change in UTMP.

Ubuntu 24.04.1 LTS localhost.localdomain ttyS0

localhost login:
```

To continue proceed to [Logging In](#logging-in).

#### QEMU microVM, noPCI

Current versions of QEMU provide a microVM machine with no PCI support, meant to
be used as a lightweight alternative to the default machine. This target aims to
provide and experience similar to Firecracker.

To launch a QEMU microVM (with no PCI support) use:

```console
$ qemu-system-x86_64 -M microvm,accel=kvm -cpu host \
      -nographic -vga none -nic none \
      -smp 2 -m 4096 \
      -kernel bzImage \
      -append "console=ttyS0 earlyprintk=ttyS0 root=/dev/vda rw " \
      -drive if=none,id=rootfs,file=rootfs.img,format=raw,cache=none \
      -device virtio-blk-device,drive=rootfs \
      -device vhost-vsock-device,id=vhost-vsock,guest-cid=42
SeaBIOS (version rel-1.16.3-0-ga6ed6b701f0a-prebuilt.qemu.org)
Booting from ROM..
early console in extract_kernel
input_data: 0x00000000024c52c4
input_len: 0x00000000007949f9
output: 0x0000000001000000
output_len: 0x0000000001c1ceb8
kernel_total_size: 0x0000000001a2c000
needed_size: 0x0000000001e00000
trampoline_32bit: 0x0000000000000000
Physical KASLR using RDRAND RDTSC...
Virtual KASLR using RDRAND RDTSC...

Decompressing Linux... Parsing ELF... Performing relocations... done.
Booting the kernel (entry_offset: 0x0000000000000000).
[    0.000000] Linux version 6.1.132 (root@buildkitsandbox) (gcc (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0, GNU ld (GNU Binutils for Ubuntu) 2.42) #1 SMP PREEMPT_DYNAMIC Sun Mar 30 00:13:19 UTC 2025
[    0.000000] Command line: console=ttyS0 earlyprintk=ttyS0 root=/dev/vda rw
[...]
[    0.203882] VFS: Mounted root (ext4 filesystem) on device 254:0.
[    0.205666] devtmpfs: mounted
[    0.206459] Freeing unused kernel image (initmem) memory: 2484K
[    0.207052] Write protecting the kernel read-only data: 20480k
[    0.208129] Freeing unused kernel image (text/rodata gap) memory: 2044K
[    0.209050] Freeing unused kernel image (rodata/data gap) memory: 1524K
[    0.209702] Run /sbin/init as init process
SELinux:  Could not open policy file <= /etc/selinux/targeted/policy/policy.33:  No such file or directory
[    0.316715] systemd[1]: systemd 255.4-1ubuntu8.5 running in system mode (+PAM +AUDIT +SELINUX +APPARMOR +IMA +SMAC)
[    0.319763] systemd[1]: Detected virtualization kvm.
[    0.320270] systemd[1]: Detected architecture x86-64.

Welcome to Ubuntu 24.04.1 LTS!

[...]
[  OK  ] Started getty@tty1.service - Getty on tty1.
[  OK  ] Started getty@tty2.service - Getty on tty2.
[  OK  ] Started getty@tty3.service - Getty on tty3.
[  OK  ] Started getty@tty4.service - Getty on tty4.
[  OK  ] Started getty@tty5.service - Getty on tty5.
[  OK  ] Started getty@tty6.service - Getty on tty6.
[  OK  ] Started serial-getty@ttyS0.service - Serial Getty on ttyS0.
[  OK  ] Reached target getty.target - Login Prompts.
[  OK  ] Reached target multi-user.target - Multi-User System.
[  OK  ] Reached target graphical.target - Graphical Interface.
         Starting systemd-update-utmp-runle…- Record Runlevel Change in UTMP...
[  OK  ] Finished systemd-update-utmp-runle…e - Record Runlevel Change in UTMP.

Ubuntu 24.04.1 LTS localhost.localdomain ttyS0

localhost login:
```

### Logging in

Since the provided image is meant for testing purposes the default user is
`root`. To log in use `root` (no password required). You should be greeted with:

```console
Welcome to Ubuntu 24.04.1 LTS (GNU/Linux 6.1.132 x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.

The programs included with the Ubuntu system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.

root@localhost:~#
```

You can verify all required libraries are installed by looking at
`/usr/local/lib/x86_64-linux-gnu`:

```console
# ls /usr/local/lib/x86_64-linux-gnu/
libmytestlib.so            libvaccel-noop.so.0        libvaccel-virtio.so
libvaccel-exec.so          libvaccel-noop.so.0.6.1    libvaccel-virtio.so.0
libvaccel-exec.so.0        libvaccel-python.so        libvaccel-virtio.so.0.1.0
libvaccel-exec.so.0.6.1    libvaccel-python.so.0      libvaccel.so
libvaccel-mbench.so        libvaccel-python.so.0.6.1  libvaccel.so.0
libvaccel-mbench.so.0      libvaccel-rpc.so           libvaccel.so.0.6.1
libvaccel-mbench.so.0.6.1  libvaccel-rpc.so.0         pkgconfig
libvaccel-noop.so          libvaccel-rpc.so.0.1.0
```

## Running the vAccel RPC agent

Before running a vAccel application on the guest, you need to first start the
vAccel RPC agent. Since the VM console should be open in the current terminal by
now, you will have to open a new terminal to execute the agent.

Depending on the VMM being used, you have to set a valid RPC address for the
agent. Firecracker and Cloud Hypervisor use a "hybrid" `unix` socket for vSock
communication, while QEMU expects a proper `vsock` socket.

To use `vaccel-rpc-agent` for the above Firecracker/Cloud Hypervisor setups use:

```sh
export VACCEL_RPC_ADDRESS="unix:///tmp/vaccel.sock_2048"
```

where `/tmp/vaccel.sock` is the VMM's vsock socket we have configured in the
previous steps.

For QEMU, the variable should be set to:

```sh
export VACCEL_RPC_ADDRESS="vsock://2:2048"
```

where `2` is the well-known vSock address of the host.

For both cases, `2048` is the port number we have configured in the previous
steps for the VMM.

Since the agent will instantiate the host vAccel, you also need to configure
vAccel in this step. You can configure vAccel by setting the related environment
variables - as you would do for a plugin - or you can use the
`vaccel-rpc-agent`'s CLI (preferred).

Since the 'NoOp' plugin is included with vAccel, we will use this as the
acceleration plugin for demonstration purposes.

To start a `vaccel-rpc-agent` with the vAccel `NoOp` plugin use:

```console
$ VACCEL_BOOTSTRAP_ENABLED=0 vaccel-rpc-agent \
      -a "${VACCEL_RPC_ADDRESS}" \
      --vaccel-config "plugins=libvaccel-noop.so,log_level=4"
2025.04.08-19:34:05.40 - <debug> Initializing vAccel
2025.04.08-19:34:05.40 - <info> vAccel 0.6.1-194-19056528
2025.04.08-19:34:05.40 - <debug> Config:
2025.04.08-19:34:05.40 - <debug>   plugins = libvaccel-noop.so
2025.04.08-19:34:05.40 - <debug>   log_level = debug
2025.04.08-19:34:05.40 - <debug>   log_file = (null)
2025.04.08-19:34:05.40 - <debug>   profiling_enabled = false
2025.04.08-19:34:05.40 - <debug>   version_ignore = false
2025.04.08-19:34:05.40 - <debug> Created top-level rundir: /run/user/1002/vaccel/j1Kwrv
2025.04.08-19:34:05.40 - <info> Registered plugin noop 0.6.1-194-19056528
2025.04.08-19:34:05.40 - <debug> Registered op noop from plugin noop
2025.04.08-19:34:05.40 - <debug> Registered op blas_sgemm from plugin noop
2025.04.08-19:34:05.40 - <debug> Registered op image_classify from plugin noop
2025.04.08-19:34:05.40 - <debug> Registered op image_detect from plugin noop
2025.04.08-19:34:05.40 - <debug> Registered op image_segment from plugin noop
2025.04.08-19:34:05.40 - <debug> Registered op image_pose from plugin noop
2025.04.08-19:34:05.40 - <debug> Registered op image_depth from plugin noop
2025.04.08-19:34:05.40 - <debug> Registered op exec from plugin noop
2025.04.08-19:34:05.40 - <debug> Registered op tf_session_load from plugin noop
2025.04.08-19:34:05.40 - <debug> Registered op tf_session_run from plugin noop
2025.04.08-19:34:05.40 - <debug> Registered op tf_session_delete from plugin noop
2025.04.08-19:34:05.40 - <debug> Registered op minmax from plugin noop
2025.04.08-19:34:05.40 - <debug> Registered op fpga_arraycopy from plugin noop
2025.04.08-19:34:05.40 - <debug> Registered op fpga_vectoradd from plugin noop
2025.04.08-19:34:05.40 - <debug> Registered op fpga_parallel from plugin noop
2025.04.08-19:34:05.40 - <debug> Registered op fpga_mmult from plugin noop
2025.04.08-19:34:05.40 - <debug> Registered op exec_with_resource from plugin noop
2025.04.08-19:34:05.40 - <debug> Registered op torch_jitload_forward from plugin noop
2025.04.08-19:34:05.40 - <debug> Registered op torch_sgemm from plugin noop
2025.04.08-19:34:05.40 - <debug> Registered op opencv from plugin noop
2025.04.08-19:34:05.40 - <debug> Registered op tflite_session_load from plugin noop
2025.04.08-19:34:05.40 - <debug> Registered op tflite_session_run from plugin noop
2025.04.08-19:34:05.40 - <debug> Registered op tflite_session_delete from plugin noop
2025.04.08-19:34:05.40 - <debug> Loaded plugin noop from libvaccel-noop.so
[2025-04-08T19:34:05Z INFO  ttrpc::sync::server] server listen started
[2025-04-08T19:34:05Z INFO  ttrpc::sync::server] server started
[2025-04-08T19:34:05Z INFO  vaccel_rpc_agent] vAccel RPC agent started
[2025-04-08T19:34:05Z INFO  vaccel_rpc_agent] Listening on 'vsock://2:2048', press Ctrl+C to exit
```

## Running the application on the guest

With the vAccel RPC agent running, you are ready to execute the application in
the VM.

Switching back to the initial terminal, you need to first configure the RPC
address that will be used by the plugin:

```sh
export VACCEL_RPC_ADDRESS="vsock://2:2048"
```

where `2` is the well-known vSock address of the host and this address is common
for all the VMMs we have setup above.

Next, you have to configure vAccel to use the plugin:

```sh
export VACCEL_PLUGINS=libvaccel-rpc.so
```

Optionally, to get debug output:

```sh
export VACCEL_LOG_LEVEL=4
```

Finally, you can run an image classification example with:

```console
# classify /usr/local/share/vaccel/images/example.jpg 1
2025.04.08-19:34:48.28 - <debug> Initializing vAccel
2025.04.08-19:34:48.28 - <info> vAccel 0.6.1-194-19056528
2025.04.08-19:34:48.28 - <debug> Config:
2025.04.08-19:34:48.28 - <debug>   plugins = libvaccel-rpc.so
2025.04.08-19:34:48.28 - <debug>   log_level = debug
2025.04.08-19:34:48.28 - <debug>   log_file = (null)
2025.04.08-19:34:48.28 - <debug>   profiling_enabled = false
2025.04.08-19:34:48.28 - <debug>   version_ignore = false
2025.04.08-19:34:48.28 - <debug> Created top-level rundir: /run/user/0/vaccel/JE4UiS
2025.04.08-19:34:48.30 - <info> Registered plugin rpc 0.1.0-36-bbffdae6
2025.04.08-19:34:48.30 - <debug> rpc is a VirtIO module
2025.04.08-19:34:48.30 - <debug> Registered op blas_sgemm from plugin rpc
2025.04.08-19:34:48.30 - <debug> Registered op image_classify from plugin rpc
2025.04.08-19:34:48.30 - <debug> Registered op image_detect from plugin rpc
2025.04.08-19:34:48.30 - <debug> Registered op image_segment from plugin rpc
2025.04.08-19:34:48.30 - <debug> Registered op image_depth from plugin rpc
2025.04.08-19:34:48.30 - <debug> Registered op image_pose from plugin rpc
2025.04.08-19:34:48.30 - <debug> Registered op tflite_session_load from plugin rpc
2025.04.08-19:34:48.30 - <debug> Registered op tflite_session_delete from plugin rpc
2025.04.08-19:34:48.30 - <debug> Registered op tflite_session_run from plugin rpc
2025.04.08-19:34:48.30 - <debug> Registered op minmax from plugin rpc
2025.04.08-19:34:48.30 - <debug> Registered op fpga_arraycopy from plugin rpc
2025.04.08-19:34:48.30 - <debug> Registered op fpga_mmult from plugin rpc
2025.04.08-19:34:48.30 - <debug> Registered op fpga_vectoradd from plugin rpc
2025.04.08-19:34:48.30 - <debug> Registered op fpga_parallel from plugin rpc
2025.04.08-19:34:48.30 - <debug> Registered op exec from plugin rpc
2025.04.08-19:34:48.30 - <debug> Registered op exec_with_resource from plugin rpc
2025.04.08-19:34:48.30 - <debug> Registered op torch_jitload_forward from plugin rpc
2025.04.08-19:34:48.30 - <debug> Registered op opencv from plugin rpc
2025.04.08-19:34:48.30 - <debug> Registered op tf_session_load from plugin rpc
2025.04.08-19:34:48.30 - <debug> Registered op tf_session_delete from plugin rpc
2025.04.08-19:34:48.30 - <debug> Registered op tf_session_run from plugin rpc
2025.04.08-19:34:48.30 - <debug> Loaded plugin rpc from libvaccel-rpc.so
2025.04.08-19:34:48.31 - <debug> [rpc] Initializing new remote session
2025.04.08-19:34:48.34 - <debug> [rpc] Initialized remote session 1
2025.04.08-19:34:48.34 - <debug> New rundir for session 1: /run/user/0/vaccel/JE4UiS/session.1
2025.04.08-19:34:48.34 - <debug> Initialized session 1 with remote (id: 1)
Initialized session with id: 1
2025.04.08-19:34:48.34 - <debug> session:1 Looking for plugin implementing VACCEL_OP_IMAGE_CLASSIFY
2025.04.08-19:34:48.34 - <debug> Returning func from hint plugin rpc
2025.04.08-19:34:48.34 - <debug> Found implementation in rpc plugin
classification tags: This is a dummy classification tag!
classification imagename: This is a dummy imgname!
2025.04.08-19:34:48.35 - <debug> [rpc] Releasing remote session 1
2025.04.08-19:34:48.35 - <debug> Released session 1
2025.04.08-19:34:48.35 - <debug> Cleaning up vAccel
2025.04.08-19:34:48.35 - <debug> Cleaning up sessions
2025.04.08-19:34:48.35 - <debug> Cleaning up resources
2025.04.08-19:34:48.35 - <debug> Cleaning up plugins
2025.04.08-19:34:48.35 - <debug> Unregistered plugin rpc
```

In the other terminal, where the vAccel RPC agent is running, you should also
see the corresponding host vAccel output:

```console
2025.04.08-19:34:48.36 - <debug> New rundir for session 1: /run/user/1002/vaccel/j1Kwrv/session.1
2025.04.08-19:34:48.36 - <debug> Initialized session 1
[2025-04-08T19:34:48Z INFO  vaccel_rpc_agent::session] Created session 1
[2025-04-08T19:34:48Z INFO  vaccel_rpc_agent::ops::genop] Genop session 1
2025.04.08-19:34:48.37 - <debug> session:1 Looking for plugin implementing VACCEL_OP_IMAGE_CLASSIFY
2025.04.08-19:34:48.37 - <debug> Returning func from hint plugin noop
2025.04.08-19:34:48.37 - <debug> Found implementation in noop plugin
2025.04.08-19:34:48.37 - <debug> [noop] Calling Image classification for session 1
2025.04.08-19:34:48.37 - <debug> [noop] Dumping arguments for Image classification:
2025.04.08-19:34:48.37 - <debug> [noop] model: (null)
2025.04.08-19:34:48.37 - <debug> [noop] len_img: 79281
2025.04.08-19:34:48.37 - <debug> [noop] len_out_text: 512
2025.04.08-19:34:48.37 - <debug> [noop] len_out_imgname: 512
2025.04.08-19:34:48.37 - <debug> [noop] will return a dummy result
2025.04.08-19:34:48.37 - <debug> [noop] will return a dummy result
2025.04.08-19:34:48.38 - <debug> Released session 1
[2025-04-08T19:34:48Z INFO  vaccel_rpc_agent::session] Destroyed session 1
```

If you compare the application output with the
[native execution case](../getting-started/running-the-examples.md#classify-noop-debug)
ignoring the vAccel log messages, you will notice that it is identical:

```console
# classify /usr/local/share/vaccel/images/example.jpg 1
...
Initialized session with id: 1
...
classification tags: This is a dummy classification tag!
classification imagename: This is a dummy imgname!
...
```

The debug log messages reveal that in the native execution case the `NoOp`
plugin is used directly:

```console
$ classify /usr/local/share/vaccel/images/example.jpg 1
2025.04.03-15:44:04.61 - <debug> Initializing vAccel
2025.04.03-15:44:04.61 - <info> vAccel 0.6.1-194-19056528
2025.04.03-15:44:04.61 - <debug> Config:
2025.04.03-15:44:04.61 - <debug>   plugins = libvaccel-noop.so
2025.04.03-15:44:04.61 - <debug>   log_level = debug
2025.04.03-15:44:04.61 - <debug>   log_file = (null)
2025.04.03-15:44:04.61 - <debug>   profiling_enabled = false
2025.04.03-15:44:04.61 - <debug>   version_ignore = false
2025.04.03-15:44:04.61 - <debug> Created top-level rundir: /run/user/1002/vaccel/VC0Gxz
2025.04.03-15:44:04.61 - <info> Registered plugin noop 0.6.1-194-19056528
...
2025.04.03-15:44:04.61 - <debug> Loaded plugin noop from libvaccel-noop.so
...
2025.04.03-15:44:04.62 - <debug> Returning func from hint plugin noop
2025.04.03-15:44:04.62 - <debug> Found implementation in noop plugin
2025.04.03-15:44:04.62 - <debug> [noop] Calling Image classification for session 1
2025.04.03-15:44:04.62 - <debug> [noop] Dumping arguments for Image classification:
2025.04.03-15:44:04.62 - <debug> [noop] model: (null)
2025.04.03-15:44:04.62 - <debug> [noop] len_img: 79281
2025.04.03-15:44:04.62 - <debug> [noop] len_out_text: 512
2025.04.03-15:44:04.62 - <debug> [noop] len_out_imgname: 512
2025.04.03-15:44:04.62 - <debug> [noop] will return a dummy result
2025.04.03-15:44:04.62 - <debug> [noop] will return a dummy result
```

whereas in the VM case, the `RPC` plugin is used on the guest:

```console
# classify /usr/local/share/vaccel/images/example.jpg 1
2025.04.08-19:34:48.28 - <debug> Initializing vAccel
2025.04.08-19:34:48.28 - <info> vAccel 0.6.1-194-19056528
2025.04.08-19:34:48.28 - <debug> Config:
2025.04.08-19:34:48.28 - <debug>   plugins = libvaccel-rpc.so
2025.04.08-19:34:48.28 - <debug>   log_level = debug
2025.04.08-19:34:48.28 - <debug>   log_file = (null)
2025.04.08-19:34:48.28 - <debug>   profiling_enabled = false
2025.04.08-19:34:48.28 - <debug>   version_ignore = false
2025.04.08-19:34:48.28 - <debug> Created top-level rundir: /run/user/0/vaccel/JE4UiS
2025.04.08-19:34:48.30 - <info> Registered plugin rpc 0.1.0-36-bbffdae6
...
2025.04.08-19:34:48.30 - <debug> Loaded plugin rpc from libvaccel-rpc.so
2025.04.08-19:34:48.31 - <debug> [rpc] Initializing new remote session
2025.04.08-19:34:48.34 - <debug> [rpc] Initialized remote session 1
...
2025.04.08-19:34:48.34 - <debug> Returning func from hint plugin rpc
2025.04.08-19:34:48.34 - <debug> Found implementation in rpc plugin
...
2025.04.08-19:34:48.35 - <debug> [rpc] Releasing remote session 1
...
```

while the `NoOp` plugin is used on the host:

```console
2025.04.08-19:34:05.40 - <debug> Initializing vAccel
2025.04.08-19:34:05.40 - <info> vAccel 0.6.1-194-19056528
2025.04.08-19:34:05.40 - <debug> Config:
2025.04.08-19:34:05.40 - <debug>   plugins = libvaccel-noop.so
2025.04.08-19:34:05.40 - <debug>   log_level = debug
2025.04.08-19:34:05.40 - <debug>   log_file = (null)
2025.04.08-19:34:05.40 - <debug>   profiling_enabled = false
2025.04.08-19:34:05.40 - <debug>   version_ignore = false
2025.04.08-19:34:05.40 - <debug> Created top-level rundir: /run/user/1002/vaccel/j1Kwrv
2025.04.08-19:34:05.40 - <info> Registered plugin noop 0.6.1-194-19056528
...
2025.04.08-19:34:05.40 - <debug> Loaded plugin noop from libvaccel-noop.so
...
2025.04.08-19:34:48.37 - <debug> Returning func from hint plugin noop
2025.04.08-19:34:48.37 - <debug> Found implementation in noop plugin
2025.04.08-19:34:48.37 - <debug> [noop] Calling Image classification for session 1
2025.04.08-19:34:48.37 - <debug> [noop] Dumping arguments for Image classification:
2025.04.08-19:34:48.37 - <debug> [noop] model: (null)
2025.04.08-19:34:48.37 - <debug> [noop] len_img: 79281
2025.04.08-19:34:48.37 - <debug> [noop] len_out_text: 512
2025.04.08-19:34:48.37 - <debug> [noop] len_out_imgname: 512
2025.04.08-19:34:48.37 - <debug> [noop] will return a dummy result
2025.04.08-19:34:48.37 - <debug> [noop] will return a dummy result
...
```
