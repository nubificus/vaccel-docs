# Build and Install Tensorflow

Official instructions for building and installing
[Tensorflow](https://www.tensorflow.org/) can be found on the Tensorflow
[Build from source](https://www.tensorflow.org/install/source) page.

In the sections below we provide a short version that can be used to build and
install Tensorflow and Tensorflow Lite C/C++ API files for use with vAccel. We
assume that the required package dependencies are already installed.

## Install Bazel

The easiest way to install the required [Bazel](https://bazel.build/) version is
to use [Bazelisk](https://github.com/bazelbuild/bazelisk). You can grab the
latest version from the Releases page.

Ie. for a Debian/Ubuntu-based system you can install Bazel 1.25.0 for x86_64
with:

```sh
wget https://github.com/bazelbuild/bazelisk/releases/download/v1.25.0/bazelisk-amd64.deb
sudo dpkg i bazelisk-amd64.deb
```

This will provide a `bazel` executable that will automatically detect and
install the required Bazel version for your Tensorflow build.

## Build and install Tensorflow and Tensorflow Lite C/C++ API files

Clone the Tensorflow repo, adjusting `TF_VERSION` to the desired version:

```sh
TF_VERSION=v2.17.0
git clone -b "${TF_VERSION}" --recursive --depth 1 \
        https://github.com/tensorflow/tensorflow.git
cd tensorflow
```

Build the Tensorflow and Tensorflow Lite source code:

```sh
./configure
bazel \
    --host_jvm_args=-Xmx2g \
    build --jobs=HOST_CPUS*.8 \
        --local_ram_resources=HOST_RAM*.4 \
        --config=v2 \
        --copt=-O3 \
        --verbose_failures \
        --discard_analysis_cache \
        -c opt \
        //tensorflow:libtensorflow.so \
        //tensorflow:libtensorflow_cc.so \
        //tensorflow:libtensorflow_framework.so \
        //tensorflow:install_headers \
        --config=monolithic \
        //tensorflow/lite/c:libtensorflowlite_c.so \
        //tensorflow/lite:libtensorflowlite.so \
        //tensorflow/lite/delegates/flex:tensorflowlite_flex
```

Note that the build process can take several hours to complete on a non-high-end
machine.

Copy TF Lite headers and install the generated files to `PREFIX`:

```sh
# Manually copy TF Lite headers (since no related bazel target is provided)
OUT_DIR=bazel-bin/tensorflow
rsync -aPm \
    --exclude='internal' --exclude='testing' --exclude='ios' \
    --exclude='python' --exclude='java' --exclude='objc' --exclude='swift' \
    --exclude='*internal*.h' --exclude='*test*.h' \
    --include='*/' --include='*.h' \
--exclude='*' \
    tensorflow/lite/* "${OUT_DIR}/include/tensorflow/lite"

# Install generated files
PREFIX=/usr/local
cp -r "${OUT_DIR}"/include "${PREFIX}/"
find "${OUT_DIR}" -path '*runfiles' -prune -o -name 'libtensorflow*.so*' \
    -exec cp -a {} "${PREFIX}/lib/" \;
rm -rf "${PREFIX}"/lib/*.params* "${PREFIX}"/lib/*.runfiles*
```
