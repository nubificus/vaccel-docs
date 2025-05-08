# Installation

The Python bindings are implemented in the `vaccel` package and are currently a
WiP, supporting a subset of the vAccel operations. The package is installable
with `pip` by using the provided Wheels or from source.

## Requirements

- To use `vaccel` you need a valid vAccel installation. You can find more
  information on how to install vAccel in the
  [Installation](../../getting-started/installation.md) page.

<!-- markdownlint-disable blanks-around-fences -->

- This package requires Python 3.10 or newer. Verify your Python version with:
    ```sh
    python3 --version
    ```
    and update Python as needed using the
    [official instructions](https://docs.python.org/3/using/index.html)

<!-- markdownlint-restore -->

## Wheel

You can get the latest `vaccel` Wheel package from the
[Releases](https://github.com/nubificus/vaccel-python/releases) page of the
[vAccel Python repository](https://github.com/nubificus/vaccel-python). Releases
include Wheels for x86_64/aarch64/armv7l systems.

To install the Wheel package of the latest `vaccel` release:

/// tab | x86

```sh
wget https://github.com/nubificus/vaccel-python/releases/download/v[[ versions.bindings.python ]]/vaccel-[[ versions.bindings.python ]]-cp310-abi3-linux_x86_64.whl
pip install vaccel-[[ versions.bindings.python ]]-cp310-abi3-linux_x86_64.whl
```

///

/// tab | ARM (64-bit)

```sh
wget https://github.com/nubificus/vaccel-python/releases/download/v[[ versions.bindings.python ]]/vaccel-[[ versions.bindings.python ]]-cp310-abi3-linux_aarch64.whl
pip install vaccel-[[ versions.bindings.python ]]-cp310-abi3-linux_aarch64.whl
```

///

/// tab | ARM (32-bit)

```sh
wget https://github.com/nubificus/vaccel-python/releases/download/v[[ versions.bindings.python ]]/vaccel-[[ versions.bindings.python ]]-cp310-abi3-linux_armv7l.whl
pip install vaccel-[[ versions.bindings.python ]]-cp310-abi3-linux_armv7l.whl
```

///

## Latest artifacts

To install the Wheel artifact of the latest `vaccel` revision:

/// tab | x86

```sh
wget https://s3.nbfc.io/nbfc-assets/github/vaccel-python/main/x86_64/vaccel-latest-cp310-abi3-linux_x86_64.whl
pip install vaccel-latest-cp310-abi3-linux_x86_64.whl
```

///

/// tab | ARM (64-bit)

```sh
wget https://s3.nbfc.io/nbfc-assets/github/vaccel-python/main/aarch64/vaccel-latest-cp310-abi3-linux_aarch64.whl
pip install vaccel-latest-cp310-abi3-linux_aarch64.whl
```

///

/// tab | ARM (32-bit)

```sh
wget https://s3.nbfc.io/nbfc-assets/github/vaccel-python/main/armv7l/vaccel-latest-cp310-abi3-linux_armv7l.whl
pip install vaccel-latest-cp310-abi3-linux_armv7l.whl
```

///

## Building from source

You can build the package from source directly and install it using `pip`:

```sh
pip install git+https://github.com/nubificus/vaccel-python
```

## Running the examples

Examples of using the package are provided in the
[examples](https://github.com/nubificus/vaccel-python/tree/main/examples)
directory.

After cloning the repo:

```sh
git clone https://github.com/nubificus/vaccel-python
cd vaccel-python
```

you can run all the available examples with sample arguments using:

```sh
python3 run-examples.py
```
