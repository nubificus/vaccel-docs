# Install from binary packages

vAccel is under heavy development. To facilitate deployment & testing, we build
binaries for the various components and produce `deb` packages. The available
binary components are:

- vAccelRT core: runtime library, 
- plugins: Jetson, PYNQ, VSOCK, VIRTIO, TF, PYTORCH [WiP], 
- vAccel Agent: the user-space agent that services vAccel API requests on the
  host,
- vAccel Python bindings: the necessary files to consume the vAccel API from a python program.

## Download binaries

Download the relevant binaries (`deb` or artifacts) using the links in the
[table](#binaries) below.

#### Binaries

Component     | Version |  Package | Binary Artifact
------------- | --------| -------- | -------------
vAccelRT core | v0.5.0  | [`x86_64`](https://s3.nbfc.io/nbfc-assets/github/vaccelrt/master/x86_64/Release-deb/vaccel-0.5.0-Linux.deb) [`arm64`](https://s3.nbfc.io/nbfc-assets/github/vaccelrt/master/aarch64/Release-deb/vaccel-0.5.0-Linux.deb) [`arm`](https://s3.nbfc.io/nbfc-assets/github/vaccelrt/master/aarch32/Release-deb/vaccel-0.5.0-Linux.deb) | [`x86_64`](https://s3.nbfc.io/nbfc-assets/github/vaccelrt/master/x86_64/Release-tar/vaccel-0.5.0-Linux.tar.gz) [`arm64`](https://s3.nbfc.io/nbfc-assets/github/vaccelrt/master/aarch64/Release-tar/vaccel-0.5.0-Linux.tar.gz) [`arm`](https://s3.nbfc.io/nbfc-assets/github/vaccelrt/master/aarch32/Release-tar/vaccel-0.5.0-Linux.tar.gz)
vAccelRT agent  | v0.3.0  | [`x86_64`](https://s3.nbfc.io/nbfc-assets/github/vaccelrt/agent/main/x86_64/Release-deb/vaccelrt-agent-0.3.0-Linux.deb) [`arm64`](https://s3.nbfc.io/nbfc-assets/github/vaccelrt/agent/main/aarch64/Release-deb/vaccelrt-agent-0.3.0-Linux.deb) [`arm`](https://s3.nbfc.io/nbfc-assets/github/vaccelrt/agent/main/aarch32/Release-deb/vaccelrt-agent-0.3.0-Linux.deb) | [`x86_64`](https://s3.nbfc.io/nbfc-assets/github/vaccelrt/agent/main/x86_64/release/vaccelrt-agent) [`arm64`](https://s3.nbfc.io/nbfc-assets/github/vaccelrt/agent/main/aarch64/release/vaccelrt-agent) [`arm`](https://s3.nbfc.io/nbfc-assets/github/vaccelrt/agent/59704ec358de8f68345556a774c60788ac957183/aarch32/release/vaccelrt-agent)
Jetson plugin | v0.1.0  | [`x86_64`](https://s3.nbfc.io/nbfc-assets/github/vaccelrt/plugins/jetson_inference/main/x86_64/Release-deb/vaccelrt-plugin-jetson-0.1.0-Linux.deb) [`arm64`](https://s3.nbfc.io/nbfc-assets/github/vaccelrt/plugins/jetson_inference/main/aarch64/Release-deb/vaccelrt-plugin-jetson-0.1-Linux.deb) | [`x86_64`](https://s3.nbfc.io/nbfc-assets/github/vaccelrt/plugins/jetson_inference/main/x86_64/Release/libvaccel-jetson.so) [`arm64`](https://s3.nbfc.io/nbfc-assets/github/vaccelrt/plugins/jetson_inference/main/aarch64/Release/libvaccel-jetson.so)
Tensorflow plugin | v0.1.0  | [`x86_64`](https://s3.nbfc.io/nbfc-assets/github/vaccelrt/plugins/tensorflow/main/x86_64/Release-deb/vaccel-tensorflow-0.1.0-Linux.deb) [`arm64`](https://s3.nbfc.io/nbfc-assets/github/vaccelrt/plugins/tensorflow/main/aarch64/Release-deb/vaccel-tensorflow-0.1.0-Linux.deb) | [`x86_64`](https://s3.nbfc.io/nbfc-assets/github/vaccelrt/plugins/tensorflow/main/x86_64/Release/libvaccel-tf.so) [`arm64`](https://s3.nbfc.io/nbfc-assets/github/vaccelrt/plugins/tensorflow/main/aarch64/Release/libvaccel-tf.so)
PYNQ plugin   | v0.1.1  | [`x86_64`](https://s3.nbfc.io/nbfc-assets/github/vaccelrt/plugins/pynq/main/x86_64/Release-deb/vaccelrt-plugin-pynq-0.1.1-Linux.deb) [`arm64`](https://s3.nbfc.io/nbfc-assets/github/vaccelrt/plugins/pynq/main/aarch64/Release-deb/vaccelrt-plugin-pynq-0.1.1-Linux.deb) [`arm`](https://s3.nbfc.io/nbfc-assets/github/vaccelrt/plugins/pynq/main/aarch32/Release-deb/vaccelrt-plugin-pynq-0.1-Linux.deb) | [`x86_64`](https://s3.nbfc.io/nbfc-assets/github/vaccelrt/plugins/pynq/main/x86_64/Release/libvaccel-pynq.so) [`arm64`](https://s3.nbfc.io/nbfc-assets/github/vaccelrt/plugins/pynq/main/aarch64/Release/libvaccel-pynq.so) [`arm`](https://s3.nbfc.io/nbfc-assets/github/vaccelrt/plugins/pynq/main/aarch32/Release/libvaccel-pynq.so)
VSOCK plugin   | v0.1.0  | [`x86_64`](https://s3.nbfc.io/nbfc-assets/github/vaccelrt/plugins/vsock/master/x86_64/Release-deb/vaccelrt-plugin-vsock-0.1.0-Linux.deb) [`arm64`](https://s3.nbfc.io/nbfc-assets/github/vaccelrt/plugins/vsock/master/aarch64/Release-deb/vaccelrt-plugin-vsock-0.1.0-Linux.deb) [`arm`](https://s3.nbfc.io/nbfc-assets/github/vaccelrt/plugins/vsock/master/aarch32/Release-deb/vaccelrt-plugin-vsock-0.1.0-Linux.deb) | [`x86_64`](https://s3.nbfc.io/nbfc-assets/github/vaccelrt/plugins/vsock/master/x86_64/Release/libvaccel-vsock.so) [`arm64`](https://s3.nbfc.io/nbfc-assets/github/vaccelrt/plugins/vsock/master/aarch64/Release/libvaccel-vsock.so) [`arm`](https://s3.nbfc.io/nbfc-assets/github/vaccelrt/plugins/vsock/master/aarch32/Release/libvaccel-vsock.so)
VIRTIO plugin   | v0.1.0  | [`x86_64`](https://s3.nbfc.io/nbfc-assets/github/vaccelrt/plugins/virtio/main/x86_64/Release-deb/vaccelrt-plugin-virtio-0.1.0-Linux.deb) [`arm64`](https://s3.nbfc.io/nbfc-assets/github/vaccelrt/plugins/virtio/main/aarch64/Release-deb/vaccelrt-plugin-virtio-0.1.0-Linux.deb) | [`x86_64`](https://s3.nbfc.io/nbfc-assets/github/vaccelrt/plugins/virtio/main/x86_64/Release/libvaccel-virtio.so) [`arm64`](https://s3.nbfc.io/nbfc-assets/github/vaccelrt/plugins/virtio/main/aarch64/Release/libvaccel-virtio.so)
TORCH plugin   | v0.1.0*  | [`x86_64`](https://s3.nbfc.io/nbfc-assets/github/vaccelrt/plugins/torch/main/x86_64/Release-deb/vaccelrt-plugin-torch-0.1.0-Linux.deb) [`arm64`](https://s3.nbfc.io/nbfc-assets/github/vaccelrt/plugins/torch/main/aarch64/Release-deb/vaccelrt-plugin-torch-0.1.0-Linux.deb) | [`x86_64`](https://s3.nbfc.io/nbfc-assets/github/vaccelrt/plugins/torch/main/x86_64/Release/libvaccel-torch.so) [`arm64`](https://s3.nbfc.io/nbfc-assets/github/vaccelrt/plugins/torch/main/aarch64/Release/libvaccel-torch.so)
Python bindings | v0.0.1 | [`x86_64`](https://s3.nbfc.io/nbfc-assets/github/python-vaccel/main/x86_64/vaccel-python-0.0.1.tar.gz) [`arm64`](https://s3.nbfc.io/nbfc-assets/github/python-vaccel/main/aarch64/vaccel-python-0.0.1.tar.gz) | [`x86_64`](https://s3.nbfc.io/nbfc-assets/github/python-vaccel/main/x86_64/vaccel-python-0.0.1.tar.gz) [`arm64`](https://s3.nbfc.io/nbfc-assets/github/python-vaccel/main/aarch64/vaccel-python-0.0.1.tar.gz)
TF bindings | v0.0.1 | [`x86_64`](https://s3.nubificus.co.uk/nbfc-assets/github/vaccelrt/plugins/tensorflow/main/x86_64/Release-deb/vaccel-tensorflow-0.1.0-Linux.deb) [`arm64`](https://s3.nubificus.co.uk/nbfc-assets/github/vaccelrt/plugins/tensorflow/main/aarch64/Release-deb/vaccel-tensorflow-0.1.0-Linux.deb) | [`x86_64`](https://s3.nubificus.co.uk/nbfc-assets/github/vaccelrt/plugins/tensorflow/main/x86_64/Release/libvaccel-tf-bindings.so) [`arm64`](https://s3.nubificus.co.uk/nbfc-assets/github/vaccelrt/plugins/tensorflow/main/aarch64/Release/libvaccel-tf-bindings.so)

In addition to the `deb` packages, we provide:

- `tar` archives for vAccelRT core, holding shared objects, include files, and examples
- shared objects (`.so`) for the various plugins
- an executable for the vAccelRT agent

## Install


### Install vAccelRT core library

#### `deb` package

We use `dpkg` to install the relevant `deb` package on a Ubuntu or Debian-based
system.

For example, to install the vAccelRT core library for an `x86_64` host, do:

```
wget https://s3.nbfc.io/nbfc-assets/github/vaccelrt/master/x86_64/Release-deb/vaccel-0.5.0-Linux.deb
dpkg -i vaccel-0.5.0-Linux.deb
```

The output should be something like the following:

```console
# wget https://s3.nbfc.io/nbfc-assets/github/vaccelrt/master/x86_64/Release-deb/vaccel-0.5.0-Linux.deb
--2022-11-08 21:25:08--  https://s3.nbfc.io/nbfc-assets/github/vaccelrt/master/x86_64/Release-deb/vaccel-0.5.0-Linux.deb
Resolving s3.nbfc.io (s3.nbfc.io)... 84.254.1.240
Connecting to s3.nbfc.io (s3.nbfc.io)|84.254.1.240|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 2124232 (2.0M) [application/x-debian-package]
Saving to: 'vaccel-0.5.0-Linux.deb'

vaccel-0.5.0-Linux.deb       100%[===========================================>]   2.03M  --.-KB/s    in 0.06s

2022-11-08 21:25:11 (31.9 MB/s) - 'vaccel-0.5.0-Linux.deb' saved [2124232/2124232]

# dpkg -i vaccel-0.5.0-Linux.deb
Selecting previously unselected package vaccel.
(Reading database ... 4878 files and directories currently installed.)
Preparing to unpack vaccel-0.5.0-Linux.deb ...
Unpacking vaccel (0.5.0) ...
Setting up vaccel (0.5.0) ...
```
The core runtime library package contains the following:

- `libvaccel.so`: the main dispatcher
- `libvaccel-python.so`: a wrapper library to be used for the python bindings
- two plugins: `libvaccel-noop.so` and `libvaccel-exec.so`
- example binaries that show the use of the vAccel User API
- helper files for the examples to run

```console
# tree /usr/local/lib
/usr/local/lib
|-- libmytestlib.so
|-- libvaccel-noop.so
|-- libvaccel-python.so
`-- libvaccel.so

0 directories, 4 files
```

```console
# tree /usr/local/bin/
/usr/local/bin/
|-- classify
|-- classify_generic
|-- depth
|-- depth_generic
|-- detect
|-- detect_generic
|-- exec
|-- exec_generic
|-- minmax
|-- minmax_generic
|-- noop
|-- pose
|-- pose_generic
|-- pynq_array_copy
|-- pynq_parallel
|-- pynq_vector_add
|-- segment
|-- segment_generic
|-- sgemm
|-- sgemm_generic
|-- tf_inference
|-- tf_model
`-- tf_saved_model

0 directories, 23 files
```

```console
# tree /usr/local/share/
/usr/local/share/
|-- images
|   `-- example.jpg
|-- input
|   `-- input_262144.csv
|-- man
|-- models
|   `-- tf
|       |-- frozen_graph.pb
|       `-- lstm2
|           |-- keras_metadata.pb
|           |-- saved_model.pb
|           `-- variables
|               |-- variables.data-00000-of-00001
|               `-- variables.index
|-- vaccel-python.pc
`-- vaccel.pc

7 directories, 9 files
```

#### tar archive

Alternatively, you can install the vAccelRT core runtime library using the tar artifact. Use the commands below to install it to `/usr/local/`:

```bash
wget https://s3.nbfc.io/nbfc-assets/github/vaccelrt/master/x86_64/Release-tar/vaccel-0.5.0-Linux.tar.gz
tar -zxvf /vaccel-0.5.0-Linux.tar.gz  --strip-components=1 -C /
```

### Install Plugins

#### `deb` package

To install a plugin, download the relevant `deb` package for the host
architecture and install it. 

For example, to install the `pynq` plugin on an aarch64 host do the following:

```bash
wget https://s3.nbfc.io/nbfc-assets/github/vaccelrt/plugins/pynq/main/aarch64/Release-deb/vaccelrt-plugin-pynq-0.1.1-Linux.deb
dpkg -i vaccelrt-plugin-pynq-0.1.1-Linux.deb
```

The output should be something like the following:
```console
# wget https://s3.nbfc.io/nbfc-assets/github/vaccelrt/plugins/pynq/main/aarch64/Release-deb/vaccelrt-plugin-pynq-0.1.1-Linux.deb
--2022-11-08 21:42:41--  https://s3.nbfc.io/nbfc-assets/github/vaccelrt/plugins/pynq/main/aarch64/Release-deb/vaccelrt-plugin-pynq-0.1.1-Linux.deb
Resolving s3.nbfc.io (s3.nbfc.io)... 84.254.1.240
Connecting to s3.nbfc.io (s3.nbfc.io)|84.254.1.240|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 9604 (9.4K) [application/x-debian-package]
Saving to: ‘vaccelrt-plugin-pynq-0.1.1-Linux.deb’

vaccelrt-plugin-pynq-0.1.1-Linux.deb   100%[============================================================================>]   9.38K  --.-KB/s    in 0.003s

2022-11-08 21:42:41 (2.90 MB/s) - ‘vaccelrt-plugin-pynq-0.1.1-Linux.deb’ saved [9604/9604]

# dpkg -i vaccelrt-plugin-pynq-0.1.1-Linux.deb
(Reading database ... 215228 files and directories currently installed.)
Preparing to unpack vaccelrt-plugin-pynq-0.1.1-Linux.deb ...
Unpacking vaccelrt-plugin-pynq (0.1.1) over (0.1.1) ...
Setting up vaccelrt-plugin-pynq (0.1.1) ...


```

and `libvaccel-pynq.so` should appear in `/usr/local/lib`:

```console
# tree /usr/local/lib/
/usr/local/lib/
├── libvaccel-exec.so
├── libvaccel-noop.so
├── libvaccel-pynq.so
├── libvaccel-python.so
├── libvaccel.so

0 directories, 5 files
```

#### shared object

Alternatively, you can grab the shared object directly from the
[table](#binaries) above and set the environment variable `VACCEL_BACKENDS` to
the full path of the file. See [Running a vAccel
application](build_run_app.md#running-a-vaccel-application) for more info on
how to specify the plugin(s) for a vAccel application.


### Install vAccelRT agent

#### `deb` package

To install the agent, download the relevant `deb` package for the host
architecture and install it. 

```bash
wget https://s3.nbfc.io/nbfc-assets/github/vaccelrt/agent/main/x86_64/Release-deb/vaccelrt-agent-0.3.0-Linux.deb
dpkg -i vaccelrt-agent-0.3.0-Linux.deb
```

The output should be something like the following:

```console
# wget https://s3.nbfc.io/nbfc-assets/github/vaccelrt/agent/main/x86_64/Release-deb/vaccelrt-agent-0.3.0-Linux.deb
--2022-11-10 18:20:57--  https://s3.nbfc.io/nbfc-assets/github/vaccelrt/agent/main/x86_64/Release-deb/vaccelrt-agent-0.3.0-Linux.deb
Resolving s3.nbfc.io (s3.nbfc.io)... 84.254.1.240
Connecting to s3.nbfc.io (s3.nbfc.io)|84.254.1.240|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 1738158 (1.7M) [application/x-debian-package]
Saving to: 'vaccelrt-agent-0.3.0-Linux.deb'

vaccelrt-agent-0.3.0-Linux.deb       100%[=====================================================================>]   1.66M  --.-KB/s    in 0.06s

2022-11-10 18:20:58 (25.8 MB/s) - 'vaccelrt-agent-0.3.0-Linux.deb' saved [1738158/1738158]

root@18c0e0189e2b:/# dpkg -i vaccelrt-agent-0.3.0-Linux.deb
Selecting previously unselected package vaccelrt-agent.
(Reading database ... 4878 files and directories currently installed.)
Preparing to unpack vaccelrt-agent-0.3.0-Linux.deb ...
Unpacking vaccelrt-agent (0.3.0) ...
Setting up vaccelrt-agent (0.3.0) ...
```

and you should see the binary in `/usr/local/bin`:

```console
# tree /usr/local/bin/
/usr/local/bin/
`-- vaccelrt-agent

0 directories, 1 file
```

#### executable

Alternatively, you can grab the binary directly and make it executable:

```
wget https://s3.nbfc.io/nbfc-assets/github/vaccelrt/agent/main/x86_64/Release/vaccelrt-agent
# We will need to make it executable as file permissions are not preserved 
chmod +x ./vaccelrt-agent
mv ./vaccelrt-agent /usr/local/bin
```

