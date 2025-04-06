# About plugins

Plugins are an essential part of vAccel. They contain the implementations of the
operations defined in the [API](../api/index.md). By keeping the implementation
logic separate from the operation definition, vAccel enables the use of
different acceleration frameworks without requiring the modification or
recompilation of the application binaries. This means, that a compiled vAccel
application can use any acceleration implementation available as a plugin by
simply specifying the plugin at runtime.

A vAccel plugin has the form of a shared object (library) that can be loaded
with `dlopen()`. The object can be compiled from any language as long as the
contained symbols/functions are callable from `C`.

You can better understand the use of the plugin system by trying to run an
[example](../getting-started/running-the-examples.md) with different plugins.

The image classification example is based on the relevant
[User API operation](../api/api-reference/operations.md#image-classification).
The operation is supported by the `NoOp` plugin, that we used in
[Running the examples](../getting-started/running-the-examples.md). It is also
supported by the [Torch](available-plugins/acceleration-plugins/torch-plugin.md)
and the [TVM](available-plugins/acceleration-plugins/tvm-plugin.md) plugins.
This means that the same `classify` binary can be used to run with the
[NoOp](../getting-started/running-the-examples.md#classify-noop-debug), the
[Torch](available-plugins/acceleration-plugins/torch-plugin.md#running-an-example)
and the
[TVM](available-plugins/acceleration-plugins/tvm-plugin.md#running-an-example)
vAccel image classification implementations simply by specifying the relevant
plugin (provided all dependencies are installed).
