# Writing a simple vAccel Rust application

For a simple example of using the `vaccel` Rust crate, you can replicate in Rust
an image classification application similar to the image classification example
from [Running the examples](/getting-started/running-the-examples).

Initialize a new `rust-vaccel-classify` project and module:

```sh
mkdir rust-vaccel-classify
cd rust-vaccel-classify
cargo init
```

You should get the following file/directory structure:

```
rust-vaccel-classify
├── Cargo.toml
└── src
    └── main.rs

2 directories, 2 files
```

Edit the `Cargo.toml` file with the following content:

```toml title="Cargo.toml"
[package]
name = "rust-vaccel-classify"
version = "0.1.0"
edition = "2021"
license = "Apache-2.0"

[features]
default = ["profiling"]
profiling = []

[dependencies]
vaccel = { git = "https://github.com/nubificus/vaccel-rust" }
protobuf = "3.1"
env_logger = "0.11"
log = "0.4"
libc = "0.2"
thiserror = "1.0"

[build-dependencies]
libc = "0.2"
bindgen = "0.69"
pkg-config = "0.3"

[dev-dependencies]
env_logger = "0.11"
log = "0.4"
```

Edit the necessary logic into `src/main.rs`:

```rust title="src/main.rs"
// SPDX-License-Identifier: Apache-2.0
use env_logger::Env;
use log::{error, info};
use std::env;
use std::fs::File;
use std::io::Read;
use std::path::Path;
use vaccel::*;

fn main() {
    env_logger::Builder::from_env(Env::default().default_filter_or("debug")).init();
    info!("Starting vAccel classification example");

    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        error!("Usage: {} <image_path>", args[0]);
        return;
    }

    let image_path = &args[1];
    if !Path::new(image_path).exists() {
        error!("Image file not found: {}", image_path);
        return;
    }

    info!("Creating new vAccel session");
    let mut sess = match Session::new(0) {
        Ok(sess) => sess,
        Err(e) => {
            error!("Error creating session: {}", e);
            return;
        }
    };
    info!("Initialized session {}", sess.id());

    info!("Reading image file: {}", image_path);
    let mut file = match File::open(image_path) {
        Ok(file) => file,
        Err(e) => {
            error!("Failed to open image file: {}", e);
            return;
        }
    };

    let mut image_data = Vec::new();
    if let Err(e) = file.read_to_end(&mut image_data) {
        error!("Failed to read image data: {}", e);
        return;
    }
    info!("Read image data: {} bytes", image_data.len());

    info!("Performing image classification");
    let ret = sess.image_classification(&mut image_data);

    match ret {
        Ok((first_vec, second_vec)) => {
            let first_str = String::from_utf8_lossy(&first_vec);
            let second_str = String::from_utf8_lossy(&second_vec);

            info!("Classification completed successfully");
            println!("Classification tags: {}", first_str);
            println!("Annotated image: {}", second_str);
        }
        Err(e) => {
            error!("Classification failed: {:?}", e);
        }
    }

    info!("Releasing session {}", sess.id());
    match sess.release() {
        Ok(()) => info!("Session released successfully"),
        Err(e) => error!("Error releasing session: {}", e),
    }
}
```

Build it:

```console
$ cargo build
    Updating crates.io index
    Updating git repository `https://github.com/nubificus/vaccel-rust`
    Updating git repository `https://github.com/nubificus/ttrpc-rust.git`
   Compiling proc-macro2 v1.0.95
   Compiling unicode-ident v1.0.18
   Compiling autocfg v1.4.0
   Compiling cfg-if v1.0.0
