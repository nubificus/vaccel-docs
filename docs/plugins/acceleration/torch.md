# vAccel Torch Plugin

The Torch plugin implements various LibTorch-related vAccel operations vAccel operations. More specifically, the included operations are:

### `VACCEL_OP_TORCH_JITLOAD_FORWARD`
The generic Torch operation, which can be used to run inference on any PyTorch model, having tensors as input and output. The function signature is the following:
```C
int vaccel_torch_jitload_forward(struct vaccel_session *sess,
				 const struct vaccel_resource *model,
				 const struct vaccel_torch_buffer *run_options,
				 struct vaccel_torch_tensor **in_tensor,
				 int nr_read,
				 struct vaccel_torch_tensor **out_tensor,
				 int nr_write);
```
- `struct vaccel_session *sess`: a pointer to a vAccel session, created with
  `vaccel_session_init()`.
- `const struct vaccel_resource *model`: a vAccel resource structure to hold
   the model. It should have been previously created with `vaccel_resource_init()`
   or similar vAccel function and registered to the input session by using
  `vaccel_resource_register()`.
- `const struct vaccel_torch_buffer *run_options`: a buffer to hold other data that
   may be useful for the plugin. It may be empty.
- `struct vaccel_torch_tensor **in_tensor`: the input tensors to be used for the
   model inference.
- `int nr_read`: the number of the input tensors.
- `struct vaccel_torch_tensor **out_tensor`: this tensor array will hold the output
   tensors after the end of the operation.
- `int nr_write`: the number of the output tensors.

### `VACCEL_OP_TORCH_SGEMM`
An operation that performs the classic single-precision general matrix multiplication (SGEMM).
```C
int vaccel_torch_sgemm(struct vaccel_session *sess,
		       struct vaccel_torch_tensor **in_A,
		       struct vaccel_torch_tensor **in_B,
		       struct vaccel_torch_tensor **in_C, int M, int N, int K,
		       struct vaccel_torch_tensor **out);
```
- `struct vaccel_session *sess`: a pointer to a vAccel session created using
  `vaccel_session_init()`.
- `struct vaccel_torch_tensor **in_A`: pointer to input tensor A.
- `struct vaccel_torch_tensor **in_B`: pointer to input tensor B.
- `struct vaccel_torch_tensor **in_C`: pointer to input tensor C.
- `int M`: first dimension of matrix A & matrix C.
- `int N`: second dimension of matrix B & matrix C.
- `int K`: second dimension of matrix A & first dimension of matrix B.
- `struct vaccel_torch_tensor **out`: the tensor that will hold the output tensor.

### `VACCEL_OP_IMAGE_CLASSIFY`
the Image classification operation, which receives an image (in the form of bytes) and a PyTorch model (as a vAccel resource) and returns the classification labels. 
```C
int vaccel_image_classification(struct vaccel_session *sess, const void *img,
				unsigned char *out_text, unsigned char *out_imgname,
				size_t len_img, size_t len_out_text, size_t len_out_imgname);
```

- `struct vaccel_session *sess`: a pointer to a vAccel session created using
  `vaccel_session_init()`.
- `const void *img`: the buffer holding the data to the input image.
- `unsigned char *out_text`: the buffer holding the classification tag output
- `unsigned char *out_imgname`: the name of the processed image, created as a
session resource (EXPERIMENTAL).
- `size_t len_img`: the size of `img` in bytes.
- `size_t len_out_text`: the size of `out_text` in bytes.
- `size_t len_out_imgname`: the size of `out_imagename` in bytes.
# Build

## Install pre-built PyTorch C/C++ API files (LibTorch)

PyTorch provides pre-built binaries for LibTorch. Ie. for version 2.5.1:

Download and extract CPU-only binaries:
```shell
wget https://download.pytorch.org/libtorch/cpu/libtorch-cxx11-abi-shared-with-deps-2.5.1%2Bcpu.zip
unzip libtorch-cxx11-abi-shared-with-deps-2.5.1+cpu.zip
```

or download and extract binaries with CUDA support (here for CUDA 11.8):
```shell
wget https://download.pytorch.org/libtorch/cu118/libtorch-cxx11-abi-shared-with-deps-2.5.1%2Bcu118.zip
unzip libtorch-cxx11-abi-shared-with-deps-2.5.1+cu118.zip
```

and move files to the desired installation directory:
```shell
sudo mv libtorch /opt/torch
```

## Install vAccel

