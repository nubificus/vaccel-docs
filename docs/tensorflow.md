# Tensorflow

## 
### Get & Build the TF C/C++ API files

```
git clone https://github.com/tensorflow/tensorflow.git && \
    cd tensorflow && \
    git checkout v2.6.0 && \
    ./configure && \
    bazel build --jobs=8 \
            --config=v2 \
            --copt=-O3 \
            --copt=-m64 \
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

```
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

also, we are missing a couple of header files:

```
wget https://raw.githubusercontent.com/tensorflow/tensorflow/master/tensorflow/c/c_api_internal.h \
     -O /opt/tensorflow/lib/include/tensorflow/c/c_api_internal.h
wget https://raw.githubusercontent.com/tensorflow/tensorflow/master/tensorflow/core/framework/op_gen_lib.h \
     -O /opt/tensorflow/lib/include/tensorflow/core/framework/op_gen_lib.h
```


### Install vAccel on the host

```
$ mkdir -p /opt/vaccel
$ wget https://github.com/cloudkernels/vaccel/releases/download/v0.4.0/vaccel_x86_64_Release.tar.gz
$ sudo tar -zxvf vaccel_x86_64_Release.tar.gz -C /opt/vaccel
```

### Build from source

```
$ git clone git@github.com:nubificus/vaccelrt-plugin-tensorflow
$ cd vaccel-plugin-tensorflow
$ mkdir build
$ cd build
$ cmake ../
$ make
```

There should be two `.so` files produced:

```
$ find ./ -name "*.so"
./bindings/libvaccel-tf-bindings.so
./plugin/libvaccel-tf.so
```

Install those to /usr/local/lib:

```
cp ./bindings/libvaccel-tf-bindings.so /usr/local//lib
cp ./plugin/libvaccel-tf.so /usr/local/lib
```

#### Run a simple vAccel test (vAccel TF API)

To test the vAccel TF API we'll need a TF model. You can get a dir with the necessary files from our s3 repo:

```
$ wget https://s3.nbfc.io/tensorflow/lstm2.tar.gz
$ tar -zxvf lstm2.tar.gz
```

Then we can run the three examples:

`tf_model` (just loads a pb model)

```
$ VACCEL_DEBUG_LEVEL=4 VACCEL_BACKENDS=plugin/libvaccel-tf.so LD_LIBRARY_PATH=/opt/vaccel/lib \
    /opt/vaccel/bin/tf_model ./lstm2/saved_model.pb
2022.08.04-18:09:01.83 - <debug> Initializing vAccel
2022.08.04-18:09:01.89 - <debug> Registered plugin tf
2022.08.04-18:09:01.89 - <debug> Registered function TensorFlow session load from plugin tf
2022.08.04-18:09:01.89 - <debug> Registered function TensorFlow session run from plugin tf
2022.08.04-18:09:01.89 - <debug> Registered function TensorFlow session delete from plugin tf
2022.08.04-18:09:01.89 - <debug> Loaded plugin tf from plugin/libvaccel-tf.so
2022.08.04-18:09:01.89 - <debug> session:1 New session
2022.08.04-18:09:01.90 - <debug> New rundir for resource /run/user/0/vaccel.RtlLS1/resource.2
2022.08.04-18:09:01.90 - <debug> Persisting file
2022.08.04-18:09:01.90 - <debug> Destroying resource 1
2022.08.04-18:09:01.90 - <debug> Destroying resource 2
2022.08.04-18:09:01.90 - <debug> Removing file /run/user/0/vaccel.RtlLS1/resource.2/model.pb
2022.08.04-18:09:01.90 - <debug> session:1 Free session
2022.08.04-18:09:01.90 - <debug> Shutting down vAccel
2022.08.04-18:09:01.90 - <debug> Cleaning up plugins
2022.08.04-18:09:01.90 - <debug> Unregistered plugin tf
```

`tf_saved_model` (loads a saved model)

