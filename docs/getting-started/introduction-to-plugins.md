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
2026.04.29-14:49:05.41 - <debug> Initializing vAccel
2026.04.29-14:49:05.41 - <info> vAccel 0.7.1-93-ebc23b1f
2026.04.29-14:49:05.41 - <debug> Config:
2026.04.29-14:49:05.41 - <debug>   plugins = (null)
2026.04.29-14:49:05.41 - <debug>   log_level = debug
2026.04.29-14:49:05.41 - <debug>   log_file = (null)
2026.04.29-14:49:05.41 - <debug>   profiling_enabled = false
2026.04.29-14:49:05.41 - <debug>   version_ignore = false
2026.04.29-14:49:05.41 - <debug> Created top-level rundir: /run/user/0/vaccel/wrlzzl
2026.04.29-14:49:05.41 - <error> No plugins registered
Could not initialize session
2026.04.29-14:49:05.41 - <debug> Cleaning up vAccel
2026.04.29-14:49:05.41 - <debug> Cleaning up sessions
2026.04.29-14:49:05.41 - <debug> Cleaning up resources
2026.04.29-14:49:05.41 - <debug> Cleaning up plugins
```

It is clear from the output that the session cannot be initialized because no
plugin has been loaded. By comparing the output with
[classify](running-the-examples.md#classify-noop-debug) from the previous
document, you can see that there are no registered plugins.

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
