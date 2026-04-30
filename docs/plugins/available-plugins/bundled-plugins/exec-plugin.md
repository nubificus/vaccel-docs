# Exec Plugin

The Exec plugin for vAccel implements a backend to call functions from external
libraries using vAccel operations.

<!-- markdownlint-disable code-block-style -->

!!! warning

    This plugin enables users to call functions from arbitrary libraries.
    Use it only on environments where the users are trusted.

## Supported operations

- [Exec](../../../api/api-reference/operations.md#exec)
- [Exec with resource](../../../api/api-reference/operations.md#exec-with-resource)
- [Debug operation](../../../api/api-reference/operations.md#debug-operation)

## Installing the plugin

The plugin comes bundled with the core vAccel installation. Find out more on how
to install vAccel at the
[Installation](../../../getting-started/installation.md) page.

## Usage

To specify Exec plugin as the selected plugin for vAccel execution:

```sh
export VACCEL_PLUGINS=libvaccel-exec.so
```

Ensure vAccel and the Exec plugin libraries are in the library search paths
before trying to use the plugin.

## Running an example

Export the necessary variables for the plugin:

```sh
export VACCEL_PLUGINS=libvaccel-exec.so
# Optionally, for verbose output
export VACCEL_LOG_LEVEL=4
```

Assuming `pkg-config` is available, you can call `mytestfunc` from the provided
`libmytestlib.so` with:

```console
$ exec_with_resource "$(pkg-config --variable=libdir vaccel)/libmytestlib.so"
2026.04.29-14:45:52.60 - <debug> Initializing vAccel
2026.04.29-14:45:52.60 - <info> vAccel 0.7.1-93-ebc23b1f
2026.04.29-14:45:52.60 - <debug> Config:
2026.04.29-14:45:52.60 - <debug>   plugins = libvaccel-exec.so
2026.04.29-14:45:52.60 - <debug>   log_level = debug
2026.04.29-14:45:52.60 - <debug>   log_file = (null)
2026.04.29-14:45:52.60 - <debug>   profiling_enabled = false
2026.04.29-14:45:52.60 - <debug>   version_ignore = false
2026.04.29-14:45:52.60 - <debug> Created top-level rundir: /run/user/0/vaccel/WHJlSC
2026.04.29-14:45:52.60 - <info> Registered plugin exec 0.7.1-93-ebc23b1f
2026.04.29-14:45:52.60 - <debug> Registered op noop from plugin exec
2026.04.29-14:45:52.60 - <debug> Registered op exec from plugin exec
2026.04.29-14:45:52.60 - <debug> Registered op exec_with_resource from plugin exec
2026.04.29-14:45:52.60 - <debug> Loaded plugin exec from libvaccel-exec.so
2026.04.29-14:45:52.60 - <warn> Path does not seem to have a `<prefix>://`
2026.04.29-14:45:52.60 - <warn> Assuming /usr/local/lib/x86_64-linux-gnu/libmytestlib.so is a local path
2026.04.29-14:45:52.60 - <debug> Initialized resource 1
2026.04.29-14:45:52.60 - <debug> New rundir for session 1: /run/user/0/vaccel/WHJlSC/session.1
2026.04.29-14:45:52.60 - <debug> Initialized session 1 with plugin exec
Initialized session with id: 1
2026.04.29-14:45:52.60 - <debug> New rundir for resource 1: /run/user/0/vaccel/WHJlSC/resource.1
2026.04.29-14:45:52.60 - <debug> session:1 Registered resource 1
2026.04.29-14:45:52.60 - <debug> New rundir for resource 2: /run/user/0/vaccel/WHJlSC/resource.2
2026.04.29-14:45:52.60 - <debug> Persisting file lib.so to /run/user/0/vaccel/WHJlSC/resource.2/lib.so
2026.04.29-14:45:52.60 - <debug> Initialized resource 2
2026.04.29-14:45:52.60 - <debug> session:1 Registered resource 2
2026.04.29-14:45:52.60 - <debug> session:1 Looking for func implementing op exec_with_resource
2026.04.29-14:45:52.60 - <debug> Returning func for op exec_with_resource from plugin exec
2026.04.29-14:45:52.60 - <debug> [exec] session:1 Calling exec_with_resource
2026.04.29-14:45:52.60 - <debug> [exec] Number of libraries: 1
2026.04.29-14:45:52.60 - <debug> [exec] Library: /usr/local/lib/x86_64-linux-gnu/libmytestlib.so
2026.04.29-14:45:52.60 - <debug> [exec] Symbol: mytestfunc
2026.04.29-14:45:52.60 - <debug> [exec] read[0].size: 4
2026.04.29-14:45:52.60 - <debug> [exec] read[0].type: int32
2026.04.29-14:45:52.60 - <debug> [exec] write[0].size: 4
2026.04.29-14:45:52.60 - <debug> [exec] write[0].type: int32
I got nr_in: 1, nr_out: 1
I got input: 10
Will return output: 20
output1: 20
2026.04.29-14:45:52.60 - <debug> session:1 Looking for func implementing op exec_with_resource
2026.04.29-14:45:52.60 - <debug> Returning func for op exec_with_resource from plugin exec
2026.04.29-14:45:52.60 - <debug> [exec] session:1 Calling exec_with_resource
2026.04.29-14:45:52.60 - <debug> [exec] Number of libraries: 1
2026.04.29-14:45:52.60 - <debug> [exec] Library: /run/user/0/vaccel/WHJlSC/resource.2/lib.so
2026.04.29-14:45:52.60 - <debug> [exec] Symbol: mytestfunc
2026.04.29-14:45:52.60 - <debug> [exec] read[0].size: 4
2026.04.29-14:45:52.60 - <debug> [exec] read[0].type: int32
2026.04.29-14:45:52.60 - <debug> [exec] write[0].size: 4
2026.04.29-14:45:52.60 - <debug> [exec] write[0].type: int32
I got nr_in: 1, nr_out: 1
I got input: 10
Will return output: 20
output2: 20
2026.04.29-14:45:52.60 - <debug> session:1 Unregistered resource 2
2026.04.29-14:45:52.60 - <debug> Removing file /run/user/0/vaccel/WHJlSC/resource.2/lib.so
2026.04.29-14:45:52.60 - <debug> Released resource 2
2026.04.29-14:45:52.60 - <debug> session:1 Unregistered resource 1
2026.04.29-14:45:52.60 - <debug> Released session 1
2026.04.29-14:45:52.60 - <debug> Released resource 1
2026.04.29-14:45:52.60 - <debug> Cleaning up vAccel
2026.04.29-14:45:52.60 - <debug> Cleaning up sessions
2026.04.29-14:45:52.60 - <debug> Cleaning up resources
2026.04.29-14:45:52.60 - <debug> Cleaning up plugins
2026.04.29-14:45:52.60 - <debug> Unregistered plugin exec
```
