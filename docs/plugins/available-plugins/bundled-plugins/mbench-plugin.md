# MBench Plugin

The MBench plugin for vAccel is microbenchmark plugin to measure operation
overhead by simulating compute intensive workloads.

## Supported operations

- [Exec](../../../api/api-reference/operations.md#exec)

## Installing the plugin

The plugin comes bundled with the core vAccel installation. Find out more on how
to install vAccel at the
[Installation](../../../getting-started/installation.md) page.

## Usage

To specify MBench plugin as the selected plugin for vAccel execution:

```sh
export VACCEL_PLUGINS=libvaccel-mbench.so
```

Ensure vAccel and the MBench plugin libraries are in the library search paths
before trying to use the plugin.

To get actual meauserement, you will probably also want to enable profiling:

```sh
export VACCEL_PROFILING_ENABLED=1
```

## Running an example

Export the necessary variables for the plugin:

```sh
export VACCEL_PLUGINS=libvaccel-mbench.so
export VACCEL_PROFILING_ENABLED=1
# Optionally, for verbose output
export VACCEL_LOG_LEVEL=4
```

Assuming vAccel is installed at `/usr/local`, you can run an example to simulate
10ms of CPU usage for `example.jpg` with:

```console
$ mbench 10 /usr/local/share/vaccel/images/example.jpg
2025.04.15-19:55:11.29 - <debug> Initializing vAccel
2025.04.15-19:55:11.29 - <info> vAccel 0.6.1-194-19056528
2025.04.15-19:55:11.29 - <debug> Config:
2025.04.15-19:55:11.29 - <debug>   plugins = libvaccel-mbench.so
2025.04.15-19:55:11.29 - <debug>   log_level = debug
2025.04.15-19:55:11.29 - <debug>   log_file = (null)
2025.04.15-19:55:11.29 - <debug>   profiling_enabled = true
2025.04.15-19:55:11.29 - <debug>   version_ignore = false
2025.04.15-19:55:11.29 - <debug> Created top-level rundir: /run/user/1002/vaccel/19PFGM
2025.04.15-19:55:11.29 - <info> Registered plugin mbench 0.6.1-194-19056528
2025.04.15-19:55:11.29 - <debug> Registered op exec from plugin mbench
2025.04.15-19:55:11.29 - <debug> Loaded plugin mbench from libvaccel-mbench.so
2025.04.15-19:55:11.29 - <debug> New rundir for session 1: /run/user/1002/vaccel/19PFGM/session.1
2025.04.15-19:55:11.29 - <debug> Initialized session 1
Initialized session with id: 1
2025.04.15-19:55:11.29 - <debug> Start profiling region mbench
2025.04.15-19:55:11.29 - <debug> session:1 Looking for plugin implementing exec
2025.04.15-19:55:11.29 - <debug> Start profiling region vaccel_exec_op
2025.04.15-19:55:11.29 - <debug> Returning func from hint plugin mbench
2025.04.15-19:55:11.29 - <debug> Found implementation in mbench plugin
2025.04.15-19:55:11.29 - <debug> Calling mbench for session 1
2025.04.15-19:55:11.29 - <debug> Start profiling region vaccel_mbench_plugin
2025.04.15-19:55:11.30 - <debug> [mbench] 10 ms elapsed
2025.04.15-19:55:11.30 - <debug> Stop profiling region vaccel_mbench_plugin
2025.04.15-19:55:11.30 - <debug> Stop profiling region vaccel_exec_op
2025.04.15-19:55:11.30 - <debug> Stop profiling region mbench
2025.04.15-19:55:11.30 - <debug> Released session 1
2025.04.15-19:55:11.30 - <info> [prof] mbench: total_time: 10060333 nsec nr_entries: 1
2025.04.15-19:55:11.30 - <info> [prof] vaccel_exec_op: total_time: 10040877 nsec nr_entries: 1
2025.04.15-19:55:11.30 - <debug> Cleaning up vAccel
2025.04.15-19:55:11.30 - <debug> Cleaning up sessions
2025.04.15-19:55:11.30 - <debug> Cleaning up resources
2025.04.15-19:55:11.30 - <debug> Cleaning up plugins
2025.04.15-19:55:11.30 - <info> [prof] vaccel_mbench_plugin: total_time: 10010329 nsec nr_entries: 1
2025.04.15-19:55:11.30 - <debug> Unregistered plugin mbench
```
