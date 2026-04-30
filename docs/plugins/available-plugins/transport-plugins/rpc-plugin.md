# RPC Plugin

The RPC plugin for vAccel implements RPC-based transport for vAccel operations.
This plugin supports `vsock`, `unix` and `tcp` sockets.

## Overview

The plugin forwards vAccel calls from a host without accelerator access (ie. a
VM) or a remote host, to a host with a hardware accelerator. In order to use the
plugin you also need the vAccel RPC agent. The agent handles the plugin requests
and translates the forwarded calls to host vAccel calls. Essentially, to use the
RPC plugin the following components must be in place:

1. _Host w/o accelerator:_ vAccel + the RPC plugin, to forward the application
   calls
2. _Host w/ accelerator:_ The vAccel RPC agent + vAccel + an acceleration
   plugin, to handle the forwarded calls and perform the actual acceleration

## Supported operations

- [Image classification](../../../api/api-reference/operations.md#image-classification)
- [Image segmentation](../../../api/api-reference/operations.md#image-segmentation)
- [Object detection](../../../api/api-reference/operations.md#object-detection)
- [Pose estimation](../../../api/api-reference/operations.md#pose-estimation)
- [Monocular depth](../../../api/api-reference/operations.md#monocular-depth)

- [Matrix-to-matrix multiplication](../../../api/api-reference/operations.md#matrix-to-matrix-multiplication)
- [Array copy](../../../api/api-reference/operations.md#array-copy)
- [Matrix-to-matrix multiplication simple](../../../api/api-reference/operations.md#matrix-to-matrix-multiplication-simple)
- [Matrix-to-matrix multiplication and addition simple](../../../api/api-reference/operations.md#matrix-to-matrix-multiplication-and-addition-simple-wip)
- [Vector add](../../../api/api-reference/operations.md#vector-add)

- [Exec](../../../api/api-reference/operations.md#exec)
- [Exec with resource](../../../api/api-reference/operations.md#exec-with-resource)

- [TensorFlow model load](../../../api/api-reference/operations.md#tensorflow-model-load)
- [TensorFlow model unload](../../../api/api-reference/operations.md#tensorflow-model-unload)
- [TensorFlow model run](../../../api/api-reference/operations.md#tensorflow-model-run)
- [TensorFlow Lite model load](../../../api/api-reference/operations.md#tensorflow-lite-model-load)
- [TensorFlow Lite model unload](../../../api/api-reference/operations.md#tensorflow-lite-model-unload)
- [TensorFlow Lite model run](../../../api/api-reference/operations.md#tensorflow-lite-model-run)

- [Torch model load](../../../api/api-reference/operations.md#torch-model-load)
- [Torch model run](../../../api/api-reference/operations.md#torch-model-run)

- [MinMax](../../../api/api-reference/operations.md#minmax)
- [Generic operation](../../../api/api-reference/operations.md#generic-operation)
- [Debug operation](../../../api/api-reference/operations.md#debug-operation)

## Installing the plugin

You can get the latest RPC plugin binary release from the
[Releases](https://github.com/nubificus/vaccel/releases) page of the vAccel
repository. Releases include DEB packages and binaries for x86_64/aarch64/armv7l
Ubuntu-based systems.

### DEB

To install the DEB package of the latest RPC plugin release:

/// tab | x86

```sh
wget https://github.com/nubificus/vaccel/releases/download/v[[ versions.vaccel ]]/vaccel-rpc_[[ versions.plugins.rpc ]]-1_amd64.deb
sudo dpkg -i vaccel-rpc_[[ versions.plugins.rpc ]]-1_amd64.deb
```

///

/// tab | ARM (64-bit)

```sh
wget https://github.com/nubificus/vaccel/releases/download/v[[ versions.vaccel ]]/vaccel-rpc_[[ versions.plugins.rpc ]]-1_arm64.deb
sudo dpkg -i vaccel-rpc_[[ versions.plugins.rpc ]]-1_arm64.deb
```

///

/// tab | ARM (32-bit)

```sh
wget https://github.com/nubificus/vaccel/releases/download/v[[ versions.vaccel ]]/vaccel-rpc_[[ versions.plugins.rpc ]]-1_armhf.deb
sudo dpkg -i vaccel-rpc_[[ versions.plugins.rpc ]]-1_armhf.deb
```

///

### TAR

To install the TAR binary package of the latest RPC plugin release:

/// tab | x86

```sh
wget https://github.com/nubificus/vaccel/releases/download/v[[ versions.vaccel ]]/vaccel-rpc_[[ versions.plugins.rpc ]]_x86_64.tar.gz
# Replace '/usr/local' below with the desired installation prefix
tar xfv vaccel-rpc_[[ versions.plugins.rpc ]]_x86_64.tar.gz --strip-components=2 -C /usr/local
# Update pkg-config files with the correct prefix
find /usr/local -name "vaccel-rpc.pc" -exec sed -i 's:^\(prefix=\).*:\1/usr/local:g' {} \;
```

///

/// tab | ARM (64-bit)

```sh
wget https://github.com/nubificus/vaccel/releases/download/v[[ versions.vaccel ]]/vaccel-rpc_[[ versions.plugins.rpc ]]_aarch64.tar.gz
# Replace '/usr/local' below with the desired installation prefix
tar xfv vaccel-rpc_[[ versions.plugins.rpc ]]_aarch64.tar.gz --strip-components=2 -C /usr/local
# Update pkg-config files with the correct prefix
find /usr/local -name "vaccel-rpc.pc" -exec sed -i 's:^\(prefix=\).*:\1/usr/local:g' {} \;
```

///

/// tab | ARM (32-bit)

```sh
wget https://github.com/nubificus/vaccel/releases/download/v[[ versions.vaccel ]]/vaccel-rpc_[[ versions.plugins.rpc ]]_armv7l.tar.gz
# Replace '/usr/local' below with the desired installation prefix
tar xfv vaccel-rpc_[[ versions.plugins.rpc ]]_armv7l.tar.gz --strip-components=2 -C /usr/local
# Update pkg-config files with the correct prefix
find /usr/local -name "vaccel-rpc.pc" -exec sed -i 's:^\(prefix=\).*:\1/usr/local:g' {} \;
```

///

### Latest artifacts

You can also find prebuilt artifacts of the latest RPC plugin revision at:

/// tab | x86

```sh
# DEB
https://s3.nbfc.io/nbfc-assets/github/vaccel/plugins/rpc/rev/main/x86_64/release/vaccel-rpc_latest_amd64.deb
# TAR
https://s3.nbfc.io/nbfc-assets/github/vaccel/plugins/rpc/rev/main/x86_64/release/vaccel-rpc_latest.tar.gz
```

///

/// tab | ARM (64-bit)

```sh
# DEB
https://s3.nbfc.io/nbfc-assets/github/vaccel/plugins/rpc/rev/main/aarch64/release/vaccel-rpc_latest_arm64.deb
# TAR
https://s3.nbfc.io/nbfc-assets/github/vaccel/plugins/rpc/rev/main/aarch64/release/vaccel-rpc_latest.tar.gz
```

///

/// tab | ARM (32-bit)

```sh
# DEB
https://s3.nbfc.io/nbfc-assets/github/vaccel/plugins/rpc/rev/main/armv7l/release/vaccel-rpc_latest_armhf.deb
# TAR
https://s3.nbfc.io/nbfc-assets/github/vaccel/plugins/rpc/rev/main/armv7l/release/vaccel-rpc_latest.tar.gz
```

///

## Installing the RPC agent

You can get the latest RPC agent binary release from the
[Releases](https://github.com/nubificus/vaccel-rust/releases) page of the
[vAccel Rust repository](https://github.com/nubificus/vaccel-rust). Releases
include DEB packages and binaries for x86_64/aarch64/armv7l Ubuntu-based
systems.

### DEB

To install the DEB package of the latest RPC agent release:

/// tab | x86

```sh
wget https://github.com/nubificus/vaccel/releases/download/v[[ versions.vaccel ]]/vaccel-rpc-agent_[[ versions.bindings.rust ]]-1_amd64.deb
sudo dpkg -i vaccel-rpc-agent_[[ versions.bindings.rust ]]-1_amd64.deb
```

///

/// tab | ARM (64-bit)

```sh
wget https://github.com/nubificus/vaccel/releases/download/v[[ versions.vaccel ]]/vaccel-rpc-agent_[[ versions.bindings.rust ]]-1_arm64.deb
sudo dpkg -i vaccel-rpc-agent_[[ versions.bindings.rust ]]-1_arm64.deb
```

///

/// tab | ARM (32-bit)

```sh
wget https://github.com/nubificus/vaccel/releases/download/v[[ versions.vaccel ]]/vaccel-rpc-agent_[[ versions.bindings.rust ]]-1_armhf.deb
sudo dpkg -i vaccel-rpc-agent_[[ versions.bindings.rust ]]-1_armhf.deb
```

///

### TAR

To install the TAR binary package of the latest RPC agent release:

/// tab | x86

```sh
wget https://github.com/nubificus/vaccel/releases/download/v[[ versions.vaccel ]]/vaccel-rpc-agent_[[ versions.bindings.rust ]]_x86_64.tar.gz
# Replace '/usr/local' below with the desired installation prefix
tar xfv vaccel-rpc-agent_[[ versions.bindings.rust ]]_x86_64.tar.gz --strip-components=2 -C /usr/local
```

///

/// tab | ARM (64-bit)

```sh
wget https://github.com/nubificus/vaccel/releases/download/v[[ versions.vaccel ]]/vaccel-rpc-agent_[[ versions.bindings.rust ]]_aarch64.tar.gz
# Replace '/usr/local' below with the desired installation prefix
tar xfv vaccel-rpc-agent_[[ versions.bindings.rust ]]_aarch64.tar.gz --strip-components=2 -C /usr/local
```

///

/// tab | ARM (32-bit)

```sh
wget https://github.com/nubificus/vaccel/releases/download/v[[ versions.vaccel ]]/vaccel-rpc-agent_[[ versions.bindings.rust ]]_armv7l.tar.gz
# Replace '/usr/local' below with the desired installation prefix
tar xfv vaccel-rpc-agent_[[ versions.bindings.rust ]]_armv7l.tar.gz --strip-components=2 -C /usr/local
```

///

### Latest artifacts

You can also find prebuilt artifacts of the latest RPC agent revision at:

/// tab | x86

```sh
# DEB
https://s3.nbfc.io/nbfc-assets/github/vaccel/rust/rev/main/x86_64/release/vaccel-rpc-agent_latest_amd64.deb
# TAR
https://s3.nbfc.io/nbfc-assets/github/vaccel/rust/rev/main/x86_64/release/vaccel-rpc-agent_latest_x86_64.tar.gz
```

///

/// tab | ARM (64-bit)

```sh
# DEB
https://s3.nbfc.io/nbfc-assets/github/vaccel/rust/rev/main/aarch64/release/vaccel-rpc-agent_latest_arm64.deb
# TAR
https://s3.nbfc.io/nbfc-assets/github/vaccel/rust/rev/main/aarch64/release/vaccel-rpc-agent_latest_aarch64.tar.gz
```

///

/// tab | ARM (32-bit)

```sh
# DEB
https://s3.nbfc.io/nbfc-assets/github/vaccel/rust/rev/main/armv7l/release/vaccel-rpc-agent_latest_armhf.deb
# TAR
https://s3.nbfc.io/nbfc-assets/github/vaccel/rust/rev/main/armv7l/release/vaccel-rpc-agent_latest_armv7l.tar.gz
```

///

## Usage

To specify RPC plugin as the selected plugin for vAccel execution:

```sh
export VACCEL_PLUGINS=libvaccel-rpc.so
```

Ensure vAccel and the RPC plugin libraries are in the library search paths
before trying to use the plugin. In order to use the plugin, an
[agent instance](#rpc-agent-usage) must be running.

Additionally, you need to use a correct RPC address for the agent and the
plugin. By default, the RPC components will use `tcp://127.0.0.1:65500` to
communicate.

The address is of the form:

```bash
"<prefix>://<address>[:<port>]"
```

where `<prefix>` is one of `tcp`, `unix` or `vsock` and `<address>`/`<port>`
have the required format for the respective socket types.

You can set an RPC address for the plugin by setting `VACCEL_RPC_ADDRESS`:

```sh
export VACCEL_RPC_ADDRESS=tcp://127.0.0.1:65500
```

### RPC agent usage

The RPC agent must be installed in the host with the actual accelerator. Ensure,
vAccel is also installed on the agent's host and present in the library search
paths before trying to start the agent.

To use the plugin, an RPC agent instance must be running and an
[acceleration](../acceleration-plugins/index.md) plugin must be loaded.
Therefore, an acceleration plugin must also be installed on the agent's host.

To set an address for the RPC agent use the `-a` flag:

```sh
vaccel-rpc-agent -a "tcp://127.0.0.1:65500"
```

You can execute the RPC agent, ie. using the `NoOp` plugin on the same host as
the plugin, with:

```sh
VACCEL_BOOTSTRAP_ENABLED=0 vaccel-rpc-agent \
    -a "tcp://127.0.0.1:65500" \
    --vaccel-config "plugins=libvaccel-noop.so"
```

You can use `--vaccel-config` with all the vaccel
[configuration](../../../configuration.md) variables in lowercase (preferred).
You can also start the agent without `--vaccel-config` by setting configuration
variables in the environment, as you would do for a plugin.

The RPC agent provides usage information via:

```sh
vaccel-rpc-agent -h
```

Example configurations for different socket types:

```bash
# unix socket
ADDRESS="unix:///path/to/unix/socket"
vaccel-rpc-agent -a "${ADDRESS}"
export VACCEL_RPC_ADDRESS=${ADDRESS}

# tcp socket
ADDRESS="tcp://localhost:65500"
vaccel-rpc-agent -a "${ADDRESS}"
export VACCEL_RPC_ADDRESS=${ADDRESS}

# vsock socket
# NOTE: Address for vsock sockets is the host reserved address
ADDRESS="vsock://2:2048"
vaccel-rpc-agent -a "${ADDRESS}"
export VACCEL_RPC_ADDRESS="${ADDRESS}"
```

## Running an example

Start the RPC agent on the accelerator host, ie using the 'NoOp' plugin:

```console
$ VACCEL_BOOTSTRAP_ENABLED=0 vaccel-rpc-agent \
      -a "tcp://127.0.0.1:65500" \
      --vaccel-config "plugins=libvaccel-noop.so"
[2026-04-30T12:42:24Z INFO  ttrpc::sync::server] server listen started
[2026-04-30T12:42:24Z INFO  ttrpc::sync::server] server started
[2026-04-30T12:42:24Z INFO  vaccel_rpc_agent] vAccel RPC agent started
[2026-04-30T12:42:24Z INFO  vaccel_rpc_agent] Listening on 'tcp://127.0.0.1:65500', press Ctrl+C to exit
```

On the same host, export the necessary variables for the plugin:

```sh
export VACCEL_PLUGINS=libvaccel-rpc.so
export VACCEL_RPC_ADDRESS=tcp://127.0.0.1:65500
# Optionally, for verbose output
export VACCEL_LOG_LEVEL=4
```

Assuming vAccel is installed at `/usr/local`, you can run a dummy image
classification with:

```console
$ classify /usr/local/share/vaccel/images/example.jpg
2026.04.30-12:42:37.76 - <debug> Initializing vAccel
2026.04.30-12:42:37.76 - <info> vAccel 0.7.1-93-ebc23b1f
2026.04.30-12:42:37.76 - <debug> Config:
2026.04.30-12:42:37.76 - <debug>   plugins = libvaccel-rpc.so
2026.04.30-12:42:37.76 - <debug>   log_level = debug
2026.04.30-12:42:37.76 - <debug>   log_file = (null)
2026.04.30-12:42:37.76 - <debug>   profiling_enabled = false
2026.04.30-12:42:37.76 - <debug>   version_ignore = false
2026.04.30-12:42:37.78 - <debug> Created top-level rundir: /run/user/0/vaccel/zha8un
2026.04.30-12:42:37.78 - <info> Registered plugin rpc 0.2.1-21-e08235e7
2026.04.30-12:42:37.78 - <debug> rpc is a VirtIO module
2026.04.30-12:42:37.78 - <debug> Registered op exec from plugin rpc
2026.04.30-12:42:37.78 - <debug> Registered op exec_with_resource from plugin rpc
2026.04.30-12:42:37.78 - <debug> Registered op image_classify from plugin rpc
2026.04.30-12:42:37.78 - <debug> Registered op image_detect from plugin rpc
2026.04.30-12:42:37.78 - <debug> Registered op image_segment from plugin rpc
2026.04.30-12:42:37.78 - <debug> Registered op image_depth from plugin rpc
2026.04.30-12:42:37.78 - <debug> Registered op image_pose from plugin rpc
2026.04.30-12:42:37.78 - <debug> Registered op tflite_model_load from plugin rpc
2026.04.30-12:42:37.78 - <debug> Registered op tflite_model_unload from plugin rpc
2026.04.30-12:42:37.78 - <debug> Registered op tflite_model_run from plugin rpc
2026.04.30-12:42:37.78 - <debug> Registered op torch_model_load from plugin rpc
2026.04.30-12:42:37.78 - <debug> Registered op torch_model_run from plugin rpc
2026.04.30-12:42:37.78 - <debug> Registered op blas_sgemm from plugin rpc
2026.04.30-12:42:37.78 - <debug> Registered op fpga_arraycopy from plugin rpc
2026.04.30-12:42:37.78 - <debug> Registered op fpga_mmult from plugin rpc
2026.04.30-12:42:37.78 - <debug> Registered op fpga_parallel from plugin rpc
2026.04.30-12:42:37.78 - <debug> Registered op fpga_vectoradd from plugin rpc
2026.04.30-12:42:37.78 - <debug> Registered op minmax from plugin rpc
2026.04.30-12:42:37.78 - <debug> Registered op opencv from plugin rpc
2026.04.30-12:42:37.78 - <debug> Registered op tf_model_load from plugin rpc
2026.04.30-12:42:37.78 - <debug> Registered op tf_model_unload from plugin rpc
2026.04.30-12:42:37.78 - <debug> Registered op tf_model_run from plugin rpc
2026.04.30-12:42:37.78 - <debug> Loaded plugin rpc from libvaccel-rpc.so
2026.04.30-12:42:37.79 - <debug> [rpc] Initializing new remote session
2026.04.30-12:42:37.79 - <debug> [rpc] Initialized remote session 1
2026.04.30-12:42:37.79 - <debug> New rundir for session 1: /run/user/0/vaccel/zha8un/session.1
2026.04.30-12:42:37.79 - <debug> Initialized session 1 with plugin rpc (remote id: 1)
Initialized session with id: 1
2026.04.30-12:42:37.79 - <debug> session:1 Looking for func implementing op image_classify
2026.04.30-12:42:37.79 - <debug> Returning func for op image_classify from plugin rpc
2026.04.30-12:42:37.79 - <debug> [rpc] session:1 Executing op image_classify
classification tags: This is a dummy classification tag!
classification imagename: This is a dummy imgname!
2026.04.30-12:42:37.83 - <debug> [rpc] Releasing remote session 1
2026.04.30-12:42:37.91 - <debug> Released session 1
2026.04.30-12:42:37.91 - <debug> Cleaning up vAccel
2026.04.30-12:42:37.91 - <debug> Cleaning up sessions
2026.04.30-12:42:37.91 - <debug> Cleaning up resources
2026.04.30-12:42:37.91 - <debug> Cleaning up plugins
2026.04.30-12:42:37.91 - <debug> Unregistered plugin rpc
```

<!-- markdownlint-disable code-block-style -->

!!! info

    You can find detailed tutorials on how to run a vAccel application
    [on a VM](../../../tutorials/running-a-vaccel-application-on-a-vm.md) and
    [remotely](../../../tutorials/running-a-vaccel-application-remotely.md) in the
    [Tutorials](../../../tutorials/index.md) section.

<!-- markdownlint-restore -->
