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
2026.04.29-14:47:14.89 - <debug> Initializing vAccel
2026.04.29-14:47:14.89 - <info> vAccel 0.7.1-93-ebc23b1f
2026.04.29-14:47:14.89 - <debug> Config:
2026.04.29-14:47:14.89 - <debug>   plugins = libvaccel-mbench.so
2026.04.29-14:47:14.89 - <debug>   log_level = debug
2026.04.29-14:47:14.89 - <debug>   log_file = (null)
2026.04.29-14:47:14.89 - <debug>   profiling_enabled = true
2026.04.29-14:47:14.89 - <debug>   version_ignore = false
2026.04.29-14:47:14.89 - <debug> Created top-level rundir: /run/user/0/vaccel/FTqcMb
2026.04.29-14:47:14.89 - <info> Registered plugin mbench 0.7.1-93-ebc23b1f
2026.04.29-14:47:14.89 - <debug> Registered op exec from plugin mbench
2026.04.29-14:47:14.89 - <debug> Loaded plugin mbench from libvaccel-mbench.so
2026.04.29-14:47:14.89 - <debug> New rundir for session 1: /run/user/0/vaccel/FTqcMb/session.1
2026.04.29-14:47:14.89 - <debug> Initialized session 1 with plugin mbench
Initialized session with id: 1
2026.04.29-14:47:14.89 - <debug> Start profiling region mbench
2026.04.29-14:47:14.89 - <debug> session:1 Looking for func implementing op exec
2026.04.29-14:47:14.89 - <debug> Start profiling region vaccel_exec_op
2026.04.29-14:47:14.89 - <debug> Returning func for op exec from plugin mbench
2026.04.29-14:47:14.89 - <debug> Calling mbench for session 1
2026.04.29-14:47:14.89 - <debug> Start profiling region vaccel_mbench_plugin
2026.04.29-14:47:14.90 - <debug> [mbench] 10 ms elapsed
2026.04.29-14:47:14.90 - <debug> Stop profiling region vaccel_mbench_plugin
2026.04.29-14:47:14.90 - <debug> Stop profiling region vaccel_exec_op
2026.04.29-14:47:14.90 - <debug> Stop profiling region mbench
2026.04.29-14:47:14.90 - <debug> Released session 1
2026.04.29-14:47:14.90 - <info> [prof] mbench: total_time: 10026978 nsec nr_entries: 1
2026.04.29-14:47:14.90 - <debug> Cleaning up vAccel
2026.04.29-14:47:14.90 - <debug> Cleaning up sessions
2026.04.29-14:47:14.90 - <debug> Cleaning up resources
2026.04.29-14:47:14.90 - <debug> Cleaning up plugins
2026.04.29-14:47:14.90 - <info> [prof] vaccel_mbench_plugin: total_time: 10008901 nsec nr_entries: 1
2026.04.29-14:47:14.90 - <debug> Unregistered plugin mbench
```
