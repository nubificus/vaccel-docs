# vAccel on Unikernels

Unikernels are stripped down OS kernels, bundled with a single application. It
is a form of application packaging and deployment, tailored for efficiency,
security, and immutability.

Unikernels are [unfit for
production](https://www.tritondatacenter.com/blog/unikernels-are-unfit-for-production)
(sic!) but provide an ideal solution for short-lived tasks in a busy cluster.
Unikernels scale much easier than VMs (or sandboxed containers), are inherently
immutable, and their binaries are easily reproducible. 

One of the limitations current unikernel frameworks impose is the use of
hardware acceleration: Acceleration frameworks such as CUDA for NVIDIA GPUs or
even Tensorflow or PyTorch have many library dependencies, and complicated
build systems that render the task of porting the code to a unikernel framework
literally impossible.

In an effort to explore this space, we tried porting a subset of vAccel to
various unikernel frameworks. Currently we support
[Unikraft](https://unikraft.io) and
[Rumprun](https://github.com/rumpkernel/rumprun), although adding support for
[OSv](https://osv.io/) or [IncludeOS](https://www.includeos.org/) should be
pretty straightforward.

In this space we include some rough instructions on how to test [vAccel with
Unikraft](/unikernels/unikraft).
