# Benchmark Methodology

To assess the performance characteristics of vAccel, we define several
representative execution modes and evaluate them using the same workload, an
image classification example, across varying input sizes. Each benchmark is
repeated multiple times, and outliers are discarded to ensure statistical
relevance.

All experiments aim to quantify the incremental overhead introduced at each
stage of the stack: from library dispatch and plugin loading to inter-VM
communication and cross-host RPC.

## Execution Modes

We evaluate the following configurations:

- **Baseline (Native)** Direct execution of the acceleration logic, using
  lightly instrumented versions of the original frameworks (e.g., Jetson
  Inference, libtorch, TVM), to align with what vAccel measures. This serves as
  our ground truth.

- **vAccel (Local)** A direct library call to the vAccel runtime and plugin
  system within the same environment (no guest/host separation). This highlights
  internal overhead from runtime initialization, argument marshaling, dispatch
  logic, and plugin invocation.

- **vAccel (VirtIO)** Running inside a QEMU-based VM, this mode uses the virtio
  transport plugin to offload acceleration tasks to the host system. We measure
  overhead due to the virtual transport driver and backend routing.

- **vAccel (RPC - VSOCK)** Using Firecracker and QEMU as the hypervisors, this
  configuration employs the RPC plugin over `AF_VSOCK` for guest-host
  communication. This exposes the cost of the transport abstraction, including
  (de)serialization and the `VSOCK` channel.

- **vAccel (RPC - TCP)** Finally, we assess performance in a distributed
  setting, where the guest VM communicates with a host agent over TCP,
  potentially running on a remote host. This simulates realistic edge/cloud
  deployments and quantifies network-induced latency.

## Workloads

All benchmarks are based on an image classification example using three
"hardware" plugins:

- **Jetson-Inference** NVIDIA-optimized inference using TensorRT, tested on
  Jetson-class devices and x86 with CUDA.

- **Torch** PyTorch models loaded using the `jitloadforward` interface of the
  vAccel Torch plugin. We target generic models such as the ResNet series
  (18-152).

- **TVM** Inference using the Apache TVM plugin with precompiled model
  artifacts, focused on portable performance across hardware targets.

We use a variety of input image resolutions and sizes to observe how overhead
scales with workload size.

## Measurement Strategy

Each benchmark measures:

- _End-to-End Latency_: From API invocation to result reception, including
  dispatch and execution.

- _Transport Overhead_: For non-local scenarios, time taken by the communication
  stack alone (measured using timestamp hooks).

- _Plugin Execution Time_: Actual time spent in the backend plugin (e.g., torch,
  tvm).

- _Relative Overhead_: Computed as the percentage increase compared to
  baseline/native execution.

All runs are repeated for over 1000 iterations with no statistical filtering,
reporting the average time for each run. Where explicitly noted, we include the
model loading time. In all other cases, we measure the time needed just for
inference.
