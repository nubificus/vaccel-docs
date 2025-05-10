# Architecture

The vAccel framework is designed to enable transparent and secure offloading of
hardware-accelerated operations from sandboxed workloads (eg., VMs, containers)
to the host. Its architecture is centered on a unified, plugin-based model that
abstracts execution, allowing for portability, flexibility, and minimal runtime
overhead.

## System overview

At a high level, vAccel consists of:

1. The **core library** that:

    - Exposes the API and is linked into user-space applications
    - Matches API operations to the underlying plugins

2. The **plugins** that handle the execution of operations:

    - A set of transport plugins, which facilitate communication between hosts
    - A set of backend plugins, which execute acceleration operations

All components interact through a well-defined API that ensures consistency and
extensibility.

![vAccel software stack](../assets/images/vaccel-stack-light.svg#only-light){width="800"}
![vAccel software stack](../assets/images/vaccel-stack-dark.svg#only-dark){width="800"}

/// caption  
vAccel software stack  
///

## Core library

The vAccel runtime library is responsible for exposing the vAccel API to user
applications, handling serialization/deserialization of operation requests,
coordinating plugins through a modular and extensible logic. The library is
written in C and is available as a shared library. It provides the base for
language bindings in Python and Go.

### API layer

The API is semantically expressive and targets coarse-grained operations like:

- ML model inference

- Image inference operations (eg. classification, segmentation etc.)

- Library-specific operations (eg. OpenCV)

- Vector operations (BLAS-related, like SGEMM etc.)

Internally, each operation is mapped to a plugin capability, abstracting
hardware or transport-specific behavior.

!!! info

    For more information on the API and the available operations see the
    [API](../api/index.md) section.

### Plugin subsystem

The vAccel plugin model provides modularity and isolation. All offload logic is
encapsulated in dynamically loadable shared objects that adhere to the vAccel
Plugin ABI.

#### Plugin types

##### Acceleration plugins

Acceleration plugins perform the actual execution of acceleration functions
using host-side libraries, hardware drivers, or frameworks (eg., CUDA, OpenCL,
neural accelerators, etc.).

They must:

- Implement the function(s) described in the vAccel API

- Register capabilities during initialization

- Handle requests from the core library (via the dispatch layer)

Each plugin is isolated from others and loaded only when required, minimizing
resource footprint and improving security.

##### Transport plugins

Transport plugins implement the guest ↔ host communication layer. They handle
request framing, sending, and receiving, enabling the core runtime to be
decoupled from specific transport mechanisms.

Examples include:

- `virtio`: Paravirtualized transport using memory-mapped buffers (via patched
  QEMU or Firecracker)

- `rpc`: Generic socket-based plugin with support for `VSOCK`, `TCP`, and `UNIX`
  sockets

These are configured at runtime, allowing per-deployment customization.

!!! info

    You can learn more about the available plugins and their usage in the
    [Plugins](../plugins/index.md) section.

## Execution model

The execution of an acceleration operation typically follows this path:

1. The user application invokes a vAccel API call.

2. The core library encodes the request into an internal format.

3. The transport plugin transmits the encoded message to the host.

4. On the host, the backend plugin receives and decodes the request.

5. The operation is executed using the corresponding hardware or framework.

6. The result is serialized and returned via the transport plugin.

This separation ensures that the application is agnostic to where and how
execution happens, that plugins can evolve independently, and that hardware
heterogeneity is abstracted away.

![vAccel workflow](../assets/images/vaccel-workflow-light.svg#only-light){width="800"}
![vAccel workflow](../assets/images/vaccel-workflow-dark.svg#only-dark){width="800"}

/// caption  
vAccel execution flow  
///

## Multi-Architecture Support

vAccel is fully portable and supports:

- `amd64`: Main development and reference architecture

- `arm64`: Optimized for edge and embedded devices (eg., NVIDIA Jetsons,
  Raspberry Pi variants etc.)

- `arm`: Deeply embedded environments (eg. Switch ASICs, FPGAs etc.)

Cross-compilation is supported via Meson and platform-specific build toolchains.
CI workflows validate plugin compatibility and API coverage across
architectures.

## Continuous integration (CI) and testing

A key enabler of robustness and portability is vAccel's integrated CI
infrastructure:

- Builds and tests all components (core, plugins) on `amd64`, `arm64`, and
  `arm`.

- Runs automated functional and integration tests for all supported transports

- Validates plugin ABI compatibility across versions

- Ensures conformance of Python and Go bindings with the C runtime

!!! info

    The CI infrastructure is described in more detail in the
    [CI](../development/ci.md) page.

## Extending vAccel

vAccel's architecture encourages third-party contributions for:

- Plugin Development: Polish / Enhance / Extend existing
  [plugins](../plugins/available-plugins/bundled-plugins) or provide additional
  [plugins](../plugins/available-plugins/acceleration-plugins/index.md) for existing [API
  operations](../api/api-guide/operations.md)

- [Transport Protocol Enhancements](https://github.com/nubificus/vaccel-rust/tree/main/vaccel-rpc-proto/protos)

vAccel’s modularity allows integration with novel transports, custom
accelerators, or domain-specific runtimes (e.g., FPGA toolchains, DSPs, AI
frameworks).
