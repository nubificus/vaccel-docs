# Container runtime integration

To facilitate the deployment of vaccel-enabled applications, we integrate vAccel
to a popular container runtime, [kata-containers](https://katacontainers.io).

Kata Containers enable containers to be seamlessly executed in sandbox Virtual
Machines. Kata Containers are as light and fast as containers and integrate with
the container management layers, while also delivering the security advantages
of VMs. Kata Containers is the result of merging two existing open source
projects: Intel Clear Containers and Hyper runV.

vAccel integration to kata comes in both modes: `virtio` and `vsock`. An
overview of the software stack is shown in Figure 1.

<figure>
  <img src="/img/vaccel-vm-kata.png" width="600" align=left
    alt="vAccel integration with kata-containers" />
  <figcaption>Figure 1. vAccel integration with kata-containers</figcaption>
</figure>

Our current, downstream implementation for Kata-containers v3.X includes support
for the AWS Firecracker sandbox, and the `vsock` mode of vAccel. Visit our
[downstream branch](https://github.com/nubificus/kata-containers/tree/vaccel-v3.0)
to peak through the code or have a look at the [tutorial](kata_vaccel.md) to get
a vAccel kata-containers runtime installed in your cluster.