```
$ VACCEL_DEBUG_LEVEL=4 VACCEL_BACKENDS=plugin/libvaccel-tf.so LD_LIBRARY_PATH=/opt/vaccel/lib \
    /opt/vaccel/bin/tf_saved_model ./lstm2/
2022.08.04-18:09:16.87 - <debug> Initializing vAccel
2022.08.04-18:09:16.95 - <debug> Registered plugin tf
2022.08.04-18:09:16.95 - <debug> Registered function TensorFlow session load from plugin tf
2022.08.04-18:09:16.95 - <debug> Registered function TensorFlow session run from plugin tf
2022.08.04-18:09:16.95 - <debug> Registered function TensorFlow session delete from plugin tf
2022.08.04-18:09:16.95 - <debug> Loaded plugin tf from plugin/libvaccel-tf.so
2022.08.04-18:09:16.95 - <info> Testing SavedModel handling from path
2022.08.04-18:09:16.95 - <info> Creating new SavedModel handle
2022.08.04-18:09:16.95 - <info> Setting path of the model
2022.08.04-18:09:16.96 - <debug> Set TensorFlow model path to ./lstm2/
2022.08.04-18:09:16.96 - <info> Registering model resource with vAccel
2022.08.04-18:09:16.96 - <debug> Registering new vAccel TensorFlow model
2022.08.04-18:09:16.96 - <debug> New resource 1
2022.08.04-18:09:16.96 - <info> Registered new resource: 1
2022.08.04-18:09:16.96 - <debug> session:1 New session
2022.08.04-18:09:16.96 - <info> New session: 1
2022.08.04-18:09:16.96 - <info> Registering model 1 with session 1
2022.08.04-18:09:16.96 - <info> Unregistering model 1 from session 1
2022.08.04-18:09:16.96 - <info> Destroying model 1
2022.08.04-18:09:16.96 - <debug> Destroying resource 1
2022.08.04-18:09:16.96 - <info> Destroying session 1
2022.08.04-18:09:16.96 - <debug> session:1 Free session
2022.08.04-18:09:16.96 - <info> Testing SavedModel handling from in memory data
2022.08.04-18:09:16.96 - <info> Creating new SavedModel handle
2022.08.04-18:09:16.96 - <debug> Setting protobuf file for model
2022.08.04-18:09:16.96 - <debug> Setting checkpoint file for model
2022.08.04-18:09:16.96 - <debug> Setting variables index file for model
2022.08.04-18:09:16.96 - <info> Registering model resource with vAccel
2022.08.04-18:09:16.96 - <debug> Registering new vAccel TensorFlow model
2022.08.04-18:09:16.96 - <debug> Persisting file
2022.08.04-18:09:16.96 - <debug> Persisting file
2022.08.04-18:09:16.96 - <debug> Persisting file
2022.08.04-18:09:16.96 - <debug> New resource 1
2022.08.04-18:09:16.96 - <info> Registered new resource: 1
2022.08.04-18:09:16.96 - <debug> session:1 New session
2022.08.04-18:09:16.96 - <info> New session: 1
2022.08.04-18:09:16.96 - <info> Registering model 1 with session 1
2022.08.04-18:09:16.96 - <info> Unregistering model 1 from session 1
2022.08.04-18:09:16.96 - <info> Destroying model 1
2022.08.04-18:09:16.96 - <debug> Destroying resource 1
2022.08.04-18:09:16.96 - <debug> Removing file /run/user/0/vaccel.aHVcx4/resource.1/saved_model.pb
2022.08.04-18:09:16.96 - <debug> Removing file /run/user/0/vaccel.aHVcx4/resource.1/variables/variables.data-00000-of-00001
2022.08.04-18:09:16.96 - <debug> Removing file /run/user/0/vaccel.aHVcx4/resource.1/variables/variables.index
2022.08.04-18:09:16.96 - <info> Destroying session 1
2022.08.04-18:09:16.96 - <debug> session:1 Free session
2022.08.04-18:09:16.96 - <debug> Shutting down vAccel
2022.08.04-18:09:16.96 - <debug> Cleaning up plugins
2022.08.04-18:09:16.96 - <debug> Unregistered plugin tf
```

`tf_inference` (performs inference on a saved model)

