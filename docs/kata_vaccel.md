# Kata-containers with vAccel

In this post, we will be going through the steps to build our downstream branch
for kata-containers with vAccel from source, both for amd64 and arm64
architectures.

### Install requirements

To build Kata Containers we need to install Rust v1.58.1, Go v1.18.0, Docker
and some apt/snap packages. The specific versions may change, so make sure to
check the [versions
database](https://github.com/kata-containers/kata-containers/blob/main/versions.yaml).

#### Apt/Snap Packages

We need to install `gcc`, `make` and `yq v3`. `containerd` and `runc` are installed by the Docker install script, in the following steps.

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install gcc make snapd bc -y
sudo snap install yq --channel=v3/stable
```

#### Rust (version 1.58.1)

We will use `rustup` to install and set Rust 1.58.1 as our default toolchain:

```bash
down_dir=$(mktemp -d)
pushd $down_dir
wget -q https://static.rust-lang.org/rustup/dist/$(uname -p)-unknown-linux-gnu/rustup-init
sudo chmod +x rustup-init
./rustup-init -q -y --default-toolchain 1.58.1
source $HOME/.cargo/env
popd
rm -rf $down_dir
```

#### Go (version 1.18)

We will download the appropriate Go binaries and add them to the `PATH` environment variable:

```bash
down_dir=$(mktemp -d)
pushd $down_dir
wget -q https://go.dev/dl/go1.18.linux-$(dpkg --print-architecture).tar.gz
sudo mkdir -p /usr/local/go1.18
sudo tar -C /usr/local/go1.18 -xzf go1.18.linux-$(dpkg --print-architecture).tar.gz
echo 'export PATH=$PATH:/usr/local/go1.18/go/bin' >> $HOME/.profile
source $HOME/.profile
popd
rm -rf $down_dir
```

#### Docker

We will install Docker using the provided convenience script:

```bash
sudo apt-get remove docker docker-engine docker.io containerd runc -y > /dev/null 2>&1
sudo rm -rf /var/lib/docker/
down_dir=$(mktemp -d)
pushd $down_dir
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
popd
rm -rf $down_dir
```

### Build Kata components

#### Build kata-runtime

First, we need to set the correct Go environment variables:

```bash
export PATH=$PATH:$(go env GOPATH)/bin && \
  export GOPATH=$(go env GOPATH) && \
  export GO111MODULE=off
```

We will use `go get` to download kata-containers source code:

```bash
go get -d -u github.com/kata-containers/kata-containers
```

Checkout our downstream branch:

```bash
cd $GOPATH/src/github.com/kata-containers/kata-containers
git remote add nbfc https://github.com/nubificus/kata-containers
git fetch -u nbfc
git checkout vaccel-v3.0
```

We are now ready to build the `kata-runtime`:

```bash
pushd $GOPATH/src/github.com/kata-containers/kata-containers/src/runtime
export GO111MODULE=on
export PREFIX=/opt/kata
make
popd
```

To install the binaries to a specific path (say `/opt/kata`) we need to specify
the `PREFIX` environment variable prior to installing:

```bash
pushd $GOPATH/src/github.com/kata-containers/kata-containers/src/runtime
export PREFIX=/opt/kata
sudo -E PATH=$PATH -E PREFIX=$PREFIX make install
popd
```

Kata binaries are now installed in `/opt/kata/bin` and configs are installed in
`/opt/kata/share/defaults/kata-containers/`.

It is recommended you add a symbolic link to /opt/kata/bin/kata-runtime and
/opt/kata/bin/containerd-shim-kata-v2 in order for containerd to reach these
binaries from the default system `PATH`.

```bash
sudo ln -s /opt/kata/bin/kata-runtime /usr/local/bin
sudo ln -s /opt/kata/bin/containerd-shim-kata-v2 /usr/local/bin
```

#### Create a rootfs

We can use either a rootfs or initrd image to launch Kata Containers with QEMU.
However, AWS Firecracker does not work with initrd images, so we will be using a
rootfs image for Kata with Firecracker.

Create the rootfs base image:

```bash
export ROOTFS_DIR=${GOPATH}/src/github.com/kata-containers/kata-containers/tools/osbuilder/rootfs-builder/rootfs
cd $GOPATH/src/github.com/kata-containers/kata-containers/tools/osbuilder/rootfs-builder
# you may change the distro (in this case we used ubuntu). to get supported distros list, run ./rootfs.sh -l
script -fec 'sudo -E GOPATH=$GOPATH AGENT_INIT=yes USE_DOCKER=true ./rootfs.sh ubuntu'
```

**Note for arm64**:

We noticed that in some instances the kata-agent compilation failed.
A possible workaround was to remove the USE_DOCKER variable. This requires `qemu-img` command to be available on your system.
You can install it with `sudo apt install -y qemu-utils`.

```bash
export ROOTFS_DIR="${GOPATH}/src/github.com/kata-containers/kata-containers/tools/osbuilder/rootfs-builder/rootfs-ubuntu"
sudo rm -rf ${ROOTFS_DIR}
cd $GOPATH/src/github.com/kata-containers/kata-containers/tools/osbuilder/rootfs-builder
script -fec 'sudo -E GOPATH=$GOPATH AGENT_INIT=yes ./rootfs.sh ubuntu'
```

Build a kata rootfs image:

```bash
cd $GOPATH/src/github.com/kata-containers/kata-containers/tools/osbuilder/image-builder && \
  script -fec 'sudo -E USE_DOCKER=true -E AGENT_INIT=yes ./image_builder.sh ${ROOTFS_DIR}'
```

Install the kata rootfs image:

```bash
export PREFIX=/opt/kata
commit=$(git log --format=%h -1 HEAD) && \
  date=$(date +%Y-%m-%d-%T.%N%z) && \
  image="kata-containers-${date}-${commit}" && \
  sudo install -o root -g root -m 0640 -D kata-containers.img "$PREFIX/share/kata-containers/${image}" && \
  (cd $PREFIX/share/kata-containers && sudo ln -sf "$image" kata-containers.img)
```

#### Build Kata Containers kernel

First, we need some additional packages to build the kernel:

```bash
sudo apt install -y libelf-dev bison flex
```

Setup the kernel source code:

```bash
cd $GOPATH/src/github.com/kata-containers/kata-containers/tools/packaging/kernel
./build-kernel.sh -d setup
```

Build the kernel:

```bash
./build-kernel.sh -d build
```

Install the kernel in the default path for Kata:

```bash
export PREFIX=/opt/kata
sudo -E PATH=$PATH -E PREFIX=$PREFIX ./build-kernel.sh -d install
```

**Note**:

We noticed that in some instances the installation or build process failed with the following error: `ERROR: path to kernel does not exist, use build-kernel.sh setup`. We mitigated this problem by specifying the version:

```bash
./build-kernel.sh -d -v 5.15.26 build
export PREFIX=/opt/kata
sudo -E PATH=$PATH -E PREFIX=$PREFIX ./build-kernel.sh -d -v 5.15.26 install
```

At this point we have succesfully built all the Kata components. All the binaries we built are stored under the `/opt/kata/bin` dir:

```bash
$ ls -l /opt/kata/bin/
total 142296
-rwxr-xr-x 1 root root 50919312 Mar  25 15:32 containerd-shim-kata-v2
-rwxr-xr-x 1 root root    16691 Mar  25 15:32 kata-collect-data.sh
-rwxr-xr-x 1 root root 42093616 Mar  25 15:32 kata-monitor
-rwxr-xr-x 1 root root 52673784 Mar  25 15:32 kata-runtime
```

The rootfs image, the initrd image and the kernel are stored under the `/opt/kata/share/defaults/kata-containers` dir:

```bash
$ ls -l /opt/kata/share/kata-containers/
total 221972
-rw-r--r-- 1 root root     72480 Μαρ  25 15:51 config-5.15.26
-rw-r----- 1 root root 134217728 Μαρ  25 15:41 kata-containers-2022-03-25-15:41:55.534872004+0200-486322a0
lrwxrwxrwx 1 root root        59 Μαρ  25 15:41 kata-containers.img -> kata-containers-2022-03-25-15:41:55.534872004+0200-486322a0
-rw-r----- 1 root root  27627256 Μαρ  24 14:43 kata-containers-initrd-2022-03-24-14:43:59.501993241+0200-853dd98b
-rw-r----- 1 root root  27626874 Μαρ  25 15:42 kata-containers-initrd-2022-03-25-15:42:28.034074480+0200-486322a0
lrwxrwxrwx 1 root root        66 Μαρ  25 15:42 kata-containers-initrd.img -> kata-containers-initrd-2022-03-25-15:42:28.034074480+0200-486322a0
-rw-r--r-- 1 root root  38736168 Μαρ  25 15:51 vmlinux-5.15.26-90
lrwxrwxrwx 1 root root        18 Μαρ  25 15:51 vmlinux.container -> vmlinux-5.15.26-90
-rw-r--r-- 1 root root   5795664 Μαρ  25 15:51 vmlinuz-5.15.26-90
lrwxrwxrwx 1 root root        18 Μαρ  25 15:51 vmlinuz.container -> vmlinuz-5.15.26-90
```

The configuration files are stored under the `/opt/kata/share/defaults/kata-containers` dir:

```bash
ls -l /opt/kata/share/defaults/kata-containers
total 72
-rw-r--r-- 1 root root  9717 Μαρ  25 15:32 configuration-acrn.toml
-rw-r--r-- 1 root root 13535 Μαρ  25 15:32 configuration-clh.toml
-rw-r--r-- 1 root root 15364 Μαρ  25 15:32 configuration-fc.toml
-rw-r--r-- 1 root root 25701 Μαρ  25 15:32 configuration-qemu.toml
lrwxrwxrwx 1 root root    23 Μαρ  25 15:32 configuration.toml -> configuration-qemu.toml
```

#### Build Firecracker

Kata Containers support AWS Firecracker v1.1.0. To build Firecracker, we will
clone the Github repo and checkout to the 1.1.0 version:

```bash
git clone https://github.com/firecracker-microvm/firecracker.git -b v1.1.0 --depth 1 &&\
  cd firecracker &&\
  git submodule update --init
```

Now we can build the binaries:

**Note** AWS Firecracker uses docker to build the image, so make sure your user
can access the docker daemon, or just run with sudo.

```bash
sudo ./tools/devtool -y build --release
toolchain="$(uname -m)-unknown-linux-musl"
sudo cp build/cargo_target/${toolchain}/release/firecracker /opt/kata/bin/firecracker &&\
sudo cp build/cargo_target/${toolchain}/release/jailer /opt/kata/bin/jailer
```

#### devmapper snapshotter

AWS Firecracker requires a block device as the backing store for a VM. To interact with containerd and kata we use the devmapper snapshotter. To check support for your containerd installation, you can run:

```bash
ctr plugins ls |grep devmapper
```

if the output of the above command is:

```bash
io.containerd.snapshotter.v1    devmapper                linux/amd64    ok
```

then you can skip this section and move on to [Configure Kata Containers to use Firecracker](#configure-kata-containers-to-use-firecracker)

If the output of the above command is:

```bash
io.containerd.snapshotter.v1    devmapper                linux/amd64    error
```

then we need to setup devmapper snapshotter. Based on a [very useful
guide](https://docs.docker.com/storage/storagedriver/device-mapper-driver/)
from docker, we can set it up using the following scripts:

```bash
#!/bin/bash
set -ex

DATA_DIR=/var/lib/containerd/io.containerd.snapshotter.v1.devmapper
POOL_NAME=containerd-pool

mkdir -p ${DATA_DIR}

# Create data file
sudo touch "${DATA_DIR}/data"
sudo truncate -s 100G "${DATA_DIR}/data"

# Create metadata file
sudo touch "${DATA_DIR}/meta"
sudo truncate -s 10G "${DATA_DIR}/meta"

# Allocate loop devices
DATA_DEV=$(sudo losetup --find --show "${DATA_DIR}/data")
META_DEV=$(sudo losetup --find --show "${DATA_DIR}/meta")

# Define thin-pool parameters.
# See https://www.kernel.org/doc/Documentation/device-mapper/thin-provisioning.txt for details.
SECTOR_SIZE=512
DATA_SIZE="$(sudo blockdev --getsize64 -q ${DATA_DEV})"
LENGTH_IN_SECTORS=$(bc <<< "${DATA_SIZE}/${SECTOR_SIZE}")
DATA_BLOCK_SIZE=128
LOW_WATER_MARK=32768

# Create a thin-pool device
sudo dmsetup create "${POOL_NAME}" \
    --table "0 ${LENGTH_IN_SECTORS} thin-pool ${META_DEV} ${DATA_DEV} ${DATA_BLOCK_SIZE} ${LOW_WATER_MARK}"

cat << EOF
#
# Add this to your config.toml configuration file and restart containerd daemon
#
[plugins]
  [plugins.devmapper]
    pool_name = "${POOL_NAME}"
    root_path = "${DATA_DIR}"
    base_image_size = "10GB"
    discard_blocks = true
EOF
```

Make it executable and run it:

```bash
sudo chmod +x ~/scripts/devmapper/create.sh && \
  cd ~/scripts/devmapper/ && \
  sudo ./create.sh
```

Now, we can add the devmapper configuration provided from the script to `/etc/containerd/config.toml` and restart containerd.

```bash
sudo systemctl restart containerd
```

We can use `dmsetup` to verify that the thin-pool was created successfully. We should also check that devmapper is registered and running:

```bash
sudo dmsetup ls
# devpool (253:0)
sudo ctr plugins ls | grep devmapper
# io.containerd.snapshotter.v1    devmapper                linux/amd64    ok
```

This script needs to be run only once, while setting up the devmapper snapshotter for containerd. Afterwards, make sure that on each reboot, the thin-pool is initialized from the same data dir. Otherwise, all the fetched containers (or the ones that you’ve created) will be re-initialized. A simple script that re-creates the thin-pool from the same data dir is shown below:

```bash
#!/bin/bash
set -ex

DATA_DIR=/var/lib/containerd/io.containerd.snapshotter.v1.devmapper
POOL_NAME=containerd-pool

# Allocate loop devices
DATA_DEV=$(sudo losetup --find --show "${DATA_DIR}/data")
META_DEV=$(sudo losetup --find --show "${DATA_DIR}/meta")

# Define thin-pool parameters.
# See https://www.kernel.org/doc/Documentation/device-mapper/thin-provisioning.txt for details.
SECTOR_SIZE=512
DATA_SIZE="$(sudo blockdev --getsize64 -q ${DATA_DEV})"
LENGTH_IN_SECTORS=$(bc <<< "${DATA_SIZE}/${SECTOR_SIZE}")
DATA_BLOCK_SIZE=128
LOW_WATER_MARK=32768

# Create a thin-pool device
sudo dmsetup create "${POOL_NAME}" \
    --table "0 ${LENGTH_IN_SECTORS} thin-pool ${META_DEV} ${DATA_DEV} ${DATA_BLOCK_SIZE} ${LOW_WATER_MARK}"
```

We can create a systemd service to run the above script on each reboot:

```bash
sudo nano /lib/systemd/system/devmapper_reload.service
```

The service file:

```bash
[Unit]
Description=Devmapper reload script

[Service]
ExecStart=/path/to/script/reload.sh

[Install]
WantedBy=multi-user.target
```

Enable the newly created service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable devmapper_reload.service
sudo systemctl start devmapper_reload.service
```

#### Configure Kata Containers to use Firecracker

Next, we need to install the Kata Containers-Firecracker configuration file. We
will use this file to configure Kata Containers to use the rootfs image we
built [previously](#create-a-rootfs).

```bash
sudo mkdir -p /opt/kata/configs
sudo install -o root -g root -m 0640 /opt/kata/share/defaults/kata-containers/configuration-fc-vaccel.toml /opt/kata/configs
sudo sed -i 's/^\(initrd =.*\)/# \1/g' /opt/kata/configs/configuration-fc-vaccel.toml
# enable seccomp
sudo sed -i '/^disable_guest_seccomp/ s/true/false/' /opt/kata/configs/configuration-fc-vaccel.toml
```

Make sure that /opt/kata/configs/configuration-fc-vaccel.toml has an image entry pointing to the rootfs we created:

```bash
17   | image = "/opt/kata/share/kata-containers/kata-containers.img"
```

#### Configure containerd

Next, we need to configure containerd. Add a file in your path (eg. `/usr/local/bin/containerd-shim-kata-fc-vaccel-v2`) with the following contents:

```bash
#!/bin/bash
KATA_CONF_FILE=/opt/kata/configs/configuration-fc-vaccel.toml /usr/local/bin/containerd-shim-kata-v2 $@
```

Make it executable:

```bash
sudo chmod +x /usr/local/bin/containerd-shim-kata-fc-vaccel-v2
```

Add the relevant section in containerd’s config.toml file (`/etc/containerd/config.toml`):

```toml
[plugins.cri.containerd.runtimes]
  [plugins.cri.containerd.runtimes.kata-fc-vaccel]
    runtime_type = "io.containerd.kata-fc-vaccel.v2"
```

Restart containerd:

```bash
sudo systemctl restart containerd
```

#### Verify the installation

We are now ready to launch a container using Kata-vaccel with Firecracker to verify that everything worked:

```bash
sudo ctr images pull --snapshotter devmapper docker.io/library/ubuntu:latest
sudo ctr run --snapshotter devmapper --runtime io.containerd.run.kata-fc-vaccel.v2 -t --rm docker.io/library/ubuntu:latest ubuntu-kata-fc-test uname -a
```

You should see the `vaccelrt-agent` running alongside the containerd process.

### Install vAccel components

Before we proceed to run our first vAccel enabled kata container, we need to install the required vAccel components:

```bash
down_dir=$(mktemp -d)
pushd $down_dir
wget -q https://s3.nbfc.io/nbfc-assets/github/vaccelrt/master/x86_64/Release-deb/vaccel-0.5.0-Linux.deb
sudo dpkg -i vaccel-0.5.0-Linux.deb
wget -q https://s3.nbfc.io/nbfc-assets/github/vaccelrt/agent/main/x86_64/Release-deb/vaccelrt-agent-0.3.0-Linux.deb
sudo dpkg -i vaccelrt-agent-0.3.0-Linux.deb
popd
rm -rf $down_dir
```

### Run a vAccel-enabled kata container

To run a vAccel enabled kata container, first, you have to get a container
image with vaccel installed. We built one with docker, based on the following
container image file:

```Dockerfile
FROM ubuntu:20.04

ENV DEBIAN_FRONTEND="noninteractive"

RUN apt-get update && apt-get install -y wget unzip && apt-get clean

# Install vAccelrt core library
RUN wget https://s3.nbfc.io/nbfc-assets/github/vaccelrt/master/x86_64/Release-deb/vaccel-0.5.0-Linux.deb && dpkg -i vaccel-0.5.0-Linux.deb

# Install the vsock plugin
RUN wget https://s3.nbfc.io/nbfc-assets/github/vaccelrt/plugins/vsock/master/x86_64/Release-deb/vaccelrt-plugin-vsock-0.1.0-Linux.deb && dpkg -i vaccelrt-plugin-vsock-0.1.0-Linux.deb

# Set some env variables
ENV LD_LIBRARY_PATH=/usr/local/lib
ENV VACCEL_BACKENDS=/usr/local/lib/libvaccel-vsock.so 

# This is the default value, no need to set it
# Also, this value is passed on from the Kata runtime
#ENV VACCEL_VSOCK=vsock://2:2048

# Uncomment for debug messages
#ENV VACCEL_DEBUG_LEVEL=4

CMD ["sleep", "infinity"]
```

Build it, or pull a pre-built one:

```console
$ sudo ctr image pull --snapshotter devmapper docker.io/nubificus/vaccel-app-container:x86_64
docker.io/nubificus/vaccel-app-container:x86_64:                                  resolved       |++++++++++++++++++++++++++++++++++++++| 
manifest-sha256:60c94495bfdf0bdcceaab4fe20fa1b427df25ddb5e6ad107d249e91a948a7bed: done           |++++++++++++++++++++++++++++++++++++++| 
config-sha256:1bf757ff35444f01a96f9481b61cf82a0ced9afe53e37e2a04e1f3d943b4d241:   done           |++++++++++++++++++++++++++++++++++++++| 
layer-sha256:7a8454f39a31d19d7b1b497aa5dea0f717605b93fc5e9d10405f1a04cecb6a88:    exists         |++++++++++++++++++++++++++++++++++++++| 
layer-sha256:db0a0fb32697f17998cf1e72c2d38a41d13c79effa25ee9a4cac3870bc4980c0:    exists         |++++++++++++++++++++++++++++++++++++++| 
layer-sha256:45dd8fb4f524a0182c1b79769dd6a2ee05eaee8b095b4af343f324c699848fb7:    exists         |++++++++++++++++++++++++++++++++++++++| 
layer-sha256:846c0b181fff0c667d9444f8378e8fcfa13116da8d308bf21673f7e4bea8d580:    exists         |++++++++++++++++++++++++++++++++++++++| 
elapsed: 2.7 s                                                                    total:  1.1 Ki (430.0 B/s)                                       
unpacking linux/amd64 sha256:60c94495bfdf0bdcceaab4fe20fa1b427df25ddb5e6ad107d249e91a948a7bed...
done
```

Finally, run the container with the `kata-fc-vaccel` runtime using the
following commnad:

```sh
sudo ctr run --snapshotter devmapper --runtime io.containerd.run.kata-fc-vaccel.v2 -t --rm docker.io/nubificus/vaccel-app-container:x86_64 ubuntu-kata-fc-vaccel /bin/bash
```

You should be presented with the prompt of the container. Then, run the vaccel
classify example, using an image from the vAccel release:

```sh
classify /usr/local/share/images/example.jpg 1
```

The full output is shown below:

```console
$ sudo ctr run --snapshotter devmapper --runtime io.containerd.run.kata-fc-vaccel.v2 -t --rm docker.io/nubificus/vaccel-app-container:x86_64 ubuntu-kata-fc-vaccel /bin/bash
root@clr-5746603866294b7885b6f2a30c04c7b7:/# classify /usr/local/share/images/example.jpg 1
Initialized session with id: 1
Image size: 79281B
classification tags: 99.902% banana
```

If you inspect the host while the container is running, you can see the vAccelrt agent running, bound to the specific container instance:

```console
$ ps -fe |grep ubuntu-kata-fc
root      983620  566482  0 18:14 pts/16   00:00:00 ctr run --snapshotter devmapper --runtime io.containerd.run.kata-fc-vaccel.v2 -t --rm docker.io/nubificus/vaccel-app-container:x86_64 ubuntu-kata-fc-vaccel /bin/bash
root      983888       1  0 18:14 ?        00:00:00 /opt/kata/bin/containerd-shim-kata-v2 -namespace default -address /run/containerd/containerd.sock -publish-binary /usr/bin/containerd -id ubuntu-kata-fc-vaccel
root      983900  983888  0 18:14 ?        00:00:01 /opt/kata/bin/firecracker --api-sock /run/vc/firecracker/ubuntu-kata-fc-vaccel/root/run/firecracker.socket --config-file /run/vc/firecracker/ubuntu-kata-fc-vaccel/root/fcConfig.json
root      983906  983888  0 18:14 ?        00:00:02 /opt/vaccel-v0.4.0/bin/vaccelrt-agent --server-address unix:///run/vc/firecracker/ubuntu-kata-fc-vaccel/root/kata.hvsock_2048
root      994531  894257  0 18:19 pts/17   00:00:00 grep ubuntu-kata-fc
```
