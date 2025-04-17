# Welcome to vAccel Documentation

vAccel is a lightweight, modular framework designed to expose hardware
acceleration functionality to workloads running in virtualized or otherwise
isolated environments. It enables transparent offloading of compute-intensive
operations to acceleration backends, abstracting away platform-specific details
through a unified API and plugin interface.

vAccel decouples applications from hardware-specific logic, enabling binary
portability across diverse hardware platforms and system configurations,
including deployments where accelerators are not directly accessible from the
application context.

<figure>
  <!--<img src="img/vaccel-overview.svg" width="600" align=left />-->
  <img src="/assets/images/vaccel-stack.png" width="800" align=center
    alt="vAccel software stack"/>
  <figcaption>Figure 1. vAccel software stack</figcaption>
</figure>

## Core Design Principles

- Portability: Applications built with vAccel can be deployed across systems
  with differing accelerator types and configurations without requiring source
  changes or recompilation.

- Security: Supports hardware-accelerated execution within strong isolation
  boundaries, including KVM-based VMs (eg., QEMU, Firecracker, Cloud
  Hypervisor).

- Modularity: vAccel supports a plugin-based architecture for backend
  accelerators, allowing hardware-specific implementations to be developed and
  maintained independently.

- Efficiency: Communication between guest and host is handled through
  low-overhead transports such as `VirtIO`, `VSOCK`, or `TCP`, minimizing
  performance loss.

- Scalability: vAccel integrates natively with Kubernetes to support large-scale,
  multi-tenant deployments of acceleration-enabled workloads.

## Key Features

- Rich Architecture Support: Native support for amd64, arm, and arm64
  platforms, including cross-compiled deployments and heterogeneous cluster
  environments.

- CI-Driven Development: An end-to-end CI pipeline validates functionality
  across multiple backends, host/guest combinations, and transport modes. All
  core components and language bindings are continuously tested for correctness
  and performance.

- Dynamic Model Inference: Enhanced support for frameworks like PyTorch (via
  `jitload_forward`) and TensorFlow, enabling runtime-loaded model execution
  inside isolated environments.

- Language Bindings: Native bindings available for Go and Python, enabling
  rapid prototyping and integration into existing ML/AI pipelines and
  cloud-native workflows.

## vAccel Architecture

At its core, vAccel consists of:

- A core library, exposing the vAccel API to applications.

- A plugin system, where backend modules handle calls to specific accelerator
  runtimes.

This layered design allows applications to remain agnostic of the underlying accelerator or transport mechanism.

Refer to the [Architecture Overview](/design/architecture) for a detailed breakdown.

## Virtualization and Transport

vAccel is designed to operate seamlessly in virtualized environments. Instead
of relying on device pass-through or vendor-specific drivers, vAccel exposes
coarse-grained acceleration operations to guest workloads over generic,
extensible transports. Implementations include:

- VirtIO (with QEMU and Firecracker support)

- RPC (VSOCK, TCP and UNIX sockets)

These transports allow flexible deployment across a range of hypervisors and system configurations.

More details are available in the [Transport Plugin](/plugins/available-plugins/transport-plugins) documentation.

## Performance

vAccel introduces minimal overhead compared to native execution. Benchmarks
across real-world inference tasks and varied payload sizes consistently
demonstrate near-native performance, with less than 5% overhead in most
configurations.

Refer to the [Performance Analysis](/benchmarks) section for detailed results and benchmarking methodology.

## Getting Started

Explore the following sections to begin integrating vAccel into your stack:

[Quickstart Guide](/getting-started/)

[Core API Documentation](/api/)

[Language Bindings](/language-bindings/)

[Plugin Development](/tutorials/writing-your-first-plugin/)

[CI and Testing Infrastructure](/ci)

For the full documentation tree, browse the sidebar navigation.
