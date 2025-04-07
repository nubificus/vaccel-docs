# Python bindings

### Initial Setup

#### Install vAccel

In order to build the python bindings for vAccel, we first need a vAccel
installation. We can either [build it from source](user-guide/building.md), or
[get the latest binary release](user-guide/binaries.md).

The relevant libs & plugins should be in `/usr/local/lib/x86_64-linux-gnu`, along with include
files in `/usr/local/include`.

```sh
# install vAccel
wget https://s3.nbfc.io/nbfc-assets/github/vaccelrt/main/`uname -m`/Release-deb/vaccel-0.6.0-Linux.deb
sudo dpkg -i vaccel-0.6.0-Linux.deb
```

#### Install Python

To build and use the Python bindings, we need to have Python3 installed.

```sh
sudo apt-get install python3 python3-venv python3-pip
```

## Install from binaries

We provide experimental builds (as a pip wheel and binary package). Get them
through the [binaries table](user-guide/binaries.md#binaries) or just run the
following commands:

```sh

wget https://s3.nbfc.io/nbfc-assets/github/python-vaccel/main/x86_64/vaccel-python-0.0.1.tar.gz
pip3 install vaccel-python-0.0.1.tar.gz
```

You should be presented with the following output:

```console
$ pip3 install vaccel-python-0.0.1.tar.gz 
Processing ./vaccel-python-0.0.1.tar.gz
  Installing build dependencies ... done
  Getting requirements to build wheel ... done
  Installing backend dependencies ... done
  Preparing metadata (pyproject.toml) ... done
Requirement already satisfied: cffi>=1.0.0 in /usr/local/lib/python3.8/dist-packages (from vaccel-python==0.0.1) (1.15.1)
Requirement already satisfied: pycparser in /usr/local/lib/python3.8/dist-packages (from cffi>=1.0.0->vaccel-python==0.0.1) (2.21)
Building wheels for collected packages: vaccel-python
  Building wheel for vaccel-python (pyproject.toml) ... done
  Created wheel for vaccel-python: filename=vaccel_python-0.0.1-cp38-cp38-linux_x86_64.whl size=44484 sha256=f0a9e056367207690f08e78cf771f15d00b5e2d7b67fac1d56b17bbe9b6b9509
  Stored in directory: /root/.cache/pip/wheels/2e/2e/a0/f07c8ed8d59a2cb16825ef23a4ef15b34d452a3bab962fea61
Successfully built vaccel-python
Installing collected packages: vaccel-python
  Attempting uninstall: vaccel-python
    Found existing installation: vaccel-python 0.0.1
    Uninstalling vaccel-python-0.0.1:
      Successfully uninstalled vaccel-python-0.0.1
Successfully installed vaccel-python-0.0.1
```

Go ahead and run an [example](#simple-example)!


## Build from Source

### Prerequisites

In Debian-based systems, you need to have the following packages to build the python bindings for vAccel:

- cmake
- build-essential
- python3-dev
- python3-venv

You can install them using the following command:

```bash
sudo apt-get install -y cmake build-essential python3-dev python3-venv
```

### Install tools to build the bindings

Additionally, to build the bindings we need the following packages (installable
via pip3). To avoid polluting the host, we could use a virtual environment:

```sh
python3 -m venv .venv
. .venv/bin/activate
```

and install the required packages:

```sh
pip3 install datestamp cffi wheel setuptools cmake_build_extension
```
### Get the source code

Get the source code for **python-vaccel**:

```bash
git clone https://github.com/nubificus/python-vaccel.git
cd python-vaccel
```

<hr>

### Build the Python package

We will create a virtual environment to install the **python-vaccel** package inside the root directory of **python-vaccel**.

```bash
python3 -m venv venv
```

Now, go ahead and activate the newly created environment:

```bash
. venv/bin/activate
```

Update pip and install Python's dependencies:

```bash
python3 -m pip install --upgrade pip
python3 -m pip install wheel
python3 -m pip install flake8 build setuptools \
    cffi pytest pytest-cov datestamp cmake_build_extension
```

Now let's build the package:

```bash
export VACCEL_PLUGINS=/usr/local/lib/x86_64-linux-gnu/libvaccel-noop.so
export LD_LIBRARY_PATH=/usr/local/lib/x86_64-linux-gnu/
export PYTHONPATH=.
python3 builder.py
python3 setup.py install
```

[Optional] Run the tests to make sure everything was build correctly:

```bash
python3 -m pytest
```

### Test the installation

To run the tests:

```bash
export VACCEL_PLUGINS=/usr/local/lib/x86_64-linux-gnu/libvaccel-noop.so
export LD_LIBRARY_PATH=/usr/local/lib/x86_64-linux-gnu/
export PYTHONPATH=$PYTHONPATH:. 
pytest


# Test coverage
export VACCEL_PLUGINS=/usr/local/lib/x86_64-linux-gnu/libvaccel-noop.so
export LD_LIBRARY_PATH=/usr/local/lib/x86_64-linux-gnu/
export PYTHONPATH=$PYTHONPATH:. 
pytest --cov=vaccel tests/
```

The output should be something like the following:

```console
$ pytest --cov=vaccel tests
=============================== test session starts ================================
platform linux -- Python 3.10.12, pytest-8.3.4, pluggy-1.5.0
rootdir: /home/mgkeka/python-vaccel
configfile: pyproject.toml
plugins: cov-6.0.0
collected 19 items

tests/test_exec.py .                                                         [  5%]
tests/test_general.py ..                                                     [ 15%]
tests/test_image.py .....                                                    [ 42%]
tests/test_image_genop.py .....                                              [ 68%]
tests/test_minmax.py .                                                       [ 73%]
tests/test_pynq_ops.py ...                                                   [ 89%]
tests/test_sgemm.py .                                                        [ 94%]
tests/test_tf.py .                                                           [100%]

---------- coverage: platform linux, python 3.10.12-final-0 ----------
Name                        Stmts   Miss  Cover
-----------------------------------------------
vaccel/__init__.py              9      0   100%
vaccel/error.py                 7      3    57%
vaccel/exec.py                 53      7    87%
vaccel/genop.py               139     22    84%
vaccel/image.py               127     15    88%
vaccel/image_genop.py          58      1    98%
vaccel/minmax.py               34      1    97%
vaccel/noop.py                 10      2    80%
vaccel/pynq_array_copy.py      17      0   100%
vaccel/pynq_parallel.py        17      0   100%
vaccel/pynq_vector_add.py      18      0   100%
vaccel/resource.py             48     18    62%
vaccel/session.py              19      3    84%
vaccel/sgemm.py                17      0   100%
vaccel/tensorflow.py          175     25    86%
vaccel/test.py                138    138     0%
-----------------------------------------------
TOTAL                         886    235    73%


================================ 19 passed in 0.16s ================================
Loading libvaccel
```

## Run a simple python application

To see python vAccel bindings in action, let's try the following example:

### Simple Example

Download an adorable kitten photo:

```bash
wget https://i.imgur.com/aSuOWgU.jpeg -O cat.jpeg
```

<hr>

Create a new python file called **cat.py** and add the following lines:

```python
from vaccel.session import Session
from vaccel.image import ImageClassify

source = "cat.jpeg"

def main():
    ses = Session(flags=3)
    print(f'Session id is {ses.id()}')
    res = ImageClassify.classify_from_filename(session=ses, source=source)
    print(res)

if __name__=="__main__":
    main()
```

Now, when you run that python file, you can see the dummy classification tag for that image:

```console
$ export VACCEL_BACKENDS=/usr/local/lib/libvaccel-noop.so 
$ export LD_LIBRARY_PATH=/usr/local/lib
$ export PYTHONPATH=.
$ python3 cat.py
Loading libvaccel
Loading plugins
Loading plugin: /usr/local/lib/libvaccel-noop.so
Loaded plugin noop from /usr/local/lib/libvaccel-noop.so
Session id is 1
[noop] Calling Image classification for session 1
[noop] Dumping arguments for Image classification:
[noop] len_img: 54372
[noop] will return a dummy result
This is a dummy classification tag!
Shutting down vAccel
```

### Classification example

To use vAccel on a more real-life example we'll use the vAccel torch plugin. This way we will be able to perform image classification and get something more useful than a dummy classification tag ;-)

Let's re-use the python program from the [simple example](#simple-example) above.
We will use the 


Afterwards, the steps are more or less simple. Install the vAccel package:

```console
root@32e90efe86b9:/data/code# wget https://s3.nbfc.io/nbfc-assets/github/vaccelrt/main/x86_64/Release-deb/vaccel-0.6.0-Linux.deb
--2022-11-05 13:43:43--  https://s3.nbfc.io/nbfc-assets/github/vaccelrt/main/x86_64/Release-deb/vaccel-0.6.0-Linux.deb
Resolving s3.nbfc.io (s3.nbfc.io)... 84.254.1.240
Connecting to s3.nbfc.io (s3.nbfc.io)|84.254.1.240|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 2124230 (2.0M) [application/x-debian-package]
Saving to: 'vaccel-0.6.0-Linux.deb'

vaccel-0.6.0-Linux.deb          100%[=======================================================>]   2.03M  --.-KB/s    in 0.06s

2022-11-05 13:43:43 (33.8 MB/s) - 'vaccel-0.6.0-Linux.deb' saved [2124230/2124230]

root@32e90efe86b9:/data/code# dpkg -i vaccel-0.6.0-Linux.deb
Selecting previously unselected package vaccel.
(Reading database ... 60677 files and directories currently installed.)
Preparing to unpack vaccel-0.6.0-Linux.deb ...
Unpacking vaccel (0.6.0) ...
Setting up vaccel (0.6.0) ...
```

Get the torch plugin:

```console
mkdir plugins
cd plugins
wget https://s3.nbfc.io/nbfc-assets/github/vaccel/plugins/torch/rev/main/x86_64/debug/vaccel-torch-latest-bin.tar.gz
--2025-04-06 08:23:33--  https://s3.nbfc.io/nbfc-assets/github/vaccel/plugins/torch/rev/main/x86_64/debug/vaccel-torch-latest-bin.tar.gz
Resolving s3.nbfc.io (s3.nbfc.io)... 84.254.1.240
Connecting to s3.nbfc.io (s3.nbfc.io)|84.254.1.240|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 2377020 (2.3M) [application/gzip]
Saving to: ‘vaccel-torch-latest-bin.tar.gz’

vaccel-torch-latest 100%[===================>]   2.27M   532KB/s    in 6.5s

2025-04-06 08:23:40 (358 KB/s) - ‘vaccel-torch-latest-bin.tar.gz’ saved [2377020/2377020]
```

Untar the dowloaded plugin:
```console
tar xvf $(ls vaccel-torch-*.tar.gz)
vaccel-torch-0.1.0-25-ab85fa03/
vaccel-torch-0.1.0-25-ab85fa03/usr/
vaccel-torch-0.1.0-25-ab85fa03/usr/lib/
vaccel-torch-0.1.0-25-ab85fa03/usr/lib/x86_64-linux-gnu/
vaccel-torch-0.1.0-25-ab85fa03/usr/lib/x86_64-linux-gnu/libvaccel-torch.so.0
vaccel-torch-0.1.0-25-ab85fa03/usr/lib/x86_64-linux-gnu/libvaccel-torch.so
vaccel-torch-0.1.0-25-ab85fa03/usr/lib/x86_64-linux-gnu/pkgconfig/
vaccel-torch-0.1.0-25-ab85fa03/usr/lib/x86_64-linux-gnu/pkgconfig/vaccel-torch.pc
vaccel-torch-0.1.0-25-ab85fa03/usr/lib/x86_64-linux-gnu/libvaccel-torch.so.0.1.0
```
For simplicity we rename the plugin folder.
```console
rm $(ls vaccel-plugin-torch*tar.xz)
for dir in vaccel-torch-*; do   mv "$dir" "vaccel-plugin-torch"; done
```
We keep the path `~/plugins/vaccel-plugin-torch/usr/lib/x86_64-linux-gnu/libvaccel-torch.so` for the plugin library. Now, under the `python-vaccel` directory, we will run the `test_image_classify()` function of the `vaccel/test.py` file by using as argument the ML model we want to use. We set the `main` function as follows:
```console
if __name__ == "__main__":
    test_image_classify("https://s3.nbfc.io/torch/resnet18.pt")
```

Now, to run the example:
```console
export VACCEL_PLUGINS=~/plugins/vaccel-plugin-torch/usr/lib/x86_64-linux-gnu/libvaccel-torch.so
export PYTHONPATH=$PYTHONPATH:.
export VACCEL_LOG_LEVEL=4
python3 vaccel/test.py
```
The output is:
```
2025.04.06-08:38:08.28 - <debug> Initializing vAccel
2025.04.06-08:38:08.28 - <info> vAccel 0.6.1-194-19056528
2025.04.06-08:38:08.28 - <debug> Config:
2025.04.06-08:38:08.28 - <debug>   plugins = /home/mgkeka/plugins/vaccel-plugin-torch/usr/lib/x86_64-linux-gnu/libvaccel-torch.so
2025.04.06-08:38:08.28 - <debug>   log_level = debug
2025.04.06-08:38:08.28 - <debug>   log_file = (null)
2025.04.06-08:38:08.28 - <debug>   profiling_enabled = false
2025.04.06-08:38:08.28 - <debug>   version_ignore = false
2025.04.06-08:38:08.28 - <debug> Created top-level rundir: /run/user/1008/vaccel/TzKbS2
2025.04.06-08:38:08.83 - <info> Registered plugin torch 0.1.0-25-ab85fa03
2025.04.06-08:38:08.83 - <debug> Registered op torch_jitload_forward from plugin torch
2025.04.06-08:38:08.83 - <debug> Registered op torch_sgemm from plugin torch
2025.04.06-08:38:08.83 - <debug> Registered op image_classify from plugin torch
2025.04.06-08:38:08.83 - <debug> Loaded plugin torch from /home/mgkeka/plugins/vaccel-plugin-torch/usr/lib/x86_64-linux-gnu/libvaccel-torch.so
Loading libvaccel
2025.04.06-08:38:08.83 - <debug> Reloading vAccel
2025.04.06-08:38:08.83 - <debug> Cleaning up vAccel
2025.04.06-08:38:08.83 - <debug> Cleaning up sessions
2025.04.06-08:38:08.83 - <debug> Cleaning up resources
2025.04.06-08:38:08.83 - <debug> Cleaning up plugins
2025.04.06-08:38:08.83 - <debug> Unregistered plugin torch
2025.04.06-08:38:08.83 - <debug> Initializing vAccel
2025.04.06-08:38:08.83 - <info> vAccel 0.6.1-194-19056528
2025.04.06-08:38:08.83 - <debug> Config:
2025.04.06-08:38:08.83 - <debug>   plugins = /home/mgkeka/plugins/vaccel-plugin-torch/usr/lib/x86_64-linux-gnu/libvaccel-torch.so
2025.04.06-08:38:08.83 - <debug>   log_level = debug
2025.04.06-08:38:08.83 - <debug>   log_file = (null)
2025.04.06-08:38:08.83 - <debug>   profiling_enabled = false
2025.04.06-08:38:08.83 - <debug>   version_ignore = false
2025.04.06-08:38:08.83 - <debug> Created top-level rundir: /run/user/1008/vaccel/Pp9r5K
2025.04.06-08:38:08.83 - <info> Registered plugin torch 0.1.0-25-ab85fa03
2025.04.06-08:38:08.83 - <debug> Registered op torch_jitload_forward from plugin torch
2025.04.06-08:38:08.83 - <debug> Registered op torch_sgemm from plugin torch
2025.04.06-08:38:08.83 - <debug> Registered op image_classify from plugin torch
2025.04.06-08:38:08.83 - <debug> Loaded plugin torch from /home/mgkeka/plugins/vaccel-plugin-torch/usr/lib/x86_64-linux-gnu/libvaccel-torch.so
Image classify test
2025.04.06-08:38:08.85 - <debug> New rundir for session 1: /run/user/1008/vaccel/Pp9r5K/session.1
2025.04.06-08:38:08.85 - <debug> Initialized session 1
Session id is 1
2025.04.06-08:38:08.85 - <debug> Initialized resource 1
2025.04.06-08:38:08.85 - <debug> New rundir for resource 1: /run/user/1008/vaccel/Pp9r5K/resource.1
2025.04.06-08:38:08.85 - <debug> Downloading https://s3.nbfc.io/torch/resnet18.pt
2025.04.06-08:38:13.88 - <debug> Downloaded: 714.2 KB of 44.7 MB (1.6%) | Speed: 142.16 KB/sec
2025.04.06-08:38:18.88 - <debug> Downloaded: 7.0 KB of 44.7 MB (15.6%) | Speed: 711.25 KB/sec
2025.04.06-08:38:23.88 - <debug> Downloaded: 19.2 MB of 44.7 MB (43.0%) | Speed: 1.28 MB/sec
2025.04.06-08:38:28.96 - <debug> Downloaded: 30.3 MB of 44.7 MB (67.7%) | Speed: 1.51 MB/sec
2025.04.06-08:38:33.96 - <debug> Downloaded: 40.6 MB of 44.7 MB (90.7%) | Speed: 1.62 MB/sec
2025.04.06-08:38:35.94 - <debug> Downloaded: 44.7 MB of 44.7 MB (100.0%) | Speed: 1.65 MB/sec
2025.04.06-08:38:35.94 - <debug> Download completed successfully
2025.04.06-08:38:35.95 - <debug> session:1 Registered resource 1
2025.04.06-08:38:35.95 - <debug> session:1 Looking for plugin implementing VACCEL_OP_IMAGE_CLASSIFY
2025.04.06-08:38:35.95 - <debug> Returning func from hint plugin torch
2025.04.06-08:38:35.95 - <debug> Found implementation in torch plugin
2025.04.06-08:38:36.26 - <debug> [torch] Model loaded successfully from: /run/user/1008/vaccel/Pp9r5K/resource.1/resnet18.pt
2025.04.06-08:38:36.44 - <debug> [torch] Prediction: banana
banana
PLACEHOLDER

2025.04.06-08:38:36.45 - <debug> session:1 Unregistered resource 1
2025.04.06-08:38:36.45 - <debug> Removing file /run/user/1008/vaccel/Pp9r5K/resource.1/resnet18.pt
2025.04.06-08:38:36.47 - <debug> Released resource 1
2025.04.06-08:38:36.47 - <debug> Released session 1
2025.04.06-08:38:36.60 - <debug> Cleaning up vAccel
2025.04.06-08:38:36.60 - <debug> Cleaning up sessions
2025.04.06-08:38:36.60 - <debug> Cleaning up resources
2025.04.06-08:38:36.60 - <debug> Cleaning up plugins
2025.04.06-08:38:36.60 - <debug> Unregistered plugin torch
```
