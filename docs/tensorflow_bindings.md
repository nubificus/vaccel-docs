# vAccel Tensorflow Bindings

To execute TF applications using vAccel, The first thing we need to do is
install tensorflow on the machine we plan to run the plugin. This is a lengthy
operation, as we need the C/C++ libraries which are not available from the
official tensorflow repo as binaries. To build from source, follow the guide below.

Alternatively you can use a container image we have already built, so feel free
to skip to [Running in a container](#running-in-a-container).

### Get & Build the TF C/C++ API files

Building the TF libraries can be a lengthy process. For instance, on a 4-core
machine with 16GB of memory the command below took ~2.5h.

```sh
git clone https://github.com/tensorflow/tensorflow.git && \
    cd tensorflow && \
    git checkout v2.11.0 && \
    ./configure && \
    bazel build --jobs=4 \
            --config=v2 \
            --copt=-O3 \
            --copt=-march=native \
            --config=opt \
            --verbose_failures \
            //tensorflow:tensorflow_cc \
            //tensorflow:install_headers \
            //tensorflow:tensorflow \
            //tensorflow:tensorflow_framework \
            //tensorflow/c:c_api \
            //tensorflow/tools/lib_package:libtensorflow
```

install TF runtime & libs to some dir in the host:

```sh
mkdir -p /opt/tensorflow/lib
cp -r bazel-bin/tensorflow/* /opt/tensorflow/lib/
cd /opt/tensorflow/lib && \
     ln -s libtensorflow_cc.so.2.6.0 libtensorflow_cc.so && \
     ln -s libtensorflow_cc.so.2.6.0 libtensorflow_cc.so.2 && \
     ln -s libtensorflow.so.2.6.0 libtensorflow.so && \
     ln -s libtensorflow.so.2.6.0 libtensorflow.so.2
LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
LD_LIBRARY_PATH=/opt/tensorflow/lib:$LD_LIBRARY_PATH
ldconfig
```

### Running in a container

If you want to avoid the burden (effort & time) to build the TF C/C++ libraries
from source, you can use a ready-made container image. Just run:

```sh
docker run --rm -it -v$PWD:/data -w /data harbor.nbfc.io/nubificus/tensorflow-base-generic:latest /bin/bash
```

and perform the steps below inside the container.

### Install vAccel on the host

```sh
wget https://s3.nbfc.io/nbfc-assets/github/vaccelrt/main/x86_64/Release-deb/vaccel-0.6.0-Linux.deb
sudo dpkg -i vaccel-0.6.0-Linux.deb
```

### Get the Tensorflow plugin & bindings

```sh
wget https://s3.nbfc.io/nbfc-assets/github/vaccelrt/plugins/tensorflow/main/x86_64/Release-deb/vaccel-tensorflow-0.1.0-Linux.deb
dpkg -i vaccel-tensorflow-0.1.0-Linux.deb
```

There should be two `.so` files installed in `/usr/local/lib`:

```
$ find /usr/local/lib -name "libvaccel-tf*.so"
libvaccel-tf-bindings.so
libvaccel-tf.so
```

Alternatively, get the binary artifacts manually from the [binaries](user-guide/binaries.md#binaries) table and install them to /usr/local/lib:

```
wget https://s3.nbfc.io/nbfc-assets/github/vaccelrt/plugins/tensorflow/main/x86_64/Release/libvaccel-tf.so
wget https://s3.nubificus.co.uk/nbfc-assets/github/vaccelrt/plugins/tensorflow/main/x86_64/Release/libvaccel-tf-bindings.so
cp libvaccel-tf-bindings.so /usr/local//lib
cp libvaccel-tf.so /usr/local/lib
```

#### Run a simple vAccel test (vAccel TF API)

To test the vAccel TF API we'll need a TF model. You can get a dir with the
necessary files from our s3 repo:

```sh
wget https://s3.nbfc.io/tensorflow/lstm2.tar.gz
tar -zxvf lstm2.tar.gz --strip-components=1
```

Then, after setting the parameters below,

```sh
export VACCEL_DEBUG_LEVEL=4
export LD_LIBRARY_PATH=/usr/local/lib
export VACCEL_BACKENDS=/usr/local/lib/libvaccel-tf.so
```

we can run the three examples:

`tf_model` (just loads a pb model)

```console
$ /usr/local/bin/tf_model lstm2/saved_model.pb 
2023.01.30-14:49:24.05 - <debug> Initializing vAccel
2023.01.30-14:49:24.05 - <debug> Created top-level rundir: /run/user/0/vaccel.XkutVJ
2023.01.30-14:49:24.10 - <debug> Registered plugin tf
2023.01.30-14:49:24.10 - <debug> Registered function TensorFlow session load from plugin tf
2023.01.30-14:49:24.10 - <debug> Registered function TensorFlow session run from plugin tf
2023.01.30-14:49:24.10 - <debug> Registered function TensorFlow session delete from plugin tf
2023.01.30-14:49:24.10 - <debug> Loaded plugin tf from /usr/local/lib/libvaccel-tf.so
2023.01.30-14:49:24.10 - <debug> session:1 New session
2023.01.30-14:49:24.10 - <debug> New rundir for resource /run/user/0/vaccel.XkutVJ/resource.2
2023.01.30-14:49:24.10 - <debug> Persisting file
2023.01.30-14:49:24.10 - <debug> Destroying resource 1
2023.01.30-14:49:24.10 - <debug> Destroying resource 2
2023.01.30-14:49:24.10 - <debug> Removing file /run/user/0/vaccel.XkutVJ/resource.2/model.pb
2023.01.30-14:49:24.10 - <debug> session:1 Free session
2023.01.30-14:49:24.10 - <debug> Shutting down vAccel
2023.01.30-14:49:24.10 - <debug> Cleaning up plugins
2023.01.30-14:49:24.10 - <debug> Unregistered plugin tf
```

`tf_saved_model` (loads a saved model)

```
$ /usr/local/bin/tf_saved_model lstm2 
2023.01.30-14:50:10.65 - <debug> Initializing vAccel
2023.01.30-14:50:10.65 - <debug> Created top-level rundir: /run/user/0/vaccel.eAMXnP
2023.01.30-14:50:10.71 - <debug> Registered plugin tf
2023.01.30-14:50:10.71 - <debug> Registered function TensorFlow session load from plugin tf
2023.01.30-14:50:10.71 - <debug> Registered function TensorFlow session run from plugin tf
2023.01.30-14:50:10.71 - <debug> Registered function TensorFlow session delete from plugin tf
2023.01.30-14:50:10.71 - <debug> Loaded plugin tf from /usr/local/lib/libvaccel-tf.so
2023.01.30-14:50:10.71 - <info> Testing SavedModel handling from path
2023.01.30-14:50:10.71 - <info> Creating new SavedModel handle
2023.01.30-14:50:10.71 - <info> Setting path of the model
2023.01.30-14:50:10.71 - <debug> Set TensorFlow model path to lstm2
2023.01.30-14:50:10.71 - <info> Registering model resource with vAccel
2023.01.30-14:50:10.71 - <debug> Registering new vAccel TensorFlow model
2023.01.30-14:50:10.71 - <debug> New resource 1
2023.01.30-14:50:10.71 - <info> Registered new resource: 1
2023.01.30-14:50:10.71 - <debug> session:1 New session
2023.01.30-14:50:10.71 - <info> New session: 1
2023.01.30-14:50:10.71 - <info> Registering model 1 with session 1
2023.01.30-14:50:10.71 - <info> Unregistering model 1 from session 1
2023.01.30-14:50:10.71 - <info> Destroying model 1
2023.01.30-14:50:10.71 - <debug> Destroying resource 1
2023.01.30-14:50:10.71 - <info> Destroying session 1
2023.01.30-14:50:10.71 - <debug> session:1 Free session
2023.01.30-14:50:10.71 - <info> Testing SavedModel handling from in memory data
2023.01.30-14:50:10.71 - <info> Creating new SavedModel handle
2023.01.30-14:50:10.71 - <debug> Setting protobuf file for model
2023.01.30-14:50:10.71 - <debug> Setting checkpoint file for model
2023.01.30-14:50:10.71 - <debug> Setting variables index file for model
2023.01.30-14:50:10.71 - <info> Registering model resource with vAccel
2023.01.30-14:50:10.71 - <debug> Registering new vAccel TensorFlow model
2023.01.30-14:50:10.71 - <debug> Persisting file
2023.01.30-14:50:10.71 - <debug> Persisting file
2023.01.30-14:50:10.71 - <debug> Persisting file
2023.01.30-14:50:10.71 - <debug> New resource 1
2023.01.30-14:50:10.71 - <info> Registered new resource: 1
2023.01.30-14:50:10.71 - <debug> session:1 New session
2023.01.30-14:50:10.71 - <info> New session: 1
2023.01.30-14:50:10.71 - <info> Registering model 1 with session 1
2023.01.30-14:50:10.71 - <info> Unregistering model 1 from session 1
2023.01.30-14:50:10.71 - <info> Destroying model 1
2023.01.30-14:50:10.71 - <debug> Destroying resource 1
2023.01.30-14:50:10.71 - <debug> Removing file /run/user/0/vaccel.eAMXnP/resource.1/saved_model.pb
2023.01.30-14:50:10.71 - <debug> Removing file /run/user/0/vaccel.eAMXnP/resource.1/variables/variables.data-00000-of-00001
2023.01.30-14:50:10.71 - <debug> Removing file /run/user/0/vaccel.eAMXnP/resource.1/variables/variables.index
2023.01.30-14:50:10.71 - <info> Destroying session 1
2023.01.30-14:50:10.71 - <debug> session:1 Free session
2023.01.30-14:50:10.71 - <debug> Shutting down vAccel
2023.01.30-14:50:10.71 - <debug> Cleaning up plugins
2023.01.30-14:50:10.71 - <debug> Unregistered plugin tf
```

`tf_inference` (performs inference on a saved model)

```sh
$ /usr/local/bin/tf_inference lstm2 
2023.01.30-14:50:44.04 - <debug> Initializing vAccel
2023.01.30-14:50:44.04 - <debug> Created top-level rundir: /run/user/0/vaccel.3qjD7J
2023.01.30-14:50:44.09 - <debug> Registered plugin tf
2023.01.30-14:50:44.09 - <debug> Registered function TensorFlow session load from plugin tf
2023.01.30-14:50:44.09 - <debug> Registered function TensorFlow session run from plugin tf
2023.01.30-14:50:44.09 - <debug> Registered function TensorFlow session delete from plugin tf
2023.01.30-14:50:44.09 - <debug> Loaded plugin tf from /usr/local/lib/libvaccel-tf.so
2023.01.30-14:50:44.09 - <debug> Set TensorFlow model path to lstm2
2023.01.30-14:50:44.09 - <debug> Registering new vAccel TensorFlow model
2023.01.30-14:50:44.09 - <debug> New resource 1
Created new model 1
2023.01.30-14:50:44.09 - <debug> session:1 New session
Initialized vAccel session 1
2023.01.30-14:50:44.09 - <debug> TensorFlow: load graph
2023.01.30-14:50:44.09 - <debug> Found implementation in tf plugin
2023.01.30-14:50:44.09 - <debug> [tf-plugin] Loading session from SavedModel
2023-01-30 14:50:44.108279: I tensorflow/cc/saved_model/reader.cc:45] Reading SavedModel from: lstm2
2023-01-30 14:50:44.159135: I tensorflow/cc/saved_model/reader.cc:89] Reading meta graph with tags { serve }
2023-01-30 14:50:44.159176: I tensorflow/cc/saved_model/reader.cc:130] Reading SavedModel debug info (if present) from: lstm2
2023-01-30 14:50:44.263678: I tensorflow/compiler/mlir/mlir_graph_optimization_pass.cc:357] MLIR V1 optimization pass is not enabled
2023-01-30 14:50:44.296034: I tensorflow/cc/saved_model/loader.cc:229] Restoring SavedModel bundle.
2023-01-30 14:50:44.459965: I tensorflow/cc/saved_model/loader.cc:213] Running initialization op on SavedModel bundle at path: lstm2
2023-01-30 14:50:44.605060: I tensorflow/cc/saved_model/loader.cc:305] SavedModel load for tags { serve }; Status: success: OK. Took 496802 microseconds.
2023.01.30-14:50:44.64 - <debug> Model from path loaded correctly
2023.01.30-14:50:44.72 - <debug> TensorFlow: run graph
2023.01.30-14:50:44.72 - <debug> Found implementation in tf plugin
2023.01.30-14:50:44.72 - <debug> [tf-plugin] Running session
2023.01.30-14:50:45.28 - <debug> [tf-plugin] Success
Success!
Output tensor => type:1 nr_dims:3
dim[0]: 1
dim[1]: 30
dim[2]: 61
Result Tensor :
0.016192
0.016538
0.016211
0.016086
0.016314
0.016367
0.016475
0.016484
0.016668
0.016283
2023.01.30-14:50:45.28 - <debug> TensorFlow: delete session
2023.01.30-14:50:45.28 - <debug> Found implementation in tf plugin
2023.01.30-14:50:45.37 - <debug> session:1 Free session
2023.01.30-14:50:45.37 - <debug> Destroying resource 1
2023.01.30-14:50:45.37 - <debug> Shutting down vAccel
2023.01.30-14:50:45.37 - <debug> Cleaning up plugins
2023.01.30-14:50:45.37 - <debug> Unregistered plugin tf
```

### Build a tensorflow example application

```sh
git clone https://github.com/AmirulOm/tensorflow_capi_sample
cd tensorflow_capi_sample
gcc -I/opt/tensorflow/lib/include/ -L/opt/tensorflow/lib main.c -ltensorflow -o main.out
```
Make sure the [saved model](https://s3.nbfc.io/tensorflow/lstm2.tar.gz) is present:

```sh
wget https://s3.nbfc.io/tensorflow/lstm2.tar.gz
tar -zxvf lstm2.tar.gz --strip-components=1
```

and after we set the LD_LIBRARY_PATH parameter:

```sh
export LD_LIBRARY_PATH=/opt/tensorflow/lib:$LD_LIBRARY_PATH
```

we can run:

```
$ ./main.out
2022-08-04 18:03:52.615232: I tensorflow/cc/saved_model/reader.cc:38] Reading SavedModel from: lstm2/
2022-08-04 18:03:52.668118: I tensorflow/cc/saved_model/reader.cc:90] Reading meta graph with tags { serve }
2022-08-04 18:03:52.668163: I tensorflow/cc/saved_model/reader.cc:132] Reading SavedModel debug info (if present) from: lstm2/
2022-08-04 18:03:52.884637: I tensorflow/cc/saved_model/loader.cc:211] Restoring SavedModel bundle.
2022-08-04 18:03:53.092219: I tensorflow/cc/saved_model/loader.cc:195] Running initialization op on SavedModel bundle at path: lstm2/
2022-08-04 18:03:53.240309: I tensorflow/cc/saved_model/loader.cc:283] SavedModel load for tags { serve }; Status: success: OK. Took 625082 microseconds.
TF_LoadSessionFromSavedModel OK
TF_GraphOperationByName serving_default_input_1 is OK
TF_GraphOperationByName StatefulPartitionedCall is OK
TF_NewTensor is OK
Session is OK
Result Tensor :
0.016192
0.016538
0.016211
0.016086
0.016314
0.016367
0.016475
0.016484
0.016668
0.016283
```

This is a generic TF execution example. To run with vAccel, apart from the
above env parameters, we'll need to specify the bindings:

```sh
$ LD_PRELOAD=/usr/local/lib/libvaccel-tf-bindings.so ./main.out 
2023.01.30-14:54:38.23 - <debug> Initializing vAccel
2023.01.30-14:54:38.23 - <debug> Created top-level rundir: /run/user/0/vaccel.Ldk8YE
2023.01.30-14:54:38.25 - <debug> Registered plugin tf
2023.01.30-14:54:38.25 - <debug> Registered function TensorFlow session load from plugin tf
2023.01.30-14:54:38.25 - <debug> Registered function TensorFlow session run from plugin tf
2023.01.30-14:54:38.25 - <debug> Registered function TensorFlow session delete from plugin tf
2023.01.30-14:54:38.25 - <debug> Loaded plugin tf from /usr/local/lib/libvaccel-tf.so
2023.01.30-14:54:38.27 - <debug> session:1 New session
2023.01.30-14:54:38.27 - <debug> Set TensorFlow model path to lstm2/
2023.01.30-14:54:38.27 - <debug> Registering new vAccel TensorFlow model
2023.01.30-14:54:38.27 - <debug> New resource 1
2023.01.30-14:54:38.27 - <debug> TensorFlow: load graph
2023.01.30-14:54:38.27 - <debug> Found implementation in tf plugin
2023.01.30-14:54:38.27 - <debug> [tf-plugin] Loading session from SavedModel
2023-01-30 14:54:38.273960: I tensorflow/cc/saved_model/reader.cc:45] Reading SavedModel from: lstm2/
2023-01-30 14:54:38.313844: I tensorflow/cc/saved_model/reader.cc:89] Reading meta graph with tags { serve }
2023-01-30 14:54:38.313888: I tensorflow/cc/saved_model/reader.cc:130] Reading SavedModel debug info (if present) from: lstm2/
2023-01-30 14:54:38.409655: I tensorflow/compiler/mlir/mlir_graph_optimization_pass.cc:357] MLIR V1 optimization pass is not enabled
2023-01-30 14:54:38.441268: I tensorflow/cc/saved_model/loader.cc:229] Restoring SavedModel bundle.
2023-01-30 14:54:38.628391: I tensorflow/cc/saved_model/loader.cc:213] Running initialization op on SavedModel bundle at path: lstm2/
2023-01-30 14:54:38.763201: I tensorflow/cc/saved_model/loader.cc:305] SavedModel load for tags { serve }; Status: success: OK. Took 489261 microseconds.
2023.01.30-14:54:38.80 - <debug> Model from path loaded correctly
2023-01-30 14:54:38.870546: I tensorflow/cc/saved_model/reader.cc:45] Reading SavedModel from: lstm2/
2023-01-30 14:54:38.918771: I tensorflow/cc/saved_model/reader.cc:89] Reading meta graph with tags { serve }
2023-01-30 14:54:38.918819: I tensorflow/cc/saved_model/reader.cc:130] Reading SavedModel debug info (if present) from: lstm2/
2023-01-30 14:54:39.050492: I tensorflow/cc/saved_model/loader.cc:229] Restoring SavedModel bundle.
2023-01-30 14:54:39.231115: I tensorflow/cc/saved_model/loader.cc:213] Running initialization op on SavedModel bundle at path: lstm2/
2023-01-30 14:54:39.379673: I tensorflow/cc/saved_model/loader.cc:305] SavedModel load for tags { serve }; Status: success: OK. Took 509137 microseconds.
TF_LoadSessionFromSavedModel OK
TF_GraphOperationByName serving_default_input_1 is OK
TF_GraphOperationByName StatefulPartitionedCall is OK
TF_NewTensor is OK
2023.01.30-14:54:39.41 - <debug> TensorFlow: run graph
2023.01.30-14:54:39.41 - <debug> Found implementation in tf plugin
2023.01.30-14:54:39.41 - <debug> [tf-plugin] Running session
2023.01.30-14:54:40.02 - <debug> [tf-plugin] Success
Session is OK
2023.01.30-14:54:40.02 - <debug> TensorFlow: delete session
2023.01.30-14:54:40.02 - <debug> Found implementation in tf plugin
2023.01.30-14:54:40.12 - <debug> Destroying resource 1
2023.01.30-14:54:40.19 - <debug> session:1 Free session
Result Tensor :
0.016192
0.016538
0.016211
0.016086
0.016314
0.016367
0.016475
0.016484
0.016668
0.016283
2023.01.30-14:54:40.19 - <debug> Shutting down vAccel
2023.01.30-14:54:40.19 - <debug> Cleaning up plugins
2023.01.30-14:54:40.19 - <debug> Unregistered plugin tf
```
