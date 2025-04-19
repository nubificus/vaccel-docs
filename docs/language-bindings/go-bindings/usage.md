# Usage

The Go bindings are implemented in the `vaccel` Go package and are currently a
WiP, supporting a subset of the vAccel operations.

## Requirements

- To use the `vaccel` Go package you need a valid vAccel installation. You can
  find more information on how to install vAccel in the
  [Installation](../../getting-started/installation.md) page.

<!-- markdownlint-disable blanks-around-fences -->

- This package requires Go 1.20 or newer. Verify your Go version with:
  ```sh
  go version
  ```
  and update Go as needed using the
  [official instructions](https://go.dev/doc/install).

<!-- markdownlint-restore -->

## Using the `vaccel` package

You can use the package in your Go code like any other Go package with:

```go
import "github.com/nubificus/go-vaccel/vaccel"
```

## Running the examples

You can find examples in the
[examples](https://github.com/nubificus/go-vaccel/tree/main/examples) directory
of the repository. The provided examples are similar to the
[C examples](../../getting-started/running-the-examples.md) and you must
configure vAccel in order to use them.

To run an image classification, like the C `classify`, set:

```sh
export VACCEL_PLUGINS=libvaccel-noop.so
```

and, assuming vAccel is installed at `/usr/local`, run with:

```console
$ go run github.com/nubificus/go-vaccel/examples/classify \
      /usr/local/share/vaccel/images/example.jpg
Output(1):  This is a dummy classification tag!
Output(2):  This is a dummy classification tag!
```

By setting log level to debug:

```sh
export VACCEL_LOG_LEVEL=4
```

you can see the verbose vAccel output, very similar to the
[C `classify`](../../getting-started/running-the-examples.md#classify-noop-debug)
output:

```console
$ go run github.com/nubificus/go-vaccel/examples/classify \
      /usr/local/share/vaccel/images/example.jpg
2025.04.15-16:51:03.74 - <debug> Initializing vAccel
2025.04.15-16:51:03.74 - <info> vAccel 0.6.1-194-19056528
2025.04.15-16:51:03.74 - <debug> Config:
2025.04.15-16:51:03.74 - <debug>   plugins = libvaccel-noop.so
2025.04.15-16:51:03.74 - <debug>   log_level = debug
2025.04.15-16:51:03.74 - <debug>   log_file = (null)
2025.04.15-16:51:03.74 - <debug>   profiling_enabled = false
2025.04.15-16:51:03.74 - <debug>   version_ignore = false
2025.04.15-16:51:03.74 - <debug> Created top-level rundir: /run/user/1002/vaccel/37513G
2025.04.15-16:51:03.75 - <info> Registered plugin noop 0.6.1-194-19056528
2025.04.15-16:51:03.75 - <debug> Registered op noop from plugin noop
2025.04.15-16:51:03.75 - <debug> Registered op blas_sgemm from plugin noop
2025.04.15-16:51:03.75 - <debug> Registered op image_classify from plugin noop
2025.04.15-16:51:03.75 - <debug> Registered op image_detect from plugin noop
2025.04.15-16:51:03.75 - <debug> Registered op image_segment from plugin noop
2025.04.15-16:51:03.75 - <debug> Registered op image_pose from plugin noop
2025.04.15-16:51:03.75 - <debug> Registered op image_depth from plugin noop
2025.04.15-16:51:03.75 - <debug> Registered op exec from plugin noop
2025.04.15-16:51:03.75 - <debug> Registered op tf_session_load from plugin noop
2025.04.15-16:51:03.75 - <debug> Registered op tf_session_run from plugin noop
2025.04.15-16:51:03.75 - <debug> Registered op tf_session_delete from plugin noop
2025.04.15-16:51:03.75 - <debug> Registered op minmax from plugin noop
2025.04.15-16:51:03.75 - <debug> Registered op fpga_arraycopy from plugin noop
2025.04.15-16:51:03.75 - <debug> Registered op fpga_vectoradd from plugin noop
2025.04.15-16:51:03.75 - <debug> Registered op fpga_parallel from plugin noop
2025.04.15-16:51:03.75 - <debug> Registered op fpga_mmult from plugin noop
2025.04.15-16:51:03.75 - <debug> Registered op exec_with_resource from plugin noop
2025.04.15-16:51:03.75 - <debug> Registered op torch_jitload_forward from plugin noop
2025.04.15-16:51:03.75 - <debug> Registered op torch_sgemm from plugin noop
2025.04.15-16:51:03.75 - <debug> Registered op opencv from plugin noop
2025.04.15-16:51:03.75 - <debug> Registered op tflite_session_load from plugin noop
2025.04.15-16:51:03.75 - <debug> Registered op tflite_session_run from plugin noop
2025.04.15-16:51:03.75 - <debug> Registered op tflite_session_delete from plugin noop
2025.04.15-16:51:03.75 - <debug> Loaded plugin noop from libvaccel-noop.so
2025.04.15-16:51:03.75 - <debug> New rundir for session 1: /run/user/1002/vaccel/37513G/session.1
2025.04.15-16:51:03.75 - <debug> Initialized session 1
2025.04.15-16:51:03.75 - <debug> session:1 Looking for plugin implementing VACCEL_OP_IMAGE_CLASSIFY
2025.04.15-16:51:03.75 - <debug> Returning func from hint plugin noop
2025.04.15-16:51:03.75 - <debug> Found implementation in noop plugin
2025.04.15-16:51:03.75 - <debug> [noop] Calling Image classification for session 1
2025.04.15-16:51:03.75 - <debug> [noop] Dumping arguments for Image classification:
2025.04.15-16:51:03.75 - <debug> [noop] model: (null)
2025.04.15-16:51:03.75 - <debug> [noop] len_img: 79281
2025.04.15-16:51:03.75 - <debug> [noop] len_out_text: 256
2025.04.15-16:51:03.75 - <debug> [noop] len_out_imgname: 256
2025.04.15-16:51:03.75 - <debug> [noop] will return a dummy result
2025.04.15-16:51:03.75 - <debug> [noop] will return a dummy result
Output(1):  This is a dummy classification tag!
2025.04.15-16:51:03.75 - <debug> session:1 Looking for plugin implementing VACCEL_OP_IMAGE_CLASSIFY
2025.04.15-16:51:03.75 - <debug> Returning func from hint plugin noop
2025.04.15-16:51:03.75 - <debug> Found implementation in noop plugin
2025.04.15-16:51:03.75 - <debug> [noop] Calling Image classification for session 1
2025.04.15-16:51:03.75 - <debug> [noop] Dumping arguments for Image classification:
2025.04.15-16:51:03.75 - <debug> [noop] model: (null)
2025.04.15-16:51:03.75 - <debug> [noop] len_img: 79281
2025.04.15-16:51:03.75 - <debug> [noop] len_out_text: 256
2025.04.15-16:51:03.75 - <debug> [noop] len_out_imgname: 256
2025.04.15-16:51:03.75 - <debug> [noop] will return a dummy result
2025.04.15-16:51:03.75 - <debug> [noop] will return a dummy result
Output(2):  This is a dummy classification tag!
2025.04.15-16:51:03.75 - <debug> Released session 1
```

## Installing the examples

If you want to install an example for local use, you can use `go install`. For
example:

```sh
go install github.com/nubificus/go-vaccel/examples/classify
```

will install the `classify` example in your local Go binary path.

## Building the examples from source

You can also clone the repository locally to build the examples:

```sh
git clone https://github.com/nubificus/go-vaccel.git
cd go-vaccel
make
```

If all went well, the examples' binaries should be available in `./bin`.