[snipped]
   Compiling tokio-vsock v0.4.0
   Compiling vaccel v0.0.0 (https://github.com/nubificus/vaccel-rust#0af1c664)
   Compiling protobuf-parse v3.7.2
   Compiling protobuf-codegen v3.7.2
   Compiling ttrpc-codegen v0.5.0 (https://github.com/nubificus/ttrpc-rust.git?branch=vaccel-dev#30b79e78)
   Compiling ttrpc v0.8.3 (https://github.com/nubificus/ttrpc-rust.git?branch=vaccel-dev#30b79e78)
   Compiling vaccel-rpc-proto v0.0.0 (https://github.com/nubificus/vaccel-rust#0af1c664)
   Compiling rust-vaccel-classify v0.1.0 (/home/ananos/develop/fresh/playground/rust-vaccel-classify)
    Finished dev [unoptimized + debuginfo] target(s) in 25.90s
```

And you are ready to run your application.

Configure vAccel:

```sh
export VACCEL_PLUGINS=libvaccel-noop.so
export VACCEL_LOG_LEVEL=4
```

and run with:
```console
$ cargo run /usr/share/vaccel/images/example.jpg
    Finished dev [unoptimized + debuginfo] target(s) in 0.07s
     Running `target/debug/rust-vaccel-classify /usr/share/vaccel/images/example.jpg`
2025.04.16-14:39:45.13 - <debug> Initializing vAccel
2025.04.16-14:39:45.13 - <info> vAccel 0.6.1-194-19056528
2025.04.16-14:39:45.13 - <debug> Config:
2025.04.16-14:39:45.13 - <debug>   plugins = libvaccel-noop.so
2025.04.16-14:39:45.13 - <debug>   log_level = debug
2025.04.16-14:39:45.13 - <debug>   log_file = (null)
2025.04.16-14:39:45.13 - <debug>   profiling_enabled = true
2025.04.16-14:39:45.13 - <debug>   version_ignore = true
2025.04.16-14:39:45.13 - <debug> Created top-level rundir: /run/user/1000/vaccel/jesuwX
2025.04.16-14:39:45.13 - <info> Registered plugin noop 0.6.1-194-19056528
2025.04.16-14:39:45.13 - <debug> Registered op noop from plugin noop
2025.04.16-14:39:45.13 - <debug> Registered op blas_sgemm from plugin noop
2025.04.16-14:39:45.13 - <debug> Registered op image_classify from plugin noop
2025.04.16-14:39:45.13 - <debug> Registered op image_detect from plugin noop
2025.04.16-14:39:45.13 - <debug> Registered op image_segment from plugin noop
2025.04.16-14:39:45.13 - <debug> Registered op image_pose from plugin noop
2025.04.16-14:39:45.13 - <debug> Registered op image_depth from plugin noop
2025.04.16-14:39:45.13 - <debug> Registered op exec from plugin noop
2025.04.16-14:39:45.13 - <debug> Registered op tf_session_load from plugin noop
2025.04.16-14:39:45.13 - <debug> Registered op tf_session_run from plugin noop
2025.04.16-14:39:45.13 - <debug> Registered op tf_session_delete from plugin noop
2025.04.16-14:39:45.13 - <debug> Registered op minmax from plugin noop
2025.04.16-14:39:45.13 - <debug> Registered op fpga_arraycopy from plugin noop
2025.04.16-14:39:45.13 - <debug> Registered op fpga_vectoradd from plugin noop
2025.04.16-14:39:45.13 - <debug> Registered op fpga_parallel from plugin noop
2025.04.16-14:39:45.13 - <debug> Registered op fpga_mmult from plugin noop
2025.04.16-14:39:45.13 - <debug> Registered op exec_with_resource from plugin noop
2025.04.16-14:39:45.13 - <debug> Registered op torch_jitload_forward from plugin noop
2025.04.16-14:39:45.13 - <debug> Registered op torch_sgemm from plugin noop
2025.04.16-14:39:45.13 - <debug> Registered op opencv from plugin noop
2025.04.16-14:39:45.13 - <debug> Registered op tflite_session_load from plugin noop
2025.04.16-14:39:45.13 - <debug> Registered op tflite_session_run from plugin noop
2025.04.16-14:39:45.13 - <debug> Registered op tflite_session_delete from plugin noop
2025.04.16-14:39:45.13 - <debug> Loaded plugin noop from libvaccel-noop.so
[2025-04-16T14:39:45Z INFO  rust_vaccel_classify] Starting vAccel classification example
[2025-04-16T14:39:45Z INFO  rust_vaccel_classify] Creating new vAccel session
2025.04.16-14:39:45.13 - <debug> New rundir for session 1: /run/user/1000/vaccel/jesuwX/session.1
2025.04.16-14:39:45.13 - <debug> Initialized session 1
[2025-04-16T14:39:45Z INFO  rust_vaccel_classify] Initialized session 1
[2025-04-16T14:39:45Z INFO  rust_vaccel_classify] Reading image file: /usr/share/vaccel/images/example.jpg
[2025-04-16T14:39:45Z INFO  rust_vaccel_classify] Read image data: 79281 bytes
[2025-04-16T14:39:45Z INFO  rust_vaccel_classify] Performing image classification
2025.04.16-14:39:45.13 - <debug> session:1 Looking for plugin implementing VACCEL_OP_IMAGE_CLASSIFY
2025.04.16-14:39:45.13 - <debug> Start profiling region vaccel_image_op
2025.04.16-14:39:45.13 - <debug> Returning func from hint plugin noop
2025.04.16-14:39:45.13 - <debug> Found implementation in noop plugin
2025.04.16-14:39:45.13 - <debug> [noop] Calling Image classification for session 1
2025.04.16-14:39:45.13 - <debug> [noop] Dumping arguments for Image classification:
2025.04.16-14:39:45.13 - <debug> [noop] model: (null)
2025.04.16-14:39:45.13 - <debug> [noop] len_img: 79281
2025.04.16-14:39:45.13 - <debug> [noop] len_out_text: 1024
2025.04.16-14:39:45.13 - <debug> [noop] len_out_imgname: 1024
2025.04.16-14:39:45.13 - <debug> [noop] will return a dummy result
2025.04.16-14:39:45.13 - <debug> [noop] will return a dummy result
2025.04.16-14:39:45.13 - <debug> Stop profiling region vaccel_image_op
[2025-04-16T14:39:45Z INFO  rust_vaccel_classify] Classification completed successfully
Classification tags: This is a dummy classification tag!
Annotated image: This is a dummy imgname!
[2025-04-16T14:39:45Z INFO  rust_vaccel_classify] Releasing session 1
2025.04.16-14:39:45.13 - <debug> Released session 1
[2025-04-16T14:39:45Z INFO  rust_vaccel_classify] Session released successfully
2025.04.16-14:39:45.13 - <debug> Cleaning up vAccel
2025.04.16-14:39:45.13 - <debug> Cleaning up sessions
2025.04.16-14:39:45.13 - <debug> Cleaning up resources
2025.04.16-14:39:45.13 - <debug> Cleaning up plugins
2025.04.16-14:39:45.13 - <debug> Unregistered plugin noop
```

