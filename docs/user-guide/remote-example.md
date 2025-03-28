# Run a vAccel application remotely

## Overview

As with the [VM case](vm-example.md), using the `vsock` plugin, allows us to run
vAccel applications in remote Hosts. Figure 1 shows the execution flow: Our code
resides in the `Remote Host`, and uses the `libvaccel-vsock.so` plugin,
specifying the Host and Port parameters of the vAccel agent, running on the Host
where the hardware accelerator resides; the vAccel agent, intercepts vAccel API
operations, and issues calls to the vAccel library, that, in turn, translates
these calls to the relevant, user-specified plugin.

<figure>
  <img src="/img/vaccel-remote-flow.png" width="800" align=left
    alt="Remote application execution flow" />
  <figcaption>Figure 1. Remote application execution flow</figcaption>
</figure>

Section [Running the agent](#running-the-vaccel-agent) describes the process to
run the agent.

To proceed with this example, we need to install the
[vAccel core library](binaries.md#install-vaccel-core-library) in both machines,
and:

- the [vAccel agent](binaries.md#install-vaccel-agent) in the Host machine that
  holds the hardware accelerator,
- the [VSOCK plugin](binaries.md#install-plugins) in the remote Host machine
  that we want to run our vAccel application.

## Running the vAccel agent

The `vaccel-agent` is just another vAccel application. It consumes the vAccel
API like any other app, with the additional value of being able to receive
commands via `ttrpc`. So we need to include the path to `libvaccel.so` in the
`LD_LIBRARY_PATH` variable, and specify the plugin we want to use via the
`VACCEL_BACKENDS` variable. The agent currently supports three socket types:
`UNIX`, `VSOCK`, and `TCP`. In this example, we are using the `TCP` socket type.

To run the agent on host we use the following commands:

```bash
export VACCEL_PLUGINS=/usr/local/lib/x86_64-linux-gnu/libvaccel-noop.so
export VACCEL_LOG_LEVEL=4
export ADDRESS=tcp://127.0.0.1:65500

vaccel-rpc-agent -a "${ADDRESS}"
```

You should be presented with the following output:
```console
2025.03.23-13:06:34.56 - <debug> Initializing vAccel
2025.03.23-13:06:34.56 - <info> vAccel 0.6.1-194-19056528-dirty
2025.03.23-13:06:34.56 - <debug> Config:
2025.03.23-13:06:34.56 - <debug>   plugins = /usr/local/lib/x86_64-linux-gnu/libvaccel-noop.so
2025.03.23-13:06:34.56 - <debug>   log_level = debug
2025.03.23-13:06:34.56 - <debug>   log_file = (null)
2025.03.23-13:06:34.56 - <debug>   profiling_enabled = false
2025.03.23-13:06:34.56 - <debug>   version_ignore = false
2025.03.23-13:06:34.56 - <debug> Created top-level rundir: /run/user/1008/vaccel/RAIcDI
2025.03.23-13:06:34.56 - <info> Registered plugin noop 0.6.1-194-19056528-dirty
2025.03.23-13:06:34.56 - <debug> Registered op noop from plugin noop
2025.03.23-13:06:34.56 - <debug> Registered op blas_sgemm from plugin noop
2025.03.23-13:06:34.56 - <debug> Registered op image_classify from plugin noop
2025.03.23-13:06:34.56 - <debug> Registered op image_detect from plugin noop
2025.03.23-13:06:34.56 - <debug> Registered op image_segment from plugin noop
2025.03.23-13:06:34.56 - <debug> Registered op image_pose from plugin noop
2025.03.23-13:06:34.56 - <debug> Registered op image_depth from plugin noop
2025.03.23-13:06:34.56 - <debug> Registered op exec from plugin noop
2025.03.23-13:06:34.56 - <debug> Registered op tf_session_load from plugin noop
2025.03.23-13:06:34.56 - <debug> Registered op tf_session_run from plugin noop
2025.03.23-13:06:34.56 - <debug> Registered op tf_session_delete from plugin noop
2025.03.23-13:06:34.56 - <debug> Registered op minmax from plugin noop
2025.03.23-13:06:34.56 - <debug> Registered op fpga_arraycopy from plugin noop
2025.03.23-13:06:34.56 - <debug> Registered op fpga_vectoradd from plugin noop
2025.03.23-13:06:34.56 - <debug> Registered op fpga_parallel from plugin noop
2025.03.23-13:06:34.56 - <debug> Registered op fpga_mmult from plugin noop
2025.03.23-13:06:34.56 - <debug> Registered op exec_with_resource from plugin noop
2025.03.23-13:06:34.56 - <debug> Registered op torch_jitload_forward from plugin noop
2025.03.23-13:06:34.56 - <debug> Registered op torch_sgemm from plugin noop
2025.03.23-13:06:34.56 - <debug> Registered op opencv from plugin noop
2025.03.23-13:06:34.56 - <debug> Registered op tflite_session_load from plugin noop
2025.03.23-13:06:34.56 - <debug> Registered op tflite_session_run from plugin noop
2025.03.23-13:06:34.56 - <debug> Registered op tflite_session_delete from plugin noop
2025.03.23-13:06:34.56 - <debug> Registered op foo from plugin noop
2025.03.23-13:06:34.56 - <debug> Loaded plugin noop from /usr/local/lib/x86_64-linux-gnu/libvaccel-noop.so
[2025-03-23T13:06:34Z INFO  ttrpc::sync::server] server listen started
[2025-03-23T13:06:34Z INFO  ttrpc::sync::server] server started
[2025-03-23T13:06:34Z INFO  vaccel_rpc_agent] vAccel RPC agent started
[2025-03-23T13:06:34Z INFO  vaccel_rpc_agent] Listening on 'tcp://127.0.0.1:65500', press Ctrl+C to exit
```

To run an application on guest, open a new terminal:
```console
export VACCEL_PLUGINS=/usr/local/lib/x86_64-linux-gnu/libvaccel-rpc.so
export VACCEL_RPC_ADDRESS=tcp://127.0.0.1:65500

classify /usr/local/share/vaccel/images/example.jpg 1
```
The output on guest is:
```
Initialized session with id: 1
classification tags: This is a dummy classification tag!
```

While on host:
```
...
2025.03.23-13:07:02.97 - <debug> New rundir for session 1: /run/user/1008/vaccel/RAIcDI/session.1
2025.03.23-13:07:02.97 - <debug> Initialized session 1
[2025-03-23T13:07:02Z INFO  vaccel_rpc_agent::session] Created session 1
[2025-03-23T13:07:02Z INFO  vaccel_rpc_agent::ops::genop] Genop session 1
2025.03.23-13:07:02.97 - <debug> session:1 Looking for plugin implementing VACCEL_OP_IMAGE_CLASSIFY
2025.03.23-13:07:02.97 - <debug> Returning func from hint plugin noop
2025.03.23-13:07:02.97 - <debug> Found implementation in noop plugin
2025.03.23-13:07:02.97 - <debug> [noop] Calling Image classification for session 1
2025.03.23-13:07:02.97 - <debug> [noop] Dumping arguments for Image classification:
2025.03.23-13:07:02.97 - <debug> [noop] model: (null)
2025.03.23-13:07:02.97 - <debug> [noop] len_img: 79281
2025.03.23-13:07:02.97 - <debug> [noop] len_out_text: 512
2025.03.23-13:07:02.97 - <debug> [noop] len_out_imgname: 512
2025.03.23-13:07:02.97 - <debug> [noop] will return a dummy result
2025.03.23-13:07:02.97 - <debug> [noop] will return a dummy result
2025.03.23-13:07:03.06 - <debug> Released session 1
[2025-03-23T13:07:03Z INFO  vaccel_rpc_agent::session] Destroyed session 1
```

## Running the application in the remote Host

In the remote Host, we will be running a vAccel application; so we need to
specify the path to `libvaccel.so` and the plugin to be used. We need to set the
paths to the vAccel core library and the `VSOCK` plugin. Additionally, we need
to set `VACCEL_VSOCK`, to point to the remote endpoint.

The vAccel examples are included in the vAccel core library installation at
`/usr/local/bin`. So, assuming the agent is running in the Host machine, the
only thing needed is to set the paths and execute the example:

```console
### Set the library path and the plugin
$ export LD_LIBRARY_PATH=/usr/local/lib
$ export VACCEL_BACKENDS=/usr/local/lib/libvaccel-vsock.so

### Set the remote endpoint
### no DNS resolving for now, just use IP Addresses
$ export VACCEL_VSOCK=tcp://192.168.254.1:8194

### Get an image:
### eg. wget https://i.imgur.com/aSuOWgU.jpeg -O cat.jpeg
### and run the example
$ /usr/local/bin/classify cat.jpeg 1
Initialized session with id: 1
Image size: 54372B
classification tags: This is a dummy classification tag!
```

We got the same output as with the
[native execution case](build-run-app.md#running-a-vaccel-application). Well,
almost the same; what we missed is the plugin output. See the native execution
case below:

The `[noop]` lines are not present when running from the remote machine. This is
because the plugin is executing in the remote Host. We only get the
`classification tags:` result back. If you look at the other terminal, where the
agent is running, you should see the following:

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
