# Welcome to vAccel

vAccel is a framework offering hardware acceleration primitive with focus on
protability. It exposes to programmers "acceleratable" functions and abstracts
away hardware complexity by means of a pluggable design.

The design goals of vAccel are:

1. **portability**: vAccel applications can be deployed in machines with
different hardware accelerators without re-writing or re-compilation.
2. **security**: A vAccel application can be deployed, *as is*, in a VM to
ensure isolation in multi-tenant environments. QEMU and
[AWS Firecracker](https://firecracker-microvm.github.io/) VMMs are currently
supported
3. **compatibility**: vAccel supports the OCI container format through integration
with the [Kata containers](https://katacontainers.io/) framework.
4. **low-overhead**: vAccel uses a very efficient transport layer for offloading
acceleratable functions from insde the VM to the host, incuring minimum overhead.
5. **scalability**: Integration with k8s allows deployment of vAccel applications
at scale.

## vAccel design

<figure>
  <img src="img/vaccel.svg" width="600" align=left />
  <figcaption>vAccel runtime stack</figcaption>
</figure>

The core component of vAccel is the vaccel runtime (vAccelRT). vAccelRT is
designed in a modular way. The core runtime exposes the vAccel API to user
applications and dispatches requests to one of many *backend plugins*, which
are the components that implement the vAccel API on a particular hardware
accelerator.

The user application links against the core runtime library and the plugin
modules are loaded at runtime by the runtime. This workflow decouples the
application from the hardware accelerator-specific parts of the stack, allowing
for seamless migration of the same binary to different platforms with different
accelerator capabilities, without the need to recomplile user code.

### Hardware acceleration in Virtual Machines

Hardware acceleration for virtualized guests is a difficult to tackle problem.
Typical solutions involve device pass-through and paravirtual drivers that
exposes hardware semantics inside the guest. vAccel differentiates itself from
these approaches by exposing coarse grain "acceleratable" functions in the guest
over a custom transport layer.

## Performance

## 
