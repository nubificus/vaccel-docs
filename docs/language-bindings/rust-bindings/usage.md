# Usage

The Rust bindings are implemented in the `vaccel` Rust crate and feature a large
subset of the vAccel operations.

## Requirements

- To use the `vaccel` Rust crate you need a working vAccel installation. You can
  find more information on how to install vAccel in the
  [Installation](../../getting-started/installation.md) page.

<!-- markdownlint-disable blanks-around-fences -->

- This package requires Rust 1.70 or newer. Verify your Rust version with:
  ```sh
  rustc version
  ```
  and update Rust as needed using the
  [official instructions](https://www.rust-lang.org/tools/install).

<!-- markdownlint-restore -->

## Using the `vaccel` crate

You can use the package in your Rust code like any other crate with:

```toml
[dependencies]
vaccel = { git = "https://github.com/nubificus/vaccel-rust" }
```

<!-- markdownlint-disable code-block-style -->

!!! warning

    To include a crate from a rust workspace repo, you need to specify
    the name of crate as the dependency.

## Running the examples

You can find examples in the
[examples](https://github.com/nubificus/vaccel-rust/tree/main/vaccel-bindings/examples)
directory of the repository. The provided examples are similar to the
[C examples](../../getting-started/running-the-examples.md) and you must
configure vAccel in order to use them.

To run a simple session init/release, like the C `noop` example, clone the
bindings repo:

```sh
git clone https://github.com/nubificus/vaccel-rust
cd vaccel-rust/vaccel-bindings
```

Build the examples:

```sh
$ cargo build --examples
warning: virtual workspace defaulting to `resolver = "1"` despite one or more workspace members being on edition 2021 which implies `resolver = "2"`
note: to keep the current resolver, specify `workspace.resolver = "1"` in the workspace root's manifest
note: to use the edition 2021 resolver, specify `workspace.resolver = "2"` in the workspace root's manifest
note: for more details see https://doc.rust-lang.org/cargo/reference/resolver.html#resolver-versions
    Updating crates.io index
    Updating git repository `https://github.com/nubificus/ttrpc-rust.git`
   Compiling proc-macro2 v1.0.95
   Compiling unicode-ident v1.0.18
[snipped]
   Compiling vaccel v0.0.0 (/home/ananos/develop/fresh/playground/vaccel-rust/vaccel-bindings)
   Compiling futures-executor v0.3.31
   Compiling futures v0.3.31
   Compiling protobuf-parse v3.7.2
   Compiling tokio-vsock v0.4.0
   Compiling protobuf-codegen v3.7.2
   Compiling ttrpc-codegen v0.5.0 (https://github.com/nubificus/ttrpc-rust.git?branch=vaccel-dev#30b79e78)
   Compiling ttrpc v0.8.3 (https://github.com/nubificus/ttrpc-rust.git?branch=vaccel-dev#30b79e78)
   Compiling vaccel-rpc-proto v0.0.0 (/home/ananos/develop/fresh/playground/vaccel-rust/vaccel-rpc-proto)
    Finished dev [unoptimized + debuginfo] target(s) in 24.59s
```

If all went well, the examples' binaries should be available in
`../target/debug/examples`.

!!! warning The directory is one level up, in the `vaccel-rust` workspace.

Set the config environment variables:

```sh
export VACCEL_PLUGINS=libvaccel-noop.so
```

and, assuming vAccel is installed at `/usr/local`, run with:

```console
$ ../target/debug/examples/session
[2025-04-16T14:44:07Z INFO  session] Starting vAccel session handling example
[2025-04-16T14:44:07Z INFO  session] Creating new vAccel session
[2025-04-16T14:44:07Z INFO  session] Initialized session 1
[2025-04-16T14:44:07Z INFO  session] Releasing session 1
[2025-04-16T14:44:07Z INFO  session] Done
```

By setting log level to debug:

```sh
export VACCEL_LOG_LEVEL=4
```

you can see the verbose vAccel output:

```console
$ ../target/debug/examples/session
2025.04.16-14:43:15.99 - <debug> Initializing vAccel
2025.04.16-14:43:15.99 - <info> vAccel 0.6.1-194-19056528
2025.04.16-14:43:15.99 - <debug> Config:
2025.04.16-14:43:15.99 - <debug>   plugins = libvaccel-noop.so
2025.04.16-14:43:15.99 - <debug>   log_level = debug
2025.04.16-14:43:15.99 - <debug>   log_file = (null)
2025.04.16-14:43:15.99 - <debug>   profiling_enabled = true
2025.04.16-14:43:15.99 - <debug>   version_ignore = true
2025.04.16-14:43:15.99 - <debug> Created top-level rundir: /run/user/1000/vaccel/oOGHc5
2025.04.16-14:43:15.99 - <info> Registered plugin noop 0.6.1-194-19056528
2025.04.16-14:43:15.99 - <debug> Registered op noop from plugin noop
2025.04.16-14:43:15.99 - <debug> Registered op blas_sgemm from plugin noop
2025.04.16-14:43:15.99 - <debug> Registered op image_classify from plugin noop
2025.04.16-14:43:15.99 - <debug> Registered op image_detect from plugin noop
2025.04.16-14:43:15.99 - <debug> Registered op image_segment from plugin noop
2025.04.16-14:43:15.99 - <debug> Registered op image_pose from plugin noop
2025.04.16-14:43:15.99 - <debug> Registered op image_depth from plugin noop
2025.04.16-14:43:15.99 - <debug> Registered op exec from plugin noop
2025.04.16-14:43:15.99 - <debug> Registered op tf_session_load from plugin noop
2025.04.16-14:43:15.99 - <debug> Registered op tf_session_run from plugin noop
2025.04.16-14:43:15.99 - <debug> Registered op tf_session_delete from plugin noop
2025.04.16-14:43:15.99 - <debug> Registered op minmax from plugin noop
2025.04.16-14:43:15.99 - <debug> Registered op fpga_arraycopy from plugin noop
2025.04.16-14:43:15.99 - <debug> Registered op fpga_vectoradd from plugin noop
2025.04.16-14:43:15.99 - <debug> Registered op fpga_parallel from plugin noop
2025.04.16-14:43:15.99 - <debug> Registered op fpga_mmult from plugin noop
2025.04.16-14:43:15.99 - <debug> Registered op exec_with_resource from plugin noop
2025.04.16-14:43:15.99 - <debug> Registered op torch_jitload_forward from plugin noop
2025.04.16-14:43:15.99 - <debug> Registered op torch_sgemm from plugin noop
2025.04.16-14:43:15.99 - <debug> Registered op opencv from plugin noop
2025.04.16-14:43:15.99 - <debug> Registered op tflite_session_load from plugin noop
2025.04.16-14:43:15.99 - <debug> Registered op tflite_session_run from plugin noop
2025.04.16-14:43:15.99 - <debug> Registered op tflite_session_delete from plugin noop
2025.04.16-14:43:15.99 - <debug> Loaded plugin noop from libvaccel-noop.so
[2025-04-16T14:43:15Z INFO  session] Starting vAccel session handling example
[2025-04-16T14:43:15Z INFO  session] Creating new vAccel session
2025.04.16-14:43:15.99 - <debug> New rundir for session 1: /run/user/1000/vaccel/oOGHc5/session.1
2025.04.16-14:43:15.99 - <debug> Initialized session 1
[2025-04-16T14:43:15Z INFO  session] Initialized session 1
[2025-04-16T14:43:15Z INFO  session] Releasing session 1
2025.04.16-14:43:15.99 - <debug> Released session 1
[2025-04-16T14:43:15Z INFO  session] Done
2025.04.16-14:43:15.99 - <debug> Cleaning up vAccel
2025.04.16-14:43:15.99 - <debug> Cleaning up sessions
2025.04.16-14:43:15.99 - <debug> Cleaning up resources
2025.04.16-14:43:15.99 - <debug> Cleaning up plugins
2025.04.16-14:43:15.99 - <debug> Unregistered plugin noop
```
