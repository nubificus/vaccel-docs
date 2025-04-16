# Testbed Description

To ensure that our performance analysis accurately reflects real-world
deployment scenarios, we run benchmarks across a diverse set of platforms that
represent both edge and cloud environments. Our testbed spans ARM and x86
architectures and includes a variety of host and virtualized configurations.

### Hardware Platforms

| **Device**             | **CPU**                  | **RAM**   | **Accelerator**           | **Notes**                        |
|------------------------|--------------------------|-----------|--------------------------|----------------------------------|
| Jetson AGX Orin Dev Kit | 8-core ARM              | 32 GB     | NVIDIA Ampere           | JetPack 6.3.0 (Ubuntu 22.04)     |
| x86 Machine             | AMD Ryzen 5 (6-core)    | 64 GB     | NVIDIA RTX 2060 SUPER   | CUDA-capable GPU                 |
| Equinix Metal (x86)     | AMD EPYC 7401P (24-core)| 256 GB    | —                       | Server-class performance         |
| Equinix Metal (ARM64)   | Ampere Altra (80-core)  | 256 GB    | —                       | High-density ARM test node       |


### Software Stack

| **Component**         | **Details**                                |
|-----------------------|---------------------------------------------|
| Host OS              | Ubuntu 24.04                                |
| Guest OS (VM)        | Ubuntu (based on container image `ubuntu:24.04`)                     |
| Kernel (VM)          | Linux 6.1.132                               |
| Hypervisors          | QEMU v9, Firecracker v1.7.0                |
| Acceleration Frameworks | CUDA 12, Torch v2.6, TVM v0.19              |
| Compilers/Toolchains | GCC/G++ 11 & 13, Clang/LLVM 17             |


All systems are configured with the same compiler toolchains to maintain
consistency in runtime behavior across architectures and platforms.

