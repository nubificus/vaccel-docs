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
$ exec_with_res "$(pkg-config --variable=libdir vaccel)/libmytestlib.so"
2025.04.15-19:37:37.77 - <debug> Initializing vAccel
2025.04.15-19:37:37.77 - <info> vAccel 0.6.1-194-19056528
2025.04.15-19:37:37.77 - <debug> Config:
2025.04.15-19:37:37.77 - <debug>   plugins = libvaccel-exec.so
2025.04.15-19:37:37.77 - <debug>   log_level = debug
2025.04.15-19:37:37.77 - <debug>   log_file = (null)
2025.04.15-19:37:37.77 - <debug>   profiling_enabled = false
2025.04.15-19:37:37.77 - <debug>   version_ignore = false
2025.04.15-19:37:37.77 - <debug> Created top-level rundir: /run/user/1002/vaccel/DYBt4h
2025.04.15-19:37:37.77 - <info> Registered plugin exec 0.6.1-194-19056528
2025.04.15-19:37:37.77 - <debug> Registered op noop from plugin exec
2025.04.15-19:37:37.77 - <debug> Registered op exec from plugin exec
2025.04.15-19:37:37.77 - <debug> Registered op exec_with_resource from plugin exec
2025.04.15-19:37:37.77 - <debug> Loaded plugin exec from libvaccel-exec.so
2025.04.15-19:37:37.77 - <warn> Path does not seem to have a `<prefix>://`
2025.04.15-19:37:37.77 - <warn> Assuming /usr/local/lib/x86_64-linux-gnu/libmytestlib.so is a local path
2025.04.15-19:37:37.77 - <debug> Initialized resource 1
2025.04.15-19:37:37.77 - <debug> New rundir for session 1: /run/user/1002/vaccel/DYBt4h/session.1
2025.04.15-19:37:37.77 - <debug> Initialized session 1
Initialized session with id: 1
2025.04.15-19:37:37.77 - <debug> New rundir for resource 1: /run/user/1002/vaccel/DYBt4h/resource.1
2025.04.15-19:37:37.77 - <debug> session:1 Registered resource 1
2025.04.15-19:37:37.77 - <debug> New rundir for resource 2: /run/user/1002/vaccel/DYBt4h/resource.2
2025.04.15-19:37:37.77 - <debug> Persisting file lib.so to /run/user/1002/vaccel/DYBt4h/resource.2/lib.so
2025.04.15-19:37:37.77 - <debug> Initialized resource 2
2025.04.15-19:37:37.77 - <debug> session:1 Registered resource 2
2025.04.15-19:37:37.77 - <debug> session:1 Looking for plugin implementing exec with resource
2025.04.15-19:37:37.77 - <debug> Returning func from hint plugin exec
2025.04.15-19:37:37.77 - <debug> Found implementation in exec plugin
2025.04.15-19:37:37.77 - <debug> [exec_with_resource] session:1 Calling exec_with_resource
2025.04.15-19:37:37.77 - <debug> [exec_with_resource] Number of libraries: 1
2025.04.15-19:37:37.77 - <debug> [exec_with_resource] Library: /usr/local/lib/x86_64-linux-gnu/libmytestlib.so
2025.04.15-19:37:37.77 - <debug> [exec_with_resource] Symbol: mytestfunc
2025.04.15-19:37:37.77 - <debug> [exec_with_resource] read[0].size: 4
2025.04.15-19:37:37.77 - <debug> [exec_with_resource] read[0].argtype: 42
2025.04.15-19:37:37.77 - <debug> [exec_with_resource] write[0].size: 4
2025.04.15-19:37:37.77 - <debug> [exec_with_resource] write[0].argtype: 42
I got nr_in: 1, nr_out: 1
I got input: 10
Will return output: 20
output1: 20
2025.04.15-19:37:37.77 - <debug> session:1 Looking for plugin implementing exec with resource
2025.04.15-19:37:37.77 - <debug> Returning func from hint plugin exec
2025.04.15-19:37:37.77 - <debug> Found implementation in exec plugin
2025.04.15-19:37:37.77 - <debug> [exec_with_resource] session:1 Calling exec_with_resource
2025.04.15-19:37:37.77 - <debug> [exec_with_resource] Number of libraries: 1
2025.04.15-19:37:37.77 - <debug> [exec_with_resource] Library: /run/user/1002/vaccel/DYBt4h/resource.2/lib.so
2025.04.15-19:37:37.77 - <debug> [exec_with_resource] Symbol: mytestfunc
2025.04.15-19:37:37.77 - <debug> [exec_with_resource] read[0].size: 4
2025.04.15-19:37:37.77 - <debug> [exec_with_resource] read[0].argtype: 0
2025.04.15-19:37:37.77 - <debug> [exec_with_resource] write[0].size: 4
2025.04.15-19:37:37.77 - <debug> [exec_with_resource] write[0].argtype: 0
I got nr_in: 1, nr_out: 1
I got input: 10
Will return output: 20
output2: 20
2025.04.15-19:37:37.77 - <debug> session:1 Unregistered resource 2
2025.04.15-19:37:37.77 - <debug> Removing file /run/user/1002/vaccel/DYBt4h/resource.2/lib.so
2025.04.15-19:37:37.77 - <debug> Released resource 2
2025.04.15-19:37:37.77 - <debug> session:1 Unregistered resource 1
2025.04.15-19:37:37.77 - <debug> Released session 1
2025.04.15-19:37:37.77 - <debug> Released resource 1
2025.04.15-19:37:37.77 - <debug> Cleaning up vAccel
2025.04.15-19:37:37.77 - <debug> Cleaning up sessions
2025.04.15-19:37:37.77 - <debug> Cleaning up resources
2025.04.15-19:37:37.77 - <debug> Cleaning up plugins
2025.04.15-19:37:37.77 - <debug> Unregistered plugin exec
```
