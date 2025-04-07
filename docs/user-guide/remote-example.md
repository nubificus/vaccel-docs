# Run a vAccel application remotely

## Overview

As with the [VM case](vm-example.md), you can use the `RPC` plugin to run a
vAccel application remotely. In this scenario, the plugin forwards function
calls to a remote system. Figure 1 shows the execution flow:

<figure>
  <img src="/img/vaccel-remote-flow.png" width="800" align=left
    alt="Remote application execution flow" />
  <figcaption>Figure 1. Remote application execution flow</figcaption>
</figure>

The application runs on the `Remote Host` and uses the `RPC` plugin, while
vAccel RPC agent runs on the host with hardware acceleration support and uses
vAccel with an acceleration plugin.

Similarly to executing an application [from a VM](vm-example.md), the following
components must be in place to use the `RPC` plugin:

1. _Host:_ The vAccel RPC agent + vAccel + an acceleration plugin, to handle the
   forwarded calls and perform the actual acceleration
2. _Remote host:_ vAccel + the `RPC` plugin, to forward the application calls

## Preparing the host

If you have not already installed vAccel, install it
[from binaries](binaries.md) or [from source](building.md). The rest of this
guide assumes vAccel libraries exist in the standard library search paths.

### Installing vAccel RPC agent

vAccel RPC agent will handle the RPC requests and forward calls to the host
vAccel instance. You can find more information on how to install the
`vaccel-rpc-agent` binary at the
[relevant section](binaries.md#install-vaccel-agent).

## Preparing the remote host

As with the [host](#preparing-the-host) above, the remote host should also have
vAccel installed and the libraries should be in the standard library search
paths.

### Installing the `RPC` plugin

You can find instructions on how to install the `RPC` plugin in the
[relevant section](binaries.md#install-plugins). The rest of this guide assumes
the plugin exists in the standard library search paths.

## Running the vAccel RPC agent

Before executing the remote application, the agent must be running on the host.
The first thing to set is the address `vaccel-rpc-agent` will listen on:

```sh
export VACCEL_RPC_ADDRESS="tcp://0.0.0.0:65500"
```

This configures the agent to listen on the `65500` TCP port and all IPv4
addresses. You can replace the IP and the port above with the desired ones.

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
2025.04.07-17:19:53.56 - <debug> Initializing vAccel
2025.04.07-17:19:53.56 - <info> vAccel 0.6.1-194-19056528
2025.04.07-17:19:53.56 - <debug> Config:
2025.04.07-17:19:53.56 - <debug>   plugins = libvaccel-noop.so
2025.04.07-17:19:53.56 - <debug>   log_level = debug
2025.04.07-17:19:53.56 - <debug>   log_file = (null)
2025.04.07-17:19:53.56 - <debug>   profiling_enabled = false
2025.04.07-17:19:53.56 - <debug>   version_ignore = false
2025.04.07-17:19:53.56 - <debug> Created top-level rundir: /run/user/1002/vaccel/YvIPeM
2025.04.07-17:19:53.56 - <info> Registered plugin noop 0.6.1-194-19056528
2025.04.07-17:19:53.56 - <debug> Registered op noop from plugin noop
2025.04.07-17:19:53.56 - <debug> Registered op blas_sgemm from plugin noop
2025.04.07-17:19:53.56 - <debug> Registered op image_classify from plugin noop
2025.04.07-17:19:53.56 - <debug> Registered op image_detect from plugin noop
2025.04.07-17:19:53.56 - <debug> Registered op image_segment from plugin noop
2025.04.07-17:19:53.56 - <debug> Registered op image_pose from plugin noop
2025.04.07-17:19:53.56 - <debug> Registered op image_depth from plugin noop
2025.04.07-17:19:53.56 - <debug> Registered op exec from plugin noop
2025.04.07-17:19:53.56 - <debug> Registered op tf_session_load from plugin noop
2025.04.07-17:19:53.56 - <debug> Registered op tf_session_run from plugin noop
2025.04.07-17:19:53.56 - <debug> Registered op tf_session_delete from plugin noop
2025.04.07-17:19:53.56 - <debug> Registered op minmax from plugin noop
2025.04.07-17:19:53.56 - <debug> Registered op fpga_arraycopy from plugin noop
2025.04.07-17:19:53.56 - <debug> Registered op fpga_vectoradd from plugin noop
2025.04.07-17:19:53.56 - <debug> Registered op fpga_parallel from plugin noop
2025.04.07-17:19:53.56 - <debug> Registered op fpga_mmult from plugin noop
2025.04.07-17:19:53.56 - <debug> Registered op exec_with_resource from plugin noop
2025.04.07-17:19:53.56 - <debug> Registered op torch_jitload_forward from plugin noop
2025.04.07-17:19:53.56 - <debug> Registered op torch_sgemm from plugin noop
2025.04.07-17:19:53.56 - <debug> Registered op opencv from plugin noop
2025.04.07-17:19:53.56 - <debug> Registered op tflite_session_load from plugin noop
2025.04.07-17:19:53.56 - <debug> Registered op tflite_session_run from plugin noop
2025.04.07-17:19:53.56 - <debug> Registered op tflite_session_delete from plugin noop
2025.04.07-17:19:53.56 - <debug> Loaded plugin noop from libvaccel-noop.so
[2025-04-07T17:19:53Z INFO  ttrpc::sync::server] server listen started
[2025-04-07T17:19:53Z INFO  ttrpc::sync::server] server started
[2025-04-07T17:19:53Z INFO  vaccel_rpc_agent] vAccel RPC agent started
[2025-04-07T17:19:53Z INFO  vaccel_rpc_agent] Listening on 'tcp://0.0.0.0:65500', press Ctrl+C to exit
```

## Running the application on the remote host

With the vAccel RPC agent running, you are ready to execute the application in
the remote host.

On the remote host, you need to first configure the RPC address that will be
used by the plugin - replace `192.0.2.1` with the IP address of the host running
the vAccel RPC agent:

```sh
export VACCEL_RPC_ADDRESS="tcp://192.0.2.1:65500"
```

The port must be the same port you have used for starting the agent.

Next, configure vAccel to use the `RPC` plugin:

```console
export VACCEL_PLUGINS=libvaccel-rpc.so
```

Optionally, to get debug output:

```sh
export VACCEL_LOG_LEVEL=4
```

Finally, you can run an image classification example with:

```console
$ classify /usr/local/share/vaccel/images/example.jpg 1
2025.04.07-17:23:51.51 - <debug> Initializing vAccel
2025.04.07-17:23:51.51 - <info> vAccel 0.6.1-194-19056528
2025.04.07-17:23:51.51 - <debug> Config:
2025.04.07-17:23:51.51 - <debug>   plugins = /usr/local/lib/x86_64-linux-gnu/libvaccel-rpc.so
2025.04.07-17:23:51.51 - <debug>   log_level = debug
2025.04.07-17:23:51.51 - <debug>   log_file = (null)
2025.04.07-17:23:51.51 - <debug>   profiling_enabled = false
2025.04.07-17:23:51.51 - <debug>   version_ignore = false
2025.04.07-17:23:51.51 - <debug> Created top-level rundir: /run/user/1002/vaccel/2Qc6ZB
2025.04.07-17:23:51.51 - <info> Registered plugin rpc 0.1.0-36-bbffdae6
2025.04.07-17:23:51.51 - <debug> rpc is a VirtIO module
2025.04.07-17:23:51.51 - <debug> Registered op blas_sgemm from plugin rpc
2025.04.07-17:23:51.51 - <debug> Registered op image_classify from plugin rpc
2025.04.07-17:23:51.51 - <debug> Registered op image_detect from plugin rpc
2025.04.07-17:23:51.51 - <debug> Registered op image_segment from plugin rpc
2025.04.07-17:23:51.51 - <debug> Registered op image_depth from plugin rpc
2025.04.07-17:23:51.51 - <debug> Registered op image_pose from plugin rpc
2025.04.07-17:23:51.51 - <debug> Registered op tflite_session_load from plugin rpc
2025.04.07-17:23:51.51 - <debug> Registered op tflite_session_delete from plugin rpc
2025.04.07-17:23:51.51 - <debug> Registered op tflite_session_run from plugin rpc
2025.04.07-17:23:51.51 - <debug> Registered op minmax from plugin rpc
2025.04.07-17:23:51.51 - <debug> Registered op fpga_arraycopy from plugin rpc
2025.04.07-17:23:51.51 - <debug> Registered op fpga_mmult from plugin rpc
2025.04.07-17:23:51.51 - <debug> Registered op fpga_vectoradd from plugin rpc
2025.04.07-17:23:51.51 - <debug> Registered op fpga_parallel from plugin rpc
2025.04.07-17:23:51.51 - <debug> Registered op exec from plugin rpc
2025.04.07-17:23:51.51 - <debug> Registered op exec_with_resource from plugin rpc
2025.04.07-17:23:51.51 - <debug> Registered op torch_jitload_forward from plugin rpc
2025.04.07-17:23:51.51 - <debug> Registered op opencv from plugin rpc
2025.04.07-17:23:51.51 - <debug> Registered op tf_session_load from plugin rpc
2025.04.07-17:23:51.51 - <debug> Registered op tf_session_delete from plugin rpc
2025.04.07-17:23:51.51 - <debug> Registered op tf_session_run from plugin rpc
2025.04.07-17:23:51.51 - <debug> Loaded plugin rpc from /usr/local/lib/x86_64-linux-gnu/libvaccel-rpc.so
2025.04.07-17:23:51.51 - <debug> [rpc] Initializing new remote session
2025.04.07-17:23:51.51 - <debug> [rpc] Initialized remote session 1
2025.04.07-17:23:51.51 - <debug> New rundir for session 1: /run/user/1002/vaccel/2Qc6ZB/session.1
2025.04.07-17:23:51.51 - <debug> Initialized session 1 with remote (id: 1)
Initialized session with id: 1
2025.04.07-17:23:51.51 - <debug> session:1 Looking for plugin implementing VACCEL_OP_IMAGE_CLASSIFY
2025.04.07-17:23:51.51 - <debug> Returning func from hint plugin rpc
2025.04.07-17:23:51.51 - <debug> Found implementation in rpc plugin
classification tags: This is a dummy classification tag!
classification imagename: This is a dummy imgname!
2025.04.07-17:23:51.55 - <debug> [rpc] Releasing remote session 1
2025.04.07-17:23:51.64 - <debug> Released session 1
2025.04.07-17:23:51.64 - <debug> Cleaning up vAccel
2025.04.07-17:23:51.64 - <debug> Cleaning up sessions
2025.04.07-17:23:51.64 - <debug> Cleaning up resources
2025.04.07-17:23:51.64 - <debug> Cleaning up plugins
2025.04.07-17:23:51.64 - <debug> Unregistered plugin rpc
```

In the host terminal, where the vAccel RPC agent is running, you should also see
the corresponding host vAccel output:

```console
2025.04.07-17:23:51.51 - <debug> New rundir for session 1: /run/user/1002/vaccel/YvIPeM/session.1
2025.04.07-17:23:51.51 - <debug> Initialized session 1
[2025-04-07T17:23:51Z INFO  vaccel_rpc_agent::session] Created session 1
[2025-04-07T17:23:51Z INFO  vaccel_rpc_agent::ops::genop] Genop session 1
2025.04.07-17:23:51.51 - <debug> session:1 Looking for plugin implementing VACCEL_OP_IMAGE_CLASSIFY
2025.04.07-17:23:51.51 - <debug> Returning func from hint plugin noop
2025.04.07-17:23:51.51 - <debug> Found implementation in noop plugin
2025.04.07-17:23:51.51 - <debug> [noop] Calling Image classification for session 1
2025.04.07-17:23:51.51 - <debug> [noop] Dumping arguments for Image classification:
2025.04.07-17:23:51.51 - <debug> [noop] model: (null)
2025.04.07-17:23:51.51 - <debug> [noop] len_img: 79281
2025.04.07-17:23:51.51 - <debug> [noop] len_out_text: 512
2025.04.07-17:23:51.51 - <debug> [noop] len_out_imgname: 512
2025.04.07-17:23:51.51 - <debug> [noop] will return a dummy result
2025.04.07-17:23:51.51 - <debug> [noop] will return a dummy result
2025.04.07-17:23:51.60 - <debug> Released session 1
[2025-04-07T17:23:51Z INFO  vaccel_rpc_agent::session] Destroyed session 1
```

If you compare the application output with the
[native execution case](build-run-app.md#running-a-vaccel-application) ignoring
the vAccel log messages, you will notice that it is identical:

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
# FIXME
```

whereas in the the remote execution case, the `RPC` plugin is used on the remote
host:

```console
$ classify /usr/local/share/vaccel/images/example.jpg 1
2025.04.07-17:23:51.51 - <debug> Initializing vAccel
2025.04.07-17:23:51.51 - <info> vAccel 0.6.1-194-19056528
2025.04.07-17:23:51.51 - <debug> Config:
2025.04.07-17:23:51.51 - <debug>   plugins = /usr/local/lib/x86_64-linux-gnu/libvaccel-rpc.so
2025.04.07-17:23:51.51 - <debug>   log_level = debug
2025.04.07-17:23:51.51 - <debug>   log_file = (null)
2025.04.07-17:23:51.51 - <debug>   profiling_enabled = false
2025.04.07-17:23:51.51 - <debug>   version_ignore = false
2025.04.07-17:23:51.51 - <debug> Created top-level rundir: /run/user/1002/vaccel/2Qc6ZB
2025.04.07-17:23:51.51 - <info> Registered plugin rpc 0.1.0-36-bbffdae6
2025.04.07-17:23:51.51 - <debug> rpc is a VirtIO module
...
2025.04.07-17:23:51.51 - <debug> Loaded plugin rpc from /usr/local/lib/x86_64-linux-gnu/libvaccel-rpc.so
2025.04.07-17:23:51.51 - <debug> [rpc] Initializing new remote session
2025.04.07-17:23:51.51 - <debug> [rpc] Initialized remote session 1
...
2025.04.07-17:23:51.51 - <debug> Returning func from hint plugin rpc
2025.04.07-17:23:51.51 - <debug> Found implementation in rpc plugin
...
2025.04.07-17:23:51.55 - <debug> [rpc] Releasing remote session 1
```

while the `NoOp` plugin is used on the host:

```console
$ VACCEL_BOOTSTRAP_ENABLED=0 vaccel-rpc-agent \
      -a "${VACCEL_RPC_ADDRESS}" \
      --vaccel-config "plugins=libvaccel-noop.so,log_level=4"
2025.04.07-17:19:53.56 - <debug> Initializing vAccel
2025.04.07-17:19:53.56 - <info> vAccel 0.6.1-194-19056528
2025.04.07-17:19:53.56 - <debug> Config:
2025.04.07-17:19:53.56 - <debug>   plugins = libvaccel-noop.so
2025.04.07-17:19:53.56 - <debug>   log_level = debug
2025.04.07-17:19:53.56 - <debug>   log_file = (null)
2025.04.07-17:19:53.56 - <debug>   profiling_enabled = false
2025.04.07-17:19:53.56 - <debug>   version_ignore = false
2025.04.07-17:19:53.56 - <debug> Created top-level rundir: /run/user/1002/vaccel/YvIPeM
2025.04.07-17:19:53.56 - <info> Registered plugin noop 0.6.1-194-19056528
...
2025.04.07-17:19:53.56 - <debug> Loaded plugin noop from libvaccel-noop.so
...
2025.04.07-17:23:51.51 - <debug> Returning func from hint plugin noop
2025.04.07-17:23:51.51 - <debug> Found implementation in noop plugin
2025.04.07-17:23:51.51 - <debug> [noop] Calling Image classification for session 1
2025.04.07-17:23:51.51 - <debug> [noop] Dumping arguments for Image classification:
2025.04.07-17:23:51.51 - <debug> [noop] model: (null)
2025.04.07-17:23:51.51 - <debug> [noop] len_img: 79281
2025.04.07-17:23:51.51 - <debug> [noop] len_out_text: 512
2025.04.07-17:23:51.51 - <debug> [noop] len_out_imgname: 512
2025.04.07-17:23:51.51 - <debug> [noop] will return a dummy result
2025.04.07-17:23:51.51 - <debug> [noop] will return a dummy result
```
