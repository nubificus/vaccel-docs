# vAccel TVM Plugin

The TVM plugin implements the vAccel Image Classification operation:

### `VACCEL_OP_IMAGE_CLASSIFY`
the operation receives an image (in the form of bytes) and a TVM model (as a vAccel resource) and returns the classification label.
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

## Install TVM from source

```shell
sudo apt update && sudo apt install -y cmake git python3 python3-pip libtinfo-dev zlib1g-dev libedit-dev
# to support CUDA, you also need libllvm15 and libllvm15-dev

git clone --recursive https://github.com/apache/tvm.git
cd tvm
mkdir build
cd build
cmake .. -DCMAKE_BUILD_TYPE=Release -DUSE_LLVM=ON
# Add -DUSE_CUDA=ON to enable CUDA
cmake --build . --parallel $(nproc)
sudo cmake --install .

```
## Install vAccel

Information about vAccel installation can be found [here](https://docs.vaccel.org/quickstart/).

## Build the plugin

Get the plugin:
```shell
git clone --recursive git@github.com:nubificus/vaccel-plugin-tvm-inference
cd vaccel-plugin-tvm-inference
```

### CPU
For CPU, you can just use
```shell
meson setup build
meson compile -C build
```
to setup the build directory and build the plugin.

### CUDA
On the other side, building for CUDA, setting the environment variables `CMAKE_CUDA_ARCHITECTURE` and
`CMAKE_CUDA_COMPILER` might be required to correctly detect the default CUDA
architecture:
```bash
export CMAKE_CUDA_ARCHITECTURE=<version>
export CMAKE_CUDA_COMPILER=/path/to/cuda/installation/bin/nvcc

meson setup -Dcuda=true build
meson compile -C build
```

## Example workflow
After having installed vAccel and its corresponding prerequisites you can run the image classification example. First, define the vAccel plugin location:
```bash
export VACCEL_PLUGINS=build/src/libvaccel-tvm-inference.so
```
Define the log level:
```bash
export VACCEL_LOG_LEVEL=4
```
Get a ResNet model to use for image classification:
```bash
wget https://s3.nbfc.io/models/tvm/optimized/opt-resnet18-v2-7.so
```
And finally:
```shell
$ classify /usr/local/share/vaccel/images/example.jpg 1 /home/ilago/vaccel-plugin-tvm-inference/opt-resnet18-v2-7.so
2025.03.19-16:40:01.38 - <debug> Initializing vAccel
2025.03.19-16:40:01.38 - <info> vAccel 0.6.1-191-f1337abd
2025.03.19-16:40:01.38 - <debug> Config:
2025.03.19-16:40:01.38 - <debug>   plugins = build/src/libvaccel-tvm-inference.so
2025.03.19-16:40:01.38 - <debug>   log_level = debug
2025.03.19-16:40:01.38 - <debug>   log_file = (null)
2025.03.19-16:40:01.38 - <debug>   profiling_enabled = false
2025.03.19-16:40:01.38 - <debug>   version_ignore = false
2025.03.19-16:40:01.38 - <debug> Created top-level rundir: /run/user/1006/vaccel/7tiixK
2025.03.19-16:40:01.38 - <info> Registered plugin vAccel TVM Inference Plugin 0.0.0-7-88b51d19
2025.03.19-16:40:01.38 - <debug> Registered op image_classify from plugin vAccel TVM Inference Plugin
2025.03.19-16:40:01.38 - <debug> Loaded plugin vAccel TVM Inference Plugin from build/src/libvaccel-tvm-inference.so
2025.03.19-16:40:01.38 - <debug> New rundir for session 1: /run/user/1006/vaccel/7tiixK/session.1
2025.03.19-16:40:01.38 - <debug> Initialized session 1
Initialized session with id: 1
2025.03.19-16:40:01.38 - <warn> Path does not seem to have a `<prefix>://`
2025.03.19-16:40:01.38 - <warn> Assuming /home/ilago/vaccel-plugin-tvm-inference/opt-resnet18-v2-7.so is a local path
2025.03.19-16:40:01.38 - <debug> Initialized resource 1
2025.03.19-16:40:01.38 - <debug> New rundir for resource 1: /run/user/1006/vaccel/7tiixK/resource.1
2025.03.19-16:40:01.38 - <debug> session:1 Registered resource 1
2025.03.19-16:40:01.38 - <debug> session:1 Looking for plugin implementing VACCEL_OP_IMAGE_CLASSIFY
2025.03.19-16:40:01.38 - <debug> Returning func from hint plugin vAccel TVM Inference Plugin
2025.03.19-16:40:01.38 - <debug> Found implementation in vAccel TVM Inference Plugin plugin
Resource path: /home/ilago/vaccel-plugin-tvm-inference/opt-resnet18-v2-7.so
loading file: /home/ilago/vaccel-plugin-tvm-inference/opt-resnet18-v2-7.so
Result: banana
classification tags: banana
classification imagename: Empty
2025.03.19-16:40:01.51 - <debug> session:1 Unregistered resource 1
2025.03.19-16:40:01.51 - <debug> Released resource 1
2025.03.19-16:40:01.51 - <debug> Released session 1
2025.03.19-16:40:01.73 - <debug> Cleaning up vAccel
2025.03.19-16:40:01.73 - <debug> Cleaning up sessions
2025.03.19-16:40:01.73 - <debug> Cleaning up resources
2025.03.19-16:40:01.73 - <debug> Cleaning up plugins
2025.03.19-16:40:01.73 - <debug> Unregistered plugin vAccel TVM Inference Plugin
```

In case of non-linked TVM functions, try running setting the path of TVM runtime library shared object to `LD_PRELOAD` environment variable. Eg:
```shell
LD_PRELOAD=/path/to/libtvm_runtime.so classify /usr/local/share/vaccel/images/example.jpg 1 /home/ilago/vaccel-plugin-tvm-inference/opt-resnet18-v2-7.so
```
