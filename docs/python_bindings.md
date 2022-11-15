# Python bindings

## Initial Setup

### Install vAccelRT

In order to build the python bindings for vAccel, we first need a vAccelRT
installation. We can either [build it from source](/building), or [get
the latest binary release](/binaries).

The relevant libs & plugins should be in `/usr/local/lib`, along with include
files in `/usr/local/include`.

TL;DR

```sh
wget https://s3.nbfc.io/nbfc-assets/github/vaccelrt/master/`uname -m`/Release-deb/vaccel-0.5.0-Linux.deb
sudo dpkg -i vaccel-0.5.0-Linux.deb
```

### Install Python

To build and use the Python bindings, we need to have Python3 installed.

```sh
sudo apt-get install python3 python3-venv python3-pip
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

## Install from binaries

We provide experimental builds (as a pip wheel and binary package). Get them
through the [binaries table](/binaries#binaries) or just run the
following commands:

```sh


```


First clone the repo:

```bash
git clone https://github.com/nubificus/python-vaccel
```

Finally, call the `builder.py` to build the bindings. The required python
packages to build are: `datestamp cffi wheel setuptools cmake_build_extension`.
To install them use:

```bash
pip3 install datestamp cffi wheel setuptools cmake_build_extension
```

and run the builder:

```bash
python3 builder.py
```

The module should be ready. To test run:

```bash
export VACCEL_BACKENDS=/usr/local/lib/libvaccel-noop.so 
export LD_LIBRARY_PATH=/usr/local/lib 
export PYTHONPATH=$PYTHONPATH:. 
python3 vaccel/test.py
```
Alternatively, you could build the pip package:

```
pip3 install build
python3 -m build
```

and install it:

```
pip install dist/vaccel*.tar.gz
```


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
export VACCEL_BACKENDS=/usr/local/lib/libvaccel-noop.so 
export LD_LIBRARY_PATH=/usr/local/lib
export PYTHONPATH=.
python3 builder.py
python3 setup.py install
```

[Optional] Run the tests to make sure everything was build correctly:

```bash
python3 -m pytest
```

## Test the installation

To run the tests:

```bash
export VACCEL_BACKENDS=/usr/local/lib/libvaccel-noop.so 
export LD_LIBRARY_PATH=/usr/local/lib 
export PYTHONPATH=$PYTHONPATH:. 
pytest


# Test coverage
export VACCEL_BACKENDS=/usr/local/lib/libvaccel-noop.so 
export LD_LIBRARY_PATH=/usr/local/lib 
export PYTHONPATH=$PYTHONPATH:. 
pytest --cov=vaccel tests/
```

The output should be something like the following:

