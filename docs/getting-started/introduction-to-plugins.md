# Introduction to plugins

Plugins contain the implementations of vAccel operations. While the vAccel
library itself is the only requirement to compile a vAccel application, you need
to use a plugin for the application to actually do something useful.

The use of plugins can become clearer by revisiting the image classification
example from [Running the examples](running-the-examples.md).

As we have already shown, to specify a backend plugin you have to set the
[`VACCEL_PLUGINS`](../configuration.md#vaccel_plugins) environment variable.

Ensure `VACCEL_PLUGINS` is not set in the environment while keeping debug
logging enabled:

```sh
unset VACCEL_PLUGINS
export VACCEL_LOG_LEVEL=4
```

If you run the example, there will be no errors concerning the binaries
themselves (ie. undefined symbols) but the operation will fail at runtime:

```console
$ classify /usr/local/share/vaccel/images/example.jpg 1
2025.04.05-19:25:04.80 - <debug> Initializing vAccel
2025.04.05-19:25:04.80 - <info> vAccel 0.6.1-194-19056528
2025.04.05-19:25:04.80 - <debug> Config:
2025.04.05-19:25:04.80 - <debug>   plugins = (null)
2025.04.05-19:25:04.80 - <debug>   log_level = debug
2025.04.05-19:25:04.80 - <debug>   log_file = (null)
2025.04.05-19:25:04.80 - <debug>   profiling_enabled = false
2025.04.05-19:25:04.80 - <debug>   version_ignore = false
2025.04.05-19:25:04.80 - <debug> Created top-level rundir: /run/user/1002/vaccel/k0R150
2025.04.05-19:25:04.80 - <debug> New rundir for session 1: /run/user/1002/vaccel/k0R150/session.1
2025.04.05-19:25:04.80 - <debug> Initialized session 1
Initialized session with id: 1
2025.04.05-19:25:04.80 - <debug> session:1 Looking for plugin implementing VACCEL_OP_IMAGE_CLASSIFY
2025.04.05-19:25:04.80 - <warn> None of the loaded plugins implement VACCEL_OP_IMAGE_CLASSIFY
Could not run op: 95
2025.04.05-19:25:04.80 - <debug> Released session 1
2025.04.05-19:25:04.80 - <debug> Cleaning up vAccel
2025.04.05-19:25:04.80 - <debug> Cleaning up sessions
2025.04.05-19:25:04.80 - <debug> Cleaning up resources
2025.04.05-19:25:04.80 - <debug> Cleaning up plugins
```

It is clear from the output that no implementation is found for the
`VACCEL_OP_IMAGE_CLASSIFY` operation. By comparing the output with
[classify](running-the-examples.md#classify-noop-debug) from the previous
document, you can see that the reason is that no plugin has been loaded.

You can find out more about the available plugins and their usage in the
[Plugins](../plugins/index.md) section.

## Using a plugin from a non-standard library path

It is recommended that vAccel and the vAccel plugins are installed in the
standard library search paths for ease of use (ie. `/usr/lib`, `/usr/local/lib`
etc.). If this is not possible or desirable there are two ways to use the
plugins:

<!-- markdownlint-disable blanks-around-fences -->

- Assuming vAccel is installed in a standard path, use the full path to specify
  the plugin. For example, if the `NoOp` plugin is installed in `/opt/noop/lib`:
    ```sh
    export VACCEL_PLUGINS=/opt/noop/lib/libvaccel-noop.so
    ```

or,

- Add the vAccel/plugin library paths to the library search paths and specify
  the plugin as usual. For example, if vAccel and the `NoOp` plugin are
  installed in `/opt/vaccel/lib`:
    ```sh
    export LD_LIBRARY_PATH=/opt/vaccel/lib:$LD_LIBRARY_PATH
    export VACCEL_PLUGINS=libvaccel-noop.so
    ```

<!-- markdownlint-restore -->
