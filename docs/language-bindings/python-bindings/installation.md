# Installation

The Python bindings are implemented in the `vaccel-python` package and are
currently a WiP, supporting a subset of the vAccel operations. The
`vaccel-python` package is provided as a Wheel, installable with `pip`.

## Requirements

To use `vaccel-python` you need a valid vAccel installation. You can find more
information on how to install vAccel in the
[Installation](../../getting-started/installation.md) page.

## Latest artifacts

To install the artifacts of the latest `vaccel-python` revision:

/// tab | x86

```sh
wget https://s3.nbfc.io/nbfc-assets/github/python-vaccel/main/x86_64/vaccel_python-[[ versions.bindings.python ]]-cp310-cp310-linux_x86_64.whl
pip3 install vaccel_python-[[ versions.bindings.python ]]-cp310-cp310-linux_x86_64.whl
```

///

/// tab | ARM (64-bit)

```sh
wget https://s3.nbfc.io/nbfc-assets/github/python-vaccel/main/aarch64/vaccel_python-[[ versions.bindings.python ]]-cp310-cp310-linux_aarch64.whl
pip3 install vaccel_python-[[ versions.bindings.python ]]-cp310-cp310-linux_aarch64.whl
```

///