```console
$ pytest --cov=vaccel tests
=================================================== test session starts ===================================================
platform linux -- Python 3.10.7, pytest-7.2.0, pluggy-1.0.0
rootdir: /home/ananos.linux/develop/python-vaccel
plugins: cov-4.0.0
collected 13 items                                                                                                        

tests/test_general.py ..                                                                                            [ 15%]
tests/test_image.py .....                                                                                           [ 53%]
tests/test_image_genop.py .....                                                                                     [ 92%]
tests/test_tf.py .                                                                                                  [100%]

---------- coverage: platform linux, python 3.10.7-final-0 -----------
Name                    Stmts   Miss  Cover
-------------------------------------------
vaccel/__init__.py          9      0   100%
vaccel/error.py             7      3    57%
vaccel/genop.py           111     12    89%
vaccel/image.py           127     15    88%
vaccel/image_genop.py      58      1    98%
vaccel/noop.py             10      2    80%
vaccel/resource.py         11     11     0%
vaccel/session.py          26      5    81%
vaccel/tensorflow.py      206     39    81%
vaccel/test.py            102    102     0%
-------------------------------------------
TOTAL                     667    190    72%


=================================================== 13 passed in 0.04s ====================================================
Loading libvaccel
Loading plugins
Loading plugin: /usr/local/lib/libvaccel-noop.so
Loaded plugin noop from /usr/local/lib/libvaccel-noop.so
[noop] Calling no-op for session 2
[noop] Calling Image classification for session 2
[noop] Dumping arguments for Image classification:
[noop] len_img: 79281
[noop] will return a dummy result
[noop] Calling Image detection for session 2
[noop] Dumping arguments for Image detection:
[noop] len_img: 79281
[noop] Calling Image segmentation for session 2
[noop] Dumping arguments for Image segmentation:
[noop] len_img: 79281
[noop] Calling Image pose for session 2
[noop] Dumping arguments for Image pose:
[noop] len_img: 79281
[noop] Calling Image depth for session 2
[noop] Dumping arguments for Image depth:
[noop] len_img: 79281
[noop] Calling Image classification for session 2
[noop] Dumping arguments for Image classification:
[noop] len_img: 79281
[noop] will return a dummy result
[noop] Calling Image detection for session 2
[noop] Dumping arguments for Image detection:
[noop] len_img: 79281
[noop] Calling Image segmentation for session 2
[noop] Dumping arguments for Image segmentation:
[noop] len_img: 79281
[noop] Calling Image pose for session 2
[noop] Dumping arguments for Image pose:
[noop] len_img: 79281
[noop] Calling Image depth for session 2
[noop] Dumping arguments for Image depth:
[noop] len_img: 79281
[noop] Run options -> (nil), 0
[noop] Number of inputs: 1
[noop] 	Node 0: serving_default_input_1:0
[noop] 	#dims: 2 -> {1 30}
[noop] 	Data type: 1
[noop] 	Data -> 0xaaaaf5135600, 120
[noop] Number of outputs: 1
[noop] 	Node 0: StatefulPartitionedCall:0
Shutting down vAccel
```

## Run a simple python application

To see python vAccel bindings in action, let's try the following example:

### Simple Example

Donwload an adorable kitten photo:

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

### Jetson example

To use vAccel on a more real-life example we'll use the jetson-inference framework. This way we will be able to perform image inference on a GPU and get something more useful than a dummy classification tag ;-)

Let's re-use the python program from the [simple example](#simple-example) above.

#### `x86_64`