```
$ VACCEL_DEBUG_LEVEL=4 VACCEL_BACKENDS=plugin/libvaccel-tf.so LD_LIBRARY_PATH=/opt/vaccel/lib \ 
    /opt/vaccel/bin/tf_inference ./lstm2/
2022.08.04-18:09:23.16 - <debug> Initializing vAccel
2022.08.04-18:09:23.22 - <debug> Registered plugin tf
2022.08.04-18:09:23.22 - <debug> Registered function TensorFlow session load from plugin tf
2022.08.04-18:09:23.22 - <debug> Registered function TensorFlow session run from plugin tf
2022.08.04-18:09:23.22 - <debug> Registered function TensorFlow session delete from plugin tf
2022.08.04-18:09:23.22 - <debug> Loaded plugin tf from plugin/libvaccel-tf.so
2022.08.04-18:09:23.22 - <debug> Set TensorFlow model path to ./lstm2/
2022.08.04-18:09:23.22 - <debug> Registering new vAccel TensorFlow model
2022.08.04-18:09:23.22 - <debug> New resource 1
Created new model 1
2022.08.04-18:09:23.22 - <debug> session:1 New session
Initialized vAccel session 1
2022.08.04-18:09:23.22 - <debug> TensorFlow: load graph
2022.08.04-18:09:23.22 - <debug> Found implementation in tf plugin
2022.08.04-18:09:23.22 - <debug> [tf-plugin] Loading session from SavedModel
2022-08-04 18:09:23.238961: I tensorflow/cc/saved_model/reader.cc:38] Reading SavedModel from: ./lstm2/
2022-08-04 18:09:23.289905: I tensorflow/cc/saved_model/reader.cc:90] Reading meta graph with tags { serve }
2022-08-04 18:09:23.289948: I tensorflow/cc/saved_model/reader.cc:132] Reading SavedModel debug info (if present) from: ./lstm2/
2022-08-04 18:09:23.506149: I tensorflow/cc/saved_model/loader.cc:211] Restoring SavedModel bundle.
2022-08-04 18:09:23.705592: I tensorflow/cc/saved_model/loader.cc:195] Running initialization op on SavedModel bundle at path: ./lstm2/
2022-08-04 18:09:23.852835: I tensorflow/cc/saved_model/loader.cc:283] SavedModel load for tags { serve }; Status: success: OK. Took 613876 microseconds.
2022.08.04-18:09:23.90 - <debug> Model from path loaded correctly
2022.08.04-18:09:23.99 - <debug> TensorFlow: run graph
2022.08.04-18:09:23.99 - <debug> Found implementation in tf plugin
2022.08.04-18:09:23.99 - <debug> [tf-plugin] Running session
2022.08.04-18:09:24.67 - <debug> [tf-plugin] Success
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
2022.08.04-18:09:24.67 - <debug> TensorFlow: delete session
2022.08.04-18:09:24.67 - <debug> Found implementation in tf plugin
2022.08.04-18:09:24.80 - <debug> session:1 Free session
2022.08.04-18:09:24.80 - <debug> Destroying resource 1
2022.08.04-18:09:24.80 - <debug> Shutting down vAccel
2022.08.04-18:09:24.80 - <debug> Cleaning up plugins
2022.08.04-18:09:24.80 - <debug> Unregistered plugin tf
```

### Build a tensorflow example application

