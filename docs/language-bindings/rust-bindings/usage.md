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

!!! info

    To include a crate from a rust workspace repo, you need to specify
    the name of the crate as the dependency.

<!-- markdownlint-restore -->

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
   Compiling proc-macro2 v1.0.106
   Compiling unicode-ident v1.0.24
[snipped]
   Compiling protobuf v3.7.2
   Compiling protobuf-support v3.7.2
   Compiling vaccel v0.0.0 (/tmp/vaccel-rust/vaccel-bindings)
   Compiling dashmap v6.1.0
   Compiling env_logger v0.11.10
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 14.92s
```

If all went well, the examples' binaries should be available in
`../target/debug/examples`.

<!-- markdownlint-disable code-block-style -->

!!! note

    The directory is one level up, in the `vaccel-rust` workspace.

<!-- markdownlint-restore -->

Set the config environment variables:

```sh
export VACCEL_PLUGINS=libvaccel-noop.so
```

and, assuming vAccel is installed at `/usr/local`, run with:

```console
$ ../target/debug/examples/session
[2026-04-29T14:51:35Z INFO  session] Starting vAccel session handling example
[2026-04-29T14:51:35Z INFO  session] Creating new vAccel session
[2026-04-29T14:51:35Z INFO  session] Initialized session 1
```

By setting log level to debug:

```sh
export VACCEL_LOG_LEVEL=4
```

you can see the verbose vAccel output:

```console
$ ../target/debug/examples/session
[2026-04-29T14:51:35Z INFO  session] Starting vAccel session handling example
[2026-04-29T14:51:35Z INFO  session] Creating new vAccel session
2026.04.29-14:51:35.50 - <debug> Initializing vAccel
2026.04.29-14:51:35.50 - <info> vAccel 0.7.1-93-ebc23b1f
2026.04.29-14:51:35.50 - <debug> Config:
2026.04.29-14:51:35.50 - <debug>   plugins = libvaccel-noop.so
2026.04.29-14:51:35.50 - <debug>   log_level = debug
2026.04.29-14:51:35.50 - <debug>   log_file = (null)
2026.04.29-14:51:35.50 - <debug>   profiling_enabled = false
2026.04.29-14:51:35.50 - <debug>   version_ignore = false
2026.04.29-14:51:35.50 - <debug> Created top-level rundir: /run/user/0/vaccel/qAtMaP
2026.04.29-14:51:35.50 - <info> Registered plugin noop 0.7.1-93-ebc23b1f
2026.04.29-14:51:35.50 - <debug> Registered op noop from plugin noop
2026.04.29-14:51:35.50 - <debug> Registered op exec from plugin noop
2026.04.29-14:51:35.50 - <debug> Registered op exec_with_resource from plugin noop
2026.04.29-14:51:35.50 - <debug> Registered op image_classify from plugin noop
2026.04.29-14:51:35.50 - <debug> Registered op image_detect from plugin noop
2026.04.29-14:51:35.50 - <debug> Registered op image_segment from plugin noop
2026.04.29-14:51:35.50 - <debug> Registered op image_pose from plugin noop
2026.04.29-14:51:35.50 - <debug> Registered op image_depth from plugin noop
2026.04.29-14:51:35.50 - <debug> Registered op tf_model_load from plugin noop
2026.04.29-14:51:35.50 - <debug> Registered op tf_model_unload from plugin noop
2026.04.29-14:51:35.50 - <debug> Registered op tf_model_run from plugin noop
2026.04.29-14:51:35.50 - <debug> Registered op tflite_model_load from plugin noop
2026.04.29-14:51:35.50 - <debug> Registered op tflite_model_unload from plugin noop
2026.04.29-14:51:35.50 - <debug> Registered op tflite_model_run from plugin noop
2026.04.29-14:51:35.50 - <debug> Registered op torch_model_load from plugin noop
2026.04.29-14:51:35.50 - <debug> Registered op torch_model_run from plugin noop
2026.04.29-14:51:35.50 - <debug> Registered op torch_sgemm from plugin noop
2026.04.29-14:51:35.50 - <debug> Registered op blas_sgemm from plugin noop
2026.04.29-14:51:35.50 - <debug> Registered op fpga_arraycopy from plugin noop
2026.04.29-14:51:35.50 - <debug> Registered op fpga_vectoradd from plugin noop
2026.04.29-14:51:35.50 - <debug> Registered op fpga_parallel from plugin noop
2026.04.29-14:51:35.50 - <debug> Registered op fpga_mmult from plugin noop
2026.04.29-14:51:35.50 - <debug> Registered op minmax from plugin noop
2026.04.29-14:51:35.50 - <debug> Registered op opencv from plugin noop
2026.04.29-14:51:35.50 - <debug> Loaded plugin noop from libvaccel-noop.so
2026.04.29-14:51:35.50 - <debug> New rundir for session 1: /run/user/0/vaccel/qAtMaP/session.1
2026.04.29-14:51:35.50 - <debug> Initialized session 1 with plugin noop
[2026-04-29T14:51:35Z INFO  session] Initialized session 1
2026.04.29-14:51:35.50 - <debug> Released session 1
2026.04.29-14:51:35.50 - <debug> Cleaning up vAccel
2026.04.29-14:51:35.50 - <debug> Cleaning up sessions
2026.04.29-14:51:35.50 - <debug> Cleaning up resources
2026.04.29-14:51:35.50 - <debug> Cleaning up plugins
2026.04.29-14:51:35.50 - <debug> Unregistered plugin noop
```
