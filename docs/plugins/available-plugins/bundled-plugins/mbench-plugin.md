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
$ VACCEL_PLUGINS=libvaccel-mbench.so VACCEL_PROFILING_ENABLED=1 VACCEL_LOG_LEVEL=4 mbench 10 /usr/local/share/vaccel/images/example.jpg
2026.04.29-00:55:09.97 - <debug> Initializing vAccel
2026.04.29-00:55:09.97 - <info> vAccel 0.7.1-93-ebc23b1f
2026.04.29-00:55:09.97 - <debug> Config:
2026.04.29-00:55:09.97 - <debug>   plugins = libvaccel-mbench.so
2026.04.29-00:55:09.97 - <debug>   log_level = debug
2026.04.29-00:55:09.97 - <debug>   log_file = (null)
2026.04.29-00:55:09.97 - <debug>   profiling_enabled = true
2026.04.29-00:55:09.97 - <debug>   version_ignore = false
2026.04.29-00:55:09.97 - <debug> Created top-level rundir: /run/user/0/vaccel/yBMakt
2026.04.29-00:55:09.97 - <info> Registered plugin mbench 0.7.1-93-ebc23b1f
2026.04.29-00:55:09.97 - <debug> Registered op exec from plugin mbench
2026.04.29-00:55:09.97 - <debug> Loaded plugin mbench from libvaccel-mbench.so
2026.04.29-00:55:09.97 - <debug> New rundir for session 1: /run/user/0/vaccel/yBMakt/session.1
2026.04.29-00:55:09.97 - <debug> Initialized session 1 with plugin mbench
Initialized session with id: 1
2026.04.29-00:55:09.97 - <debug> Start profiling region mbench
2026.04.29-00:55:09.97 - <debug> session:1 Looking for func implementing op exec
2026.04.29-00:55:09.97 - <debug> Start profiling region vaccel_exec_op
2026.04.29-00:55:09.97 - <debug> Returning func for op exec from plugin mbench
2026.04.29-00:55:09.97 - <debug> Calling mbench for session 1
2026.04.29-00:55:09.97 - <debug> Start profiling region vaccel_mbench_plugin
2026.04.29-00:55:09.98 - <debug> [mbench] 10 ms elapsed
2026.04.29-00:55:09.98 - <debug> Stop profiling region vaccel_mbench_plugin
2026.04.29-00:55:09.98 - <debug> Stop profiling region vaccel_exec_op
2026.04.29-00:55:09.98 - <debug> Stop profiling region mbench
2026.04.29-00:55:09.98 - <debug> Released session 1
2026.04.29-00:55:09.98 - <info> [prof] mbench: total_time: 10025819 nsec nr_entries: 1
2026.04.29-00:55:09.98 - <info> [prof] vaccel_exec_op: total_time: 10019046 nsec nr_entries: 1
2026.04.29-00:55:09.98 - <debug> Cleaning up vAccel
2026.04.29-00:55:09.98 - <debug> Cleaning up sessions
2026.04.29-00:55:09.98 - <debug> Cleaning up resources
2026.04.29-00:55:09.98 - <debug> Cleaning up plugins
2026.04.29-00:55:09.98 - <info> [prof] vaccel_mbench_plugin: total_time: 10010250 nsec nr_entries: 1
2026.04.29-00:55:09.98 - <debug> Unregistered plugin mbench
```