```
$ git clone https://github.com/AmirulOm/tensorflow_capi_sample
$ cd tensorflow_capi_sample
$ gcc -I/opt/tensorflow/lib/include/ -L/opt/tensorflow/lib main.c -ltensorflow -o main.out
```
Make sure the [saved model](https://s3.nbfc.io/tensorflow/lstm2.tar.gz) is present:
```
$ wget https://s3.nbfc.io/tensorflow/lstm2.tar.gz
$ tar -zxvf lstm2.tar.gz 
```
and run:
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

This is a generic TF execution example. To run with vAccel, we'll need to specify the plugin and the bindings:

```
$ VACCEL_DEBUG_LEVEL=4 VACCEL_BACKENDS=/opt/vaccel/lib/libvaccel-tf.so \
    LD_LIBRARY_PATH=/opt/vaccel/lib:/opt/tensorflow/lib \
	LD_PRELOAD=/opt/vaccel/lib/libvaccel-tf-bindings.so ./main.out
2022.08.04-18:07:23.00 - <debug> Initializing vAccel
2022.08.04-18:07:24.03 - <debug> Registered plugin tf
2022.08.04-18:07:24.03 - <debug> Registered function TensorFlow session load from plugin tf
2022.08.04-18:07:24.03 - <debug> Registered function TensorFlow session run from plugin tf
2022.08.04-18:07:24.03 - <debug> Registered function TensorFlow session delete from plugin tf
2022.08.04-18:07:24.03 - <debug> Loaded plugin tf from ../../vaccelrt-plugin-tensorflow/build/plugin/libvaccel-tf.so
2022.08.04-18:07:24.05 - <debug> session:1 New session
2022.08.04-18:07:24.05 - <debug> Set TensorFlow model path to lstm2/
2022.08.04-18:07:24.05 - <debug> Registering new vAccel TensorFlow model
2022.08.04-18:07:24.05 - <debug> New resource 1
2022.08.04-18:07:24.05 - <debug> TensorFlow: load graph
2022.08.04-18:07:24.05 - <debug> Found implementation in tf plugin
2022.08.04-18:07:24.05 - <debug> [tf-plugin] Loading session from SavedModel
2022-08-04 18:07:24.055445: I tensorflow/cc/saved_model/reader.cc:38] Reading SavedModel from: lstm2/
2022-08-04 18:07:24.106579: I tensorflow/cc/saved_model/reader.cc:90] Reading meta graph with tags { serve }
2022-08-04 18:07:24.106622: I tensorflow/cc/saved_model/reader.cc:132] Reading SavedModel debug info (if present) from: lstm2/
2022-08-04 18:07:24.319568: I tensorflow/cc/saved_model/loader.cc:211] Restoring SavedModel bundle.
2022-08-04 18:07:24.536920: I tensorflow/cc/saved_model/loader.cc:195] Running initialization op on SavedModel bundle at path: lstm2/
2022-08-04 18:07:24.690045: I tensorflow/cc/saved_model/loader.cc:283] SavedModel load for tags { serve }; Status: success: OK. Took 634603 microseconds.
2022.08.04-18:07:24.74 - <debug> Model from path loaded correctly
2022-08-04 18:07:24.836546: I tensorflow/cc/saved_model/reader.cc:38] Reading SavedModel from: lstm2/
2022-08-04 18:07:24.874934: I tensorflow/cc/saved_model/reader.cc:90] Reading meta graph with tags { serve }
2022-08-04 18:07:24.874973: I tensorflow/cc/saved_model/reader.cc:132] Reading SavedModel debug info (if present) from: lstm2/
2022-08-04 18:07:25.072489: I tensorflow/cc/saved_model/loader.cc:211] Restoring SavedModel bundle.
2022-08-04 18:07:25.271591: I tensorflow/cc/saved_model/loader.cc:195] Running initialization op on SavedModel bundle at path: lstm2/
2022-08-04 18:07:25.421925: I tensorflow/cc/saved_model/loader.cc:283] SavedModel load for tags { serve }; Status: success: OK. Took 585388 microseconds.
TF_LoadSessionFromSavedModel OK
TF_GraphOperationByName serving_default_input_1 is OK
TF_GraphOperationByName StatefulPartitionedCall is OK
TF_NewTensor is OK
2022.08.04-18:07:25.47 - <debug> TensorFlow: run graph
2022.08.04-18:07:25.47 - <debug> Found implementation in tf plugin
2022.08.04-18:07:25.47 - <debug> [tf-plugin] Running session
2022.08.04-18:07:26.13 - <debug> [tf-plugin] Success
Session is OK
2022.08.04-18:07:26.13 - <debug> TensorFlow: delete session
2022.08.04-18:07:26.13 - <debug> Found implementation in tf plugin
2022.08.04-18:07:26.26 - <debug> Destroying resource 1
2022.08.04-18:07:26.37 - <debug> session:1 Free session
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
2022.08.04-18:07:26.37 - <debug> Shutting down vAccel
2022.08.04-18:07:26.37 - <debug> Cleaning up plugins
2022.08.04-18:07:26.37 - <debug> Unregistered plugin tf
```
