# Operations API

The Operations API consists of the vAccel acceleration functions. More
specifically, it includes the "definitions" - interface - of the functions
(operations) that can be implemented by the plugins.

## Overview

Each operation is defined in two ways:

1. **An operation type** that is used to identify the operation
2. **An actual function** that maps the function interface to the plugin
   function

For example, you can have a look at the definitions of the simple
[`SGEMM` operation](../api-reference/operations.md#matrix-to-matrix-multiplication)
that handles matrix to matrix multiplication.

The operation type (`VACCEL_OP_BLAS_SGEMM`) is defined in the public
[op.h](https://github.com/nubificus/vaccel/blob/v[[versions.vaccel]]/src/include/vaccel/op.h):

```c title="src/include/vaccel/op.h"
...
/* Define vaccel_op_type_t, vaccel_op_type_to_str() and
 * vaccel_op_type_to_base_str() */
#define _ENUM_PREFIX VACCEL_OP
#define VACCEL_OP_TYPE_ENUM_LIST(VACCEL_ENUM_ITEM)            \
...
        VACCEL_ENUM_ITEM(BLAS_SGEMM, _ENUM_PREFIX)            \
...
```

The `vaccel_sgemm` function corresponding to the operation type is defined in
[blas.c](https://github.com/nubificus/vaccel/blob/v[[versions.vaccel]]/src/ops/blas.c)
and exported internally with
[blas.h](https://github.com/nubificus/vaccel/blob/v[[versions.vaccel]]/src/ops/blas.h):

```c title="src/ops/blas.c"
int vaccel_sgemm(struct vaccel_session *sess, long long int m, long long int n,
                 long long int k, float alpha, float *a, long long int lda,
                 float *b, long long int ldb, float beta, float *c,
                 long long int ldc)
{
        int ret;
...
        sgemm_fn_t plugin_sgemm =
                plugin_get_op_func(VACCEL_OP_BLAS_SGEMM, sess->hint);
        if (!plugin_sgemm) {
                ret = VACCEL_ENOTSUP;
                goto out;
        }

        ret = plugin_sgemm(sess, m, n, k, alpha, a, lda, b, ldb, beta, c, ldc);
...
        return ret;
}
```

The plugin function for `VACCEL_OP_BLAS_SGEMM` is loaded with
`plugin_get_op_func()`. That is how a user calling `vaccel_sgemm` gets the
plugin implementation of the function.

To actually build an operation, you also also have to add these two files to the
[build system](https://github.com/nubificus/vaccel/blob/v[[versions.vaccel]]/src/ops/meson.build):

```meson title="src/ops/meson.build"
vaccel_headers += files([
  'blas.h',
...
])

vaccel_sources += files([
  'blas.c',
...
])
```

## Special operations

To facilitate development of transport plugins and integration with existing
projects, vAccel provides some special-purpose operations.

### The Generic operation (`GenOp`)

While defining a new operation is relatively simple, any new operation needs to
be implemented for the transport plugins. To simplify addition of new operations
with minimal modifications to the transport plugins, vAccel defines the
[Generic operation (`GenOp`)](../api-reference/operations.md#generic-operation).

`GenOp` provides a generic interface to pass arguments to an operation. Any
operation that has a `GenOp` variant can be supported by a transport plugin with
minimal modifications to the plugin itself, provided `GenOp` is already
implemented in the transport layer.

To add `GenOp` support for an operation you need to define an `unpack` function
that will convert the generic arguments to the actual function arguments.

Revisiting
[blas.c](https://github.com/nubificus/vaccel/blob/v[[versions.vaccel]]/src/ops/blas.c)
from above, the relevant `vaccel_sgemm_unpack` is:

```c title="src/ops/blas.c"
int vaccel_sgemm_unpack(struct vaccel_session *sess, struct vaccel_arg *read,
                        int nr_read, struct vaccel_arg *write, int nr_write)
{
...
        long long int m = *(long long int *)read[0].buf;
        long long int n = *(long long int *)read[1].buf;
        long long int k = *(long long int *)read[2].buf;
        float alpha = *(float *)read[3].buf;
        float *a = (float *)read[4].buf;
        long long int lda = *(long long int *)read[5].buf;
        float *b = (float *)read[6].buf;
        long long int ldb = *(long long int *)read[7].buf;
        float beta = *(float *)read[8].buf;
        long long int ldc = *(long long int *)read[9].buf;

        float *c = (float *)write[0].buf;

        return vaccel_sgemm(sess, m, n, k, alpha, a, lda, b, ldb, beta, c, ldc);
}
```

Each `vaccel_sgemm` argument is expected as `vaccel_arg` in a specific order.

To define the function as a genop unpacking function you also need to add it to
the `callbacks` array in the same place as `VACCEL_OP_BLAS_SGEMM` is defined in
the respective enum:

```c title="src/ops/genop.c"
...
unpack_func_t callbacks[VACCEL_OP_MAX] = {
...
        vaccel_sgemm_unpack, /* 1 */
...
};
...
```

An example of the relevant "packing" of the arguments can be found in the
[`sgemm_generic`](https://github.com/nubificus/vaccel/blob/v[[versions.vaccel]]/examples/sgemm_generic.c)
example:

```c title="examples/sgemm_generic.c"
...
int main(int argc, char *argv[])
{
...
        vaccel_op_type_t op_type = VACCEL_OP_BLAS_SGEMM;
        struct vaccel_arg read[] = {
                { .size = sizeof(vaccel_op_type_t), .buf = &op_type },
                { .size = sizeof(m), .buf = &m },
                { .size = sizeof(n), .buf = &n },
                { .size = sizeof(k), .buf = &k },
                { .size = sizeof(alpha), .buf = (void *)&alpha },
                { .size = sizeof(a), .buf = a },
                { .size = sizeof(k), .buf = &k },
                { .size = sizeof(b), .buf = b },
                { .size = sizeof(n), .buf = &n },
                { .size = sizeof(beta), .buf = (void *)&beta },
                { .size = sizeof(n), .buf = &n },
        };
        struct vaccel_arg write[] = {
                { .size = sizeof(c), .buf = c },
        };
...
                ret = vaccel_genop(&sess, read, sizeof(read) / sizeof(read[0]),
                                   write, sizeof(write) / sizeof(write[0]));
...
}
```

### The Exec operation

Adding operations requires modification and rebuilding of vAccel itself. To use
an unmodified vAccel with a new operation, you can take advantage of the
[`Exec` operation](../api-reference/operations.md#exec).

The `Exec` operation - combined with the
[`Exec` plugin](../../plugins/available-plugins/bundled-plugins/exec-plugin.md) -
enables execution of functions from arbitrary libraries without requiring the
addition of new operations. The operation's usage is similar to `GenOp`,
described above.

While the `Exec` workflow can be support new operations without modifying
vAccel, it must be used with caution in shared systems, since it allows the
execution of arbitrary functions.