We will need to use a host with an NVIDIA GPU (our's is just an `RTX 2060
SUPER`) and jetson-inference installed. To facilitate dependency resolving we
use a [container image](/jetson#build-a-jetson-inference-container-image) on a host with nvidia-container-runtime installed.

so, assuming our code is in `/data/code` let's spawn our container and see this in action:

```sh
docker run --gpus 0 --rm -it -v/data/code:/data/ -w /data nubificus/jetson-inference-updated:x86_64 /bin/bash
```

Afterwards, the steps are more or less the same as above. Install the vAccelRT package:

```console
root@32e90efe86b9:/data/code# wget https://s3.nbfc.io/nbfc-assets/github/vaccelrt/master/x86_64/Release-deb/vaccel-0.5.0-Linux.deb
--2022-11-05 13:43:43--  https://s3.nbfc.io/nbfc-assets/github/vaccelrt/master/x86_64/Release-deb/vaccel-0.5.0-Linux.deb
Resolving s3.nbfc.io (s3.nbfc.io)... 84.254.1.240
Connecting to s3.nbfc.io (s3.nbfc.io)|84.254.1.240|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 2124230 (2.0M) [application/x-debian-package]
Saving to: 'vaccel-0.5.0-Linux.deb'

vaccel-0.5.0-Linux.deb          100%[=======================================================>]   2.03M  --.-KB/s    in 0.06s

2022-11-05 13:43:43 (33.8 MB/s) - 'vaccel-0.5.0-Linux.deb' saved [2124230/2124230]

root@32e90efe86b9:/data/code# dpkg -i vaccel-0.5.0-Linux.deb
Selecting previously unselected package vaccel.
(Reading database ... 60677 files and directories currently installed.)
Preparing to unpack vaccel-0.5.0-Linux.deb ...
Unpacking vaccel (0.5.0) ...
Setting up vaccel (0.5.0) ...
```

Get and install the jetson plugin:

```console
root@32e90efe86b9:/data/code# wget https://s3.nubificus.co.uk/nbfc-assets/github/vaccelrt/plugins/jetson_inference/master/x86_64/vaccelrt-plugin-jetson-0.1-Linux.deb
--2022-11-05 14:45:53--  https://s3.nubificus.co.uk/nbfc-assets/github/vaccelrt/plugins/jetson_inference/master/x86_64/vaccelrt-plugin-jetson-0.1-Linux.deb
Resolving s3.nubificus.co.uk (s3.nubificus.co.uk)... 84.254.1.240
Connecting to s3.nubificus.co.uk (s3.nubificus.co.uk)|84.254.1.240|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 13146 (13K) [application/x-debian-package]
Saving to: 'vaccelrt-plugin-jetson-0.1-Linux.deb'

vaccelrt-plugin-jetson-0.1-Linu 100%[=======================================================>]  12.84K  --.-KB/s    in 0.001s

2022-11-05 14:45:53 (8.39 MB/s) - 'vaccelrt-plugin-jetson-0.1-Linux.deb' saved [13146/13146]

root@32e90efe86b9:/data/code# dpkg -i vaccelrt-plugin-jetson-0.1-Linux.deb
(Reading database ... 60748 files and directories currently installed.)
Preparing to unpack vaccelrt-plugin-jetson-0.1-Linux.deb ...
Unpacking vaccelrt-plugin-jetson (0.1) over (0.1) ...
Setting up vaccelrt-plugin-jetson (0.1) ...
```

Install the bindings:

```console
root@32e90efe86b9:/data/code# .vaccel-venv/bin/pip3 install https://s3.nbfc.io/nbfc-assets/github/python-vaccel/main/x86_64/vaccel-python-0.0.1.tar.gz
Collecting https://s3.nbfc.io/nbfc-assets/github/python-vaccel/main/x86_64/vaccel-python-0.0.1.tar.gz
  Downloading https://s3.nbfc.io/nbfc-assets/github/python-vaccel/main/x86_64/vaccel-python-0.0.1.tar.gz (23 kB)
  Installing build dependencies ... done
  Getting requirements to build wheel ... done
    Preparing wheel metadata ... done
Collecting cffi>=1.0.0
  Using cached cffi-1.15.1-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (442 kB)
Collecting pycparser
  Using cached pycparser-2.21-py2.py3-none-any.whl (118 kB)
Building wheels for collected packages: vaccel
  Building wheel for vaccel (PEP 517) ... done
  Created wheel for vaccel: filename=vaccel-python-0.0.1-cp38-cp38-linux_x86_64.whl size=44494 sha256=a63bd263ba219e985821fc34416dc8f12ced508eb8e265b78a896ac2ed375f72
  Stored in directory: /root/.cache/pip/wheels/a6/e6/1c/4c91a42c1cad7e5e4ca86acd006bcded10cba25e85268e81ef
Successfully built vaccel
Installing collected packages: pycparser, cffi, vaccel
Successfully installed cffi-1.15.1 pycparser-2.21 vaccel-python-0.0.1
```


Now let's go ahead and run the example!

```
root@32e90efe86b9:/data/code# export LD_LIBRARY_PATH=/usr/local/lib/
root@32e90efe86b9:/data/code# export VACCEL_BACKENDS=/usr/local/lib/libvaccel-jetson.so
root@32e90efe86b9:/data/code# export VACCEL_IMAGENET_NETWORKS=/data/code/networks
root@32e90efe86b9:/data/code# .vaccel-venv/bin/python3 cat.py
Loading libvaccel
Loading plugins
Loading plugin: /usr/local/lib/libvaccel-jetson.so
Loaded plugin jetson-inference from ./libvaccel-jetson.so

imageNet -- loading classification network model from:
         -- prototxt     ./local_net//googlenet.prototxt
         -- model        ./local_net//bvlc_googlenet.caffemodel
         -- class_labels ./local_net//ilsvrc12_synset_words.txt
         -- input_blob   'data'
         -- output_blob  'prob'
         -- batch_size   1

[TRT]    TensorRT version 8.5.1
[TRT]    loading NVIDIA plugins...
[TRT]    Registered plugin creator - ::BatchedNMSDynamic_TRT version 1
[TRT]    Registered plugin creator - ::BatchedNMS_TRT version 1
[TRT]    Registered plugin creator - ::BatchTilePlugin_TRT version 1
[TRT]    Registered plugin creator - ::Clip_TRT version 1
[TRT]    Registered plugin creator - ::CoordConvAC version 1
[TRT]    Registered plugin creator - ::CropAndResizeDynamic version 1
[TRT]    Registered plugin creator - ::CropAndResize version 1
[TRT]    Registered plugin creator - ::DecodeBbox3DPlugin version 1
[TRT]    Registered plugin creator - ::DetectionLayer_TRT version 1
[TRT]    Registered plugin creator - ::EfficientNMS_Explicit_TF_TRT version 1
[TRT]    Registered plugin creator - ::EfficientNMS_Implicit_TF_TRT version 1
[TRT]    Registered plugin creator - ::EfficientNMS_ONNX_TRT version 1
[TRT]    Registered plugin creator - ::EfficientNMS_TRT version 1
[TRT]    Could not register plugin creator -  ::FlattenConcat_TRT version 1
[TRT]    Registered plugin creator - ::GenerateDetection_TRT version 1
[TRT]    Registered plugin creator - ::GridAnchor_TRT version 1
[TRT]    Registered plugin creator - ::GridAnchorRect_TRT version 1
[TRT]    Registered plugin creator - ::InstanceNormalization_TRT version 1
[TRT]    Registered plugin creator - ::InstanceNormalization_TRT version 2
[TRT]    Registered plugin creator - ::LReLU_TRT version 1
[TRT]    Registered plugin creator - ::MultilevelCropAndResize_TRT version 1
[TRT]    Registered plugin creator - ::MultilevelProposeROI_TRT version 1
[TRT]    Registered plugin creator - ::MultiscaleDeformableAttnPlugin_TRT version 1
[TRT]    Registered plugin creator - ::NMSDynamic_TRT version 1
[TRT]    Registered plugin creator - ::NMS_TRT version 1
[TRT]    Registered plugin creator - ::Normalize_TRT version 1
[TRT]    Registered plugin creator - ::PillarScatterPlugin version 1
[TRT]    Registered plugin creator - ::PriorBox_TRT version 1
[TRT]    Registered plugin creator - ::ProposalDynamic version 1
[TRT]    Registered plugin creator - ::ProposalLayer_TRT version 1
[TRT]    Registered plugin creator - ::Proposal version 1
[TRT]    Registered plugin creator - ::PyramidROIAlign_TRT version 1
[TRT]    Registered plugin creator - ::Region_TRT version 1
[TRT]    Registered plugin creator - ::Reorg_TRT version 1
[TRT]    Registered plugin creator - ::ResizeNearest_TRT version 1
[TRT]    Registered plugin creator - ::ROIAlign_TRT version 1
[TRT]    Registered plugin creator - ::RPROI_TRT version 1
[TRT]    Registered plugin creator - ::ScatterND version 1
[TRT]    Registered plugin creator - ::SpecialSlice_TRT version 1
[TRT]    Registered plugin creator - ::Split version 1
[TRT]    Registered plugin creator - ::VoxelGeneratorPlugin version 1
[TRT]    detected model format - caffe  (extension '.caffemodel')
[TRT]    desired precision specified for GPU: FASTEST
[TRT]    requested fasted precision for device GPU without providing valid calibrator, disabling INT8
[TRT]    [MemUsageChange] Init CUDA: CPU +307, GPU +0, now: CPU 320, GPU 223 (MiB)
[TRT]    Trying to load shared library libnvinfer_builder_resource.so.8.5.1
[TRT]    Loaded shared library libnvinfer_builder_resource.so.8.5.1
[TRT]    [MemUsageChange] Init builder kernel library: CPU +262, GPU +74, now: CPU 636, GPU 297 (MiB)
[TRT]    CUDA lazy loading is not enabled. Enabling it can significantly reduce device memory usage. See `CUDA_MODULE_LOADING` in https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#env-vars
[TRT]    native precisions detected for GPU:  FP32, FP16, INT8
[TRT]    selecting fastest native precision for GPU:  FP16
[TRT]    attempting to open engine cache file ./local_net//bvlc_googlenet.caffemodel.1.1.8501.GPU.FP16.engine
[TRT]    loading network plan from engine cache... ./local_net//bvlc_googlenet.caffemodel.1.1.8501.GPU.FP16.engine
[TRT]    device GPU, loaded ./local_net//bvlc_googlenet.caffemodel
[TRT]    Loaded engine size: 15 MiB
[TRT]    Trying to load shared library libcudnn.so.8
[TRT]    Loaded shared library libcudnn.so.8
[TRT]    Using cuDNN as plugin tactic source
[TRT]    Using cuDNN as core library tactic source
[TRT]    [MemUsageChange] Init cuDNN: CPU +576, GPU +236, now: CPU 977, GPU 477 (MiB)
[TRT]    Deserialization required 488590 microseconds.
[TRT]    [MemUsageChange] TensorRT-managed allocation in engine deserialization: CPU +0, GPU +13, now: CPU 0, GPU 13 (MiB)
[TRT]    Trying to load shared library libcudnn.so.8
[TRT]    Loaded shared library libcudnn.so.8
[TRT]    Using cuDNN as plugin tactic source
[TRT]    Using cuDNN as core library tactic source
[TRT]    [MemUsageChange] Init cuDNN: CPU +0, GPU +8, now: CPU 977, GPU 477 (MiB)
[TRT]    Total per-runner device persistent memory is 94720
[TRT]    Total per-runner host persistent memory is 147088
[TRT]    Allocated activation device memory of size 3612672
[TRT]    [MemUsageChange] TensorRT-managed allocation in IExecutionContext creation: CPU +0, GPU +3, now: CPU 0, GPU 16 (MiB)
[TRT]    CUDA lazy loading is not enabled. Enabling it can significantly reduce device memory usage. See `CUDA_MODULE_LOADING` in https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#env-vars
[TRT]
[TRT]    CUDA engine context initialized on device GPU:
[TRT]       -- layers       72
[TRT]       -- maxBatchSize 1
[TRT]       -- deviceMemory 3612672
[TRT]       -- bindings     2
[TRT]       binding 0
                -- index   0
                -- name    'data'
                -- type    FP32
                -- in/out  INPUT
                -- # dims  3
                -- dim #0  3
                -- dim #1  224
                -- dim #2  224
[TRT]       binding 1
                -- index   1
                -- name    'prob'
                -- type    FP32
                -- in/out  OUTPUT
                -- # dims  3
                -- dim #0  1000
                -- dim #1  1
                -- dim #2  1
[TRT]
[TRT]    binding to input 0 data  binding index:  0
[TRT]    binding to input 0 data  dims (b=1 c=3 h=224 w=224) size=602112
[TRT]    binding to output 0 prob  binding index:  1
[TRT]    binding to output 0 prob  dims (b=1 c=1000 h=1 w=1) size=4000
[TRT]
[TRT]    device GPU, ./local_net//bvlc_googlenet.caffemodel initialized.
[TRT]    imageNet -- loaded 1000 class info entries
[TRT]    imageNet -- ./local_net//bvlc_googlenet.caffemodel initialized.
class 0281 - 0.219604  (tabby, tabby cat)
class 0282 - 0.062927  (tiger cat)
class 0283 - 0.018173  (Persian cat)
class 0284 - 0.017746  (Siamese cat, Siamese)
class 0285 - 0.483398  (Egyptian cat)
class 0287 - 0.180664  (lynx, catamount)
imagenet: 48.33984% class #285 (Egyptian cat)
imagenet: attempting to save output image
imagenet: completed saving
imagenet: shutting down...
48.340% Egyptian cat
Shutting down vAccel
```


#### `aarch64`

For aarch64 things are more or less the same. We run the example on a Jetson
Xavier AGX, so jetson-inference and the nvidia stack is included in the Jetson
Linux variant (L4T).

The steps to take only refer to installing jetson-inference libs, vAccel and
the python bindings so assuming there's a Jetson Linux distro with Jetpack
installed:

- install jetson-inference:
```
git clone --recursive https://github.com/dusty-nv/jetson-inference
cd jetson-inference 
mkdir build
cd build
cmake ../
make install
```

- install vAccelRT:

```
wget https://s3.nubificus.co.uk/nbfc-assets/github/vaccelrt/master/aarch64/Release-deb/vaccel-0.5.0-Linux.deb
dpkg -i vaccel-0.5.0-Linux.deb
```

- install the jetson plugin:

```
wget https://s3.nubificus.co.uk/nbfc-assets/github/vaccelrt/plugins/jetson_inference/master/aarch64/vaccelrt-plugin-jetson-0.1-Linux.deb
dpkg -i vaccelrt-plugin-jetson-0.1-Linux.deb
```

- install python bindings in a virtual env:
```
python3 -m venv .vaccel-venv
.vaccel-venv/bin/pip3 install https://s3.nbfc.io/nbfc-assets/github/python-vaccel/main/aarch64/vaccel-python-0.0.1.tar.gz
```

- run the example:

```
# .vaccel-venv/bin/python3 cat.py
Loading libvaccel
2022.11.05-20:25:12.79 - <debug> Initializing vAccel
2022.11.05-20:25:12.79 - <debug> Created top-level rundir: /run/user/0/vaccel.G2ZhVr
Loading plugins
Loading plugin: /usr/local/lib/libvaccel-jetson.so
2022.11.05-20:25:12.91 - <debug> Registered plugin jetson-inference
2022.11.05-20:25:12.91 - <debug> Registered function image classification from plugin jetson-inference
2022.11.05-20:25:12.91 - <debug> Registered function image detection from plugin jetson-inference
2022.11.05-20:25:12.91 - <debug> Registered function image segmentation from plugin jetson-inference
Loaded plugin jetson-inference from /usr/local/lib/libvaccel-jetson.so
2022.11.05-20:25:12.96 - <debug> session:1 New session
Session id is 1
2022.11.05-20:25:12.96 - <debug> session:1 Looking for plugin implementing image classification
2022.11.05-20:25:12.96 - <debug> Found implementation in jetson-inference plugin

imageNet -- loading classification network model from:
         -- prototxt     /home/ananos/develop/jetson-inference/data/networks/googlenet.prototxt
         -- model        /home/ananos/develop/jetson-inference/data/networks/bvlc_googlenet.caffemodel
         -- class_labels /home/ananos/develop/jetson-inference/data/networks/ilsvrc12_synset_words.txt
         -- input_blob   'data'
         -- output_blob  'prob'
         -- batch_size   1

[TRT]    TensorRT version 8.4.1
[TRT]    loading NVIDIA plugins...
[TRT]    Registered plugin creator - ::GridAnchor_TRT version 1
[TRT]    Registered plugin creator - ::GridAnchorRect_TRT version 1
[TRT]    Registered plugin creator - ::NMS_TRT version 1
[TRT]    Registered plugin creator - ::Reorg_TRT version 1
[TRT]    Registered plugin creator - ::Region_TRT version 1
[TRT]    Registered plugin creator - ::Clip_TRT version 1
[TRT]    Registered plugin creator - ::LReLU_TRT version 1
[TRT]    Registered plugin creator - ::PriorBox_TRT version 1
[TRT]    Registered plugin creator - ::Normalize_TRT version 1
[TRT]    Registered plugin creator - ::ScatterND version 1
[TRT]    Registered plugin creator - ::RPROI_TRT version 1
[TRT]    Registered plugin creator - ::BatchedNMS_TRT version 1
[TRT]    Registered plugin creator - ::BatchedNMSDynamic_TRT version 1
[TRT]    Registered plugin creator - ::BatchTilePlugin_TRT version 1
[TRT]    Could not register plugin creator -  ::FlattenConcat_TRT version 1
[TRT]    Registered plugin creator - ::CropAndResize version 1
[TRT]    Registered plugin creator - ::CropAndResizeDynamic version 1
[TRT]    Registered plugin creator - ::DetectionLayer_TRT version 1
[TRT]    Registered plugin creator - ::EfficientNMS_TRT version 1
[TRT]    Registered plugin creator - ::EfficientNMS_ONNX_TRT version 1
[TRT]    Registered plugin creator - ::EfficientNMS_Explicit_TF_TRT version 1
[TRT]    Registered plugin creator - ::EfficientNMS_Implicit_TF_TRT version 1
[TRT]    Registered plugin creator - ::ProposalDynamic version 1
[TRT]    Registered plugin creator - ::Proposal version 1
[TRT]    Registered plugin creator - ::ProposalLayer_TRT version 1
[TRT]    Registered plugin creator - ::PyramidROIAlign_TRT version 1
[TRT]    Registered plugin creator - ::ResizeNearest_TRT version 1
[TRT]    Registered plugin creator - ::Split version 1
[TRT]    Registered plugin creator - ::SpecialSlice_TRT version 1
[TRT]    Registered plugin creator - ::InstanceNormalization_TRT version 1
[TRT]    Registered plugin creator - ::InstanceNormalization_TRT version 2
[TRT]    Registered plugin creator - ::CoordConvAC version 1
[TRT]    Registered plugin creator - ::DecodeBbox3DPlugin version 1
[TRT]    Registered plugin creator - ::GenerateDetection_TRT version 1
[TRT]    Registered plugin creator - ::MultilevelCropAndResize_TRT version 1
[TRT]    Registered plugin creator - ::MultilevelProposeROI_TRT version 1
[TRT]    Registered plugin creator - ::NMSDynamic_TRT version 1
[TRT]    Registered plugin creator - ::PillarScatterPlugin version 1
[TRT]    Registered plugin creator - ::VoxelGeneratorPlugin version 1
[TRT]    Registered plugin creator - ::MultiscaleDeformableAttnPlugin_TRT version 1
[TRT]    detected model format - caffe  (extension '.caffemodel')
[TRT]    desired precision specified for GPU: FASTEST
[TRT]    requested fasted precision for device GPU without providing valid calibrator, disabling INT8
[TRT]    [MemUsageChange] Init CUDA: CPU +187, GPU +0, now: CPU 211, GPU 3925 (MiB)
[TRT]    [MemUsageChange] Init builder kernel library: CPU +131, GPU +123, now: CPU 361, GPU 4067 (MiB)
[TRT]    native precisions detected for GPU:  FP32, FP16, INT8
[TRT]    selecting fastest native precision for GPU:  FP16
[TRT]    found engine cache file /home/ananos/develop/jetson-inference/data/networks/bvlc_googlenet.caffemodel.1.1.8401.GPU.FP16.engine
[TRT]    found model checksum /home/ananos/develop/jetson-inference/data/networks/bvlc_googlenet.caffemodel.sha256sum
[TRT]    echo "$(cat /home/ananos/develop/jetson-inference/data/networks/bvlc_googlenet.caffemodel.sha256sum) /home/ananos/develop/jetson-inference/data/networks/bvlc_googlenet.caffemodel" | sha256sum --check --status
[TRT]    model matched checksum /home/ananos/develop/jetson-inference/data/networks/bvlc_googlenet.caffemodel.sha256sum
[TRT]    loading network plan from engine cache... /home/ananos/develop/jetson-inference/data/networks/bvlc_googlenet.caffemodel.1.1.8401.GPU.FP16.engine
[TRT]    device GPU, loaded /home/ananos/develop/jetson-inference/data/networks/bvlc_googlenet.caffemodel
[TRT]    [MemUsageChange] Init CUDA: CPU +0, GPU +0, now: CPU 245, GPU 4080 (MiB)
[TRT]    Loaded engine size: 14 MiB
[TRT]    Deserialization required 15317 microseconds.
[TRT]    [MemUsageChange] TensorRT-managed allocation in engine deserialization: CPU +0, GPU +13, now: CPU 0, GPU 13 (MiB)
[TRT]    Total per-runner device persistent memory is 75776
[TRT]    Total per-runner host persistent memory is 110304
[TRT]    Allocated activation device memory of size 5218304
[TRT]    [MemUsageChange] TensorRT-managed allocation in IExecutionContext creation: CPU +0, GPU +5, now: CPU 0, GPU 18 (MiB)
[TRT]
[TRT]    CUDA engine context initialized on device GPU:
[TRT]       -- layers       72
[TRT]       -- maxBatchSize 1
[TRT]       -- deviceMemory 5218304
[TRT]       -- bindings     2
[TRT]       binding 0
                -- index   0
                -- name    'data'
                -- type    FP32
                -- in/out  INPUT
                -- # dims  3
                -- dim #0  3
                -- dim #1  224
                -- dim #2  224
[TRT]       binding 1
                -- index   1
                -- name    'prob'
                -- type    FP32
                -- in/out  OUTPUT
                -- # dims  3
                -- dim #0  1000
                -- dim #1  1
                -- dim #2  1
[TRT]
[TRT]    binding to input 0 data  binding index:  0
[TRT]    binding to input 0 data  dims (b=1 c=3 h=224 w=224) size=602112
[TRT]    binding to output 0 prob  binding index:  1
[TRT]    binding to output 0 prob  dims (b=1 c=1000 h=1 w=1) size=4000
[TRT]
[TRT]    device GPU, /home/ananos/develop/jetson-inference/data/networks/bvlc_googlenet.caffemodel initialized.
[TRT]    loaded 1000 class labels
[TRT]    imageNet -- /home/ananos/develop/jetson-inference/data/networks/bvlc_googlenet.caffemodel initialized.
class 0281 - 0.222134  (tabby, tabby cat)
class 0282 - 0.063147  (tiger cat)
class 0283 - 0.018521  (Persian cat)
class 0284 - 0.018234  (Siamese cat, Siamese)
class 0285 - 0.477663  (Egyptian cat)
class 0287 - 0.182722  (lynx, catamount)
imagenet: 47.76627% class #285 (Egyptian cat)
imagenet: attempting to save output image
imagenet: completed saving
imagenet: shutting down...
47.766% Egyptian cat
2022.11.05-20:25:16.39 - <debug> session:1 Free session
Shutting down vAccel
2022.11.05-20:25:16.45 - <debug> Shutting down vAccel
2022.11.05-20:25:16.45 - <debug> Cleaning up plugins
2022.11.05-20:25:16.45 - <debug> Unregistered plugin jetson-inference
```


