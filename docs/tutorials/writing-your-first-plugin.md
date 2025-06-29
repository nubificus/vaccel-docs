# Writing your first plugin

vAccel plugins provide the glue code between vAccel User API operations and
their hardware implementations. A vAccel plugin is a shared object, built in any
programming language that can generate it.

The required operations that need to be implemented for a shared object to be
linked as a vAccel plugin, are the following:

<!-- markdownlint-disable blanks-around-fences -->
<!-- prettier-ignore-start -->

- An `init()` function, called upon plugin initialization
  ```c
  static int init(void) {
  ...
  }
  ```

- A `fini()` function, called before unloading the plugin
  ```c
  static int fini(void) {
  ...
  }
  ```

<!-- prettier-ignore-end -->
<!-- markdownlint-restore -->

- A definition of the `VACCEL_PLUGIN` with:

    - `.name` : The name of the plugin
    - `.version` : The version of the plugin
    - `.vaccel_version` : The vAccel library version that the plugin was built
      against
    - `.init` : The function to call upon plugin initialization (eg. `init()`)
    - `.fini` : The function to call before unloading the plugin (eg. on program
      exit, `fini()`)

```c
VACCEL_PLUGIN(
    .name = "vAccel template plugin",
    .version = "0.9",
    .vaccel_version = VACCEL_VERSION,
    .init = init,
    .fini = fini
)
```

At initialization, the plugin needs to register the vAccel operations that it
implements. To do that, we use an array of `struct vaccel_op`s, that map each
function implementation to the respective API operation. An operation array
could look like the following:

```c
static struct vaccel_op ops[] = {
    VACCEL_OP_INIT(ops[0], VACCEL_OP_NOOP, my_noop_function),
    [...]
};
```

where `VACCEL_OP_NOOP` is the operation `type` and `my_noop_function` is the
`func`tion implementation:

```c
struct vaccel_op {
    /* operation type */
    vaccel_op_type_t type;

    /* function implementing the operation */
    void *func;

    [...]
};
```

## Implement a simple `NOOP` plugin

To better understand how to implement an actual plugin we provide a
[vaccel-plugin-template](https://github.com/nubificus/vaccel-plugin-template).
This repo is a good start for developing a vAccel plugin in C.

Let's look into `src/vaccel.c` from the template repo:

```c
#include <inttypes.h>
#include <stdio.h>
#include <vaccel.h> /* header with vAccel API */

/* A function that will be mapped to a vAccel User API operation using
 * register_plugin_functions() */
static int my_noop_function(struct vaccel_session *sess)
{
    fprintf(stderr, "[my noop function] session: %" PRId64 "\n", sess->id);
    return VACCEL_OK;
}

/* An array of the operations to be mapped */
struct vaccel_op ops[] = {
    VACCEL_OP_INIT(ops[0], VACCEL_NO_OP, my_noop_function),
};

/* The init() function, called upon plugin initialization */
static int init(void)
{
    /* This is where the static function above `my_noop_function()`
     * gets mapped to the relevant vAccel User API operation. */
    return vaccel_plugin_register_ops(ops, sizeof(ops) / sizeof(ops[0]));
}

/* The fini() function, called before unloading the plugin */
static int fini(void)
{
    return VACCEL_OK;
}

VACCEL_PLUGIN(.name = "template", .version = "0.9",
              .vaccel_version = VACCEL_VERSION, .init = init, .fini = fini)
```

The plugin registers `my_noop_function()` to serve as the implementation of the
`VACCEL_OP_NOOP` API operation.

## Install requirements

Before building a vAccel plugin, you need to install the main vAccel library.
Instructions on how to build vAccel can be found
[here](../getting-started/installation.md).

You also need some packages to build the plugin itself:

```bash
sudo apt-get install build-essential ninja-build pkg-config python3-pip
sudo pip install meson
```

## Build the plugin

Now you can build the vAccel plugin template that implements the `NOOP` user API
operation with your own custom function.

First clone the repo:

```bash
git clone https://github.com/nubificus/vaccel-plugin-template
cd vaccel-plugin-template
```

Use `meson` to prepare the `build` directory:

```bash
meson setup build
```

an build the plugin with:

```bash
meson compile -C build
```

This should output a shared object (`libvaccel-template.so`) in `./build/src/`.

<!-- markdownlint-disable code-block-style -->

!!! info

    To use this plugin with vAccel, you need to select it using the environment
    variable `VACCEL_PLUGINS` when running our vAccel application (ie.
    `VACCEL_PLUGINS=/path/to/libvaccel-template.so`).

    See [Running the examples](../getting-started/running-the-examples.md) for
    more information.

<!-- markdownlint-restore -->