Information about vAccel installation can be found [here](https://docs.vaccel.org/quickstart/).

## Build the plugin

Get the plugin:
```bash
git clone --recursive git@github.com:nubificus/vaccel-plugin-torch
cd vaccel-plugin-torch
```

LibTorch does not provide a `.pc` file so discovery is done using the Meson
CMake module.

If LibTorch is installed in a non-standard path you will need to provide a CMake
prefix:
```bash
meson setup --cmake-prefix-path=/path/to/torch/installation build
```

else, a simple:
```bash
meson setup build
```
should correctly detect the required dependencies.

### Enable CUDA support

To build with CUDA support you will probably need to add the CUDA installation
path to the CMake prefix:
```bash
meson setup \
    --cmake-prefix-path='/path/to/torch/installation;/path/to/cuda/installation' \
    build
```

Additionally, setting the environment variables `CMAKE_CUDA_ARCHITECTURE` and
`CMAKE_CUDA_COMPILER` might be required to correctly detect the default CUDA
architecture:
```bash
export CMAKE_CUDA_ARCHITECTURE=<version>
export CMAKE_CUDA_COMPILER=/path/to/cuda/installation/bin/nvcc

meson setup \
    --cmake-prefix-path='/path/to/torch/installation;/path/to/cuda/installation' \
    build
```

To finally build the plugin:
```bash
meson compile -C build
```

## Example workflow
After having installed vAccel and its corresponding prerequisites
```bash
wget https://download.pytorch.org/libtorch/nightly/cpu/libtorch-shared-with-deps-latest.zip
unzip libtorch-shared-with-deps-latest.zip 
rm libtorch-shared-with-deps-latest.zip 
sudo mv libtorch/ /opt/torch

git clone git@github.com:nubificus/vaccel-plugin-torch
cd vaccel-plugin-torch/
meson setup --cmake-prefix-path=/opt/torch build
meson compile -C build
```

Afterwards, you can run the image classification example. First, define the vAccel plugin location:
```bash
export VACCEL_PLUGINS=build/src/libvaccel-torch.so
```
Define the log level:
```bash
export VACCEL_LOG_LEVEL=4
```
Get a ResNet model to use for image classification:
```bash
wget https://s3.nbfc.io/torch/resnet18.pt
```
And finally:
```shell
$ classify /usr/local/share/vaccel/images/example.jpg 1 resnet18.pt 
2025.03.17-17:24:17.28 - <debug> Initializing vAccel
2025.03.17-17:24:17.28 - <info> vAccel 0.6.1-191-f1337abd
2025.03.17-17:24:17.28 - <debug> Config:
2025.03.17-17:24:17.28 - <debug>   plugins = build/src/libvaccel-torch.so
2025.03.17-17:24:17.28 - <debug>   log_level = debug
2025.03.17-17:24:17.28 - <debug>   log_file = (null)
2025.03.17-17:24:17.28 - <debug>   profiling_enabled = false
2025.03.17-17:24:17.28 - <debug>   version_ignore = false
2025.03.17-17:24:17.28 - <debug> Created top-level rundir: /run/user/1006/vaccel/WeXJY4
2025.03.17-17:24:18.06 - <warn> Plugin may be incompatible with current vAccel version (built w/ 0.6.1-182-262677eb, used w/ 0.6.1-191-f1337abd)
2025.03.17-17:24:18.06 - <info> Registered plugin torch 0.1.0-22-7cf3d0e4
2025.03.17-17:24:18.06 - <debug> Registered op torch_jitload_forward from plugin torch
2025.03.17-17:24:18.06 - <debug> Registered op torch_sgemm from plugin torch
2025.03.17-17:24:18.06 - <debug> Registered op image_classify from plugin torch
2025.03.17-17:24:18.06 - <debug> Loaded plugin torch from build/src/libvaccel-torch.so
2025.03.17-17:24:18.06 - <debug> New rundir for session 1: /run/user/1006/vaccel/WeXJY4/session.1
2025.03.17-17:24:18.06 - <debug> Initialized session 1
Initialized session with id: 1
2025.03.17-17:24:18.06 - <warn> Path does not seem to have a `<prefix>://`
2025.03.17-17:24:18.06 - <warn> Assuming resnet18.pt is a local path
2025.03.17-17:24:18.06 - <debug> Initialized resource 1
2025.03.17-17:24:18.06 - <debug> New rundir for resource 1: /run/user/1006/vaccel/WeXJY4/resource.1
2025.03.17-17:24:18.06 - <debug> session:1 Registered resource 1
2025.03.17-17:24:18.06 - <debug> session:1 Looking for plugin implementing VACCEL_OP_IMAGE_CLASSIFY
2025.03.17-17:24:18.06 - <debug> Returning func from hint plugin torch 
2025.03.17-17:24:18.06 - <debug> Found implementation in torch plugin
2025.03.17-17:24:18.51 - <debug> [torch] Model loaded successfully from: resnet18.pt
2025.03.17-17:24:18.77 - <debug> [torch] Prediction: banana
classification tags: banana
classification imagename: PLACEHOLDER
2025.03.17-17:24:18.79 - <debug> session:1 Unregistered resource 1
2025.03.17-17:24:18.79 - <debug> Released resource 1
2025.03.17-17:24:18.79 - <debug> Released session 1
2025.03.17-17:24:18.97 - <debug> Cleaning up vAccel
2025.03.17-17:24:18.97 - <debug> Cleaning up sessions
2025.03.17-17:24:18.97 - <debug> Cleaning up resources
2025.03.17-17:24:18.97 - <debug> Cleaning up plugins
2025.03.17-17:24:18.97 - <debug> Unregistered plugin torch
```

Furthermore, you can also use the torch inference example, which uses the generic `jitload_forward` operation:

```shell
$ torch_inference /usr/local/share/vaccel/images/example.jpg resnet18.pt /usr/local/share/vaccel/labels/imagenet.txt
2025.03.17-18:19:59.55 - <debug> Initializing vAccel
2025.03.17-18:19:59.55 - <info> vAccel 0.6.1-191-f1337abd
2025.03.17-18:19:59.55 - <debug> Config:
2025.03.17-18:19:59.55 - <debug>   plugins = build/src/libvaccel-torch.so
2025.03.17-18:19:59.55 - <debug>   log_level = debug
2025.03.17-18:19:59.55 - <debug>   log_file = (null)
2025.03.17-18:19:59.55 - <debug>   profiling_enabled = false
2025.03.17-18:19:59.55 - <debug>   version_ignore = false
2025.03.17-18:19:59.55 - <debug> Created top-level rundir: /run/user/1006/vaccel/9nxdRQ
2025.03.17-18:20:00.18 - <warn> Plugin may be incompatible with current vAccel version (built w/ 0.6.1-182-262677eb, used w/ 0.6.1-191-f1337abd)
2025.03.17-18:20:00.18 - <info> Registered plugin torch 0.1.0-22-7cf3d0e4
2025.03.17-18:20:00.18 - <debug> Registered op torch_jitload_forward from plugin torch
2025.03.17-18:20:00.18 - <debug> Registered op torch_sgemm from plugin torch
2025.03.17-18:20:00.18 - <debug> Registered op image_classify from plugin torch
2025.03.17-18:20:00.18 - <debug> Loaded plugin torch from build/src/libvaccel-torch.so
2025.03.17-18:20:00.18 - <warn> Path does not seem to have a `<prefix>://`
2025.03.17-18:20:00.18 - <warn> Assuming resnet18.pt is a local path
2025.03.17-18:20:00.18 - <debug> Initialized resource 1
Initialized model resource 1
2025.03.17-18:20:00.18 - <debug> New rundir for session 1: /run/user/1006/vaccel/9nxdRQ/session.1
2025.03.17-18:20:00.18 - <debug> Initialized session 1
Initialized vAccel session 1
2025.03.17-18:20:00.18 - <debug> New rundir for resource 1: /run/user/1006/vaccel/9nxdRQ/resource.1
2025.03.17-18:20:00.18 - <debug> session:1 Registered resource 1
2025.03.17-18:20:00.23 - <debug> session:1 Looking for plugin implementing torch_jitload_forward operation
2025.03.17-18:20:00.23 - <debug> Returning func from hint plugin torch 
2025.03.17-18:20:00.23 - <debug> Found implementation in torch plugin
2025.03.17-18:20:00.23 - <debug> [torch] session:1 Jitload & Forward Process
2025.03.17-18:20:00.23 - <debug> [torch] Model: resnet18.pt
2025.03.17-18:20:00.23 - <debug> [torch] CUDA not available, running in CPU mode
Success!
Result Tensor :
Output tensor => type:7 nr_dims:2
size: 4000 B
Prediction: banana
2025.03.17-18:20:00.59 - <debug> session:1 Unregistered resource 1
2025.03.17-18:20:00.59 - <debug> Released session 1
2025.03.17-18:20:00.59 - <debug> Released resource 1
2025.03.17-18:20:00.60 - <debug> Cleaning up vAccel
2025.03.17-18:20:00.60 - <debug> Cleaning up sessions
2025.03.17-18:20:00.60 - <debug> Cleaning up resources
2025.03.17-18:20:00.60 - <debug> Cleaning up plugins
2025.03.17-18:20:00.60 - <debug> Unregistered plugin torch
```
