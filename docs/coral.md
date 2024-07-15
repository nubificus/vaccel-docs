# Google Coral TPU

To build the vAccel Google Coral TPU plugin, we will use a simple image classification example based on `tflite`


To execute an image classification operation on the Google Coral TPU, we first
need to implement the operation using one of the available acceleration
frameworks and then register this function to the vAccel plugin we are
building. 

To achieve this, we patch a `tflite` example for Google coral, and
build the available image classification function as a shared library, exposing
the following API to the relevant plugin:

```c
int coral_classify(char *model_file_ptr,
                   char *label_file_ptr,
                   char *image_file_ptr,
                   float thres,
                   char **tags,
                   size_t *out_len) 
```

## Patch the code

The first step in order to build the library is to get the example code from
the Google Coral github repo:

```
git clone https://github.com/google-coral/tflite
```

Then we need to apply the following patch (`libify_classify.patch`) to the relevant example:

```patch
diff --git a/cpp/examples/classification/classify.cc b/cpp/examples/classification/classify.cc
index 69dfe04..1129976 100644
--- a/cpp/examples/classification/classify.cc
+++ b/cpp/examples/classification/classify.cc
@@ -22,6 +22,72 @@ int32_t ToInt32(const char p[4]) {
   return (p[3] << 24) | (p[2] << 16) | (p[1] << 8) | p[0];
 }
 
+std::vector<uint8_t> ReadBmpImageFromBuf(char* buf,
+                                  int* out_width = nullptr,
+                                  int* out_height = nullptr,
+                                  int* out_channels = nullptr) {
+  char header[kBmpHeaderSize];
+  memcpy(header, buf, sizeof(header));
+
+  const char* file_header = header;
+  const char* info_header = header + kBmpFileHeaderSize;
+  char *ptr = buf + sizeof(header);
+
+  if (file_header[0] != 'B' || file_header[1] != 'M')
+    return {};  // Invalid file type.
+
+  const int channels = info_header[14] / 8;
+  if (channels != 1 && channels != 3) return {};  // Unsupported bits per pixel.
+
+  if (ToInt32(&info_header[16]) != 0) return {};  // Unsupported compression.
+
+  uint32_t offset = ToInt32(&file_header[10]);
+#if 0
+  if (offset > kBmpHeaderSize)// && 
+      //!file.seekg(offset - kBmpHeaderSize, std::ios::cur))
+    return {};  // Seek failed.
+#endif
+
+  offset -= kBmpHeaderSize;
+  //printf("kBmpFileHeaderSize:%d\n", kBmpFileHeaderSize);
+  //printf("kBmpHeaderSize:%d\n", kBmpHeaderSize);
+  //printf("offset:%d\n", offset);
+  ptr = ptr+offset;
+  int width = ToInt32(&info_header[4]);
+  if (width < 0) return {};  // Invalid width.
+
+  int height = ToInt32(&info_header[8]);
+  const bool top_down = height < 0;
+  if (top_down) height = -height;
+
+  const int line_bytes = width * channels;
+  const int line_padding_bytes =
+      4 * ((8 * channels * width + 31) / 32) - line_bytes;
+  std::vector<uint8_t> image(line_bytes * height);
+  for (int i = 0; i < height; ++i) {
+    uint8_t* line = &image[(top_down ? i : (height - 1 - i)) * line_bytes];
+    memcpy(line, ptr, line_bytes);
+#if 0
+    if (!file.read(reinterpret_cast<char*>(line), line_bytes))
+      return {};  // Read failed.
+    if (!file.seekg(line_padding_bytes, std::ios::cur))
+      return {};  // Seek failed.
+#endif
+    //printf("line_bytes: %d line_padding_bytes:%d\n", line_bytes, line_padding_bytes);
+    ptr = ptr + line_padding_bytes;
+    ptr = ptr + line_bytes;
+    if (channels == 3) {
+      for (int j = 0; j < width; ++j) std::swap(line[3 * j], line[3 * j + 2]);
+    }
+  }
+
+  if (out_width) *out_width = width;
+  if (out_height) *out_height = height;
+  if (out_channels) *out_channels = channels;
+  return image;
+}
+
+
 std::vector<uint8_t> ReadBmpImage(const char* filename,
                                   int* out_width = nullptr,
                                   int* out_height = nullptr,
@@ -50,6 +116,9 @@ std::vector<uint8_t> ReadBmpImage(const char* filename,
       !file.seekg(offset - kBmpHeaderSize, std::ios::cur))
     return {};  // Seek failed.
 
+  printf("kBmpFileHeaderSize:%d\n", kBmpFileHeaderSize);
+  printf("kBmpHeaderSize:%d\n", kBmpHeaderSize);
+  printf("offset:%d\n", offset);
   int width = ToInt32(&info_header[4]);
   if (width < 0) return {};  // Invalid width.
 
@@ -63,6 +132,7 @@ std::vector<uint8_t> ReadBmpImage(const char* filename,
   std::vector<uint8_t> image(line_bytes * height);
   for (int i = 0; i < height; ++i) {
     uint8_t* line = &image[(top_down ? i : (height - 1 - i)) * line_bytes];
+    printf("line_bytes: %d line_padding_bytes:%d\n", line_bytes, line_padding_bytes);
     if (!file.read(reinterpret_cast<char*>(line), line_bytes))
       return {};  // Read failed.
     if (!file.seekg(line_padding_bytes, std::ios::cur))
@@ -117,18 +187,12 @@ std::vector<std::pair<int, float>> Sort(const std::vector<float>& scores,
 }
 }  // namespace
 
-int main(int argc, char* argv[]) {
-  if (argc != 5) {
-    std::cerr << argv[0]
-              << " <model_file> <label_file> <image_file> <threshold>"
-              << std::endl;
-    return 1;
-  }
-
-  const std::string model_file = argv[1];
-  const std::string label_file = argv[2];
-  const std::string image_file = argv[3];
-  const float threshold = std::stof(argv[4]);
+extern "C" int coral_classify(char *model_file_ptr, char *label_file_ptr, char *image_file_ptr, float thres, char **tags, size_t *out_len) 
+{
+  const std::string model_file (model_file_ptr);
+  const std::string label_file (label_file_ptr);
+  const std::string image_file (image_file_ptr);
+  const float threshold = thres;
 
   // Find TPU device.
   size_t num_devices;
@@ -151,7 +215,8 @@ int main(int argc, char* argv[]) {
   // Load image.
   int image_bpp, image_width, image_height;
   auto image =
-      ReadBmpImage(image_file.c_str(), &image_width, &image_height, &image_bpp);
+      ReadBmpImageFromBuf(image_file_ptr, &image_width, &image_height, &image_bpp);
+      //ReadBmpImage(image_file_ptr, &image_width, &image_height, &image_bpp);
   if (image.empty()) {
     std::cerr << "Cannot read image from " << image_file << std::endl;
     return 1;
@@ -174,7 +239,7 @@ int main(int argc, char* argv[]) {
 
   auto* delegate =
       edgetpu_create_delegate(device.type, device.path, nullptr, 0);
-  interpreter->ModifyGraphWithDelegate({delegate, edgetpu_free_delegate});
+  interpreter->ModifyGraphWithDelegate(delegate);
 
   // Allocate tensors.
   if (interpreter->AllocateTensors() != kTfLiteOk) {
@@ -204,9 +269,13 @@ int main(int argc, char* argv[]) {
 
   // Get interpreter output.
   auto results = Sort(Dequantize(*interpreter->output_tensor(0)), threshold);
+  *tags = strdup(GetLabel(labels, results[0].first).c_str());
+  *out_len = strlen(*tags);
+#if 0
   for (auto& result : results)
     std::cout << std::setw(7) << std::fixed << std::setprecision(5)
               << result.second << GetLabel(labels, result.first) << std::endl;
+#endif
 
   return 0;
 }
```

```
cd tflite
patch -p1 < ../libify_classify.path
```

Alternatively you could just clone from our forked repo:

```
git clone https://github.com/nubificus/tflite -b vaccel
```

Then, we need to install the requirements & build tflite for google coral (could take some time, so please be patient ;-)).

## Download the latest Edge TPU runtime

You can grab the latest Edge TPU runtime archive from
[https://coral.ai/software/](https://coral.ai/software/). Then extract it next
to the Makefile:

```
cd tflite/cpp/examples/classification/
wget https://dl.google.com/coral/edgetpu_api/edgetpu_runtime_20200710.zip
```

## Download and build Tensorflow

```
git clone https://github.com/tensorflow/tensorflow.git
tensorflow/tensorflow/lite/tools/make/download_dependencies.sh
tensorflow/tensorflow/lite/tools/make/build_lib.sh
```

## Build the shared library

Finally, build the classify shared object that we will then link to the vAccel Google Coral TPU plugin.

```sh
g++ -shared -fPIC -std=c++11 classify.cc
        -o /usr/local/lib/libclassify.so
        -I/data/tflite/cpp/examples/classification/edgetpu_runtime/libedgetpu/
        -Itensorflow/
        -Itensorflow//tensorflow/lite/tools/make/downloads/flatbuffers/include
        -Ltensorflow//tensorflow/lite/tools/make/gen/generic-aarch64_armv8-a/lib
        -Ledgetpu_runtime/libedgetpu/direct/aarch64/
        -l:libedgetpu.so.1.0 -lpthread -lm -ldl
        tensorflow/tensorflow/lite/tools/make/gen/linux_aarch64/lib/libtensorflow-lite.a
```

## Build vAccelRT plugin

Following the generic process for vAccelRT building (from [Building vAccelRT](/vaccelrt)) we now have to enable the vAccel Google Coral Edge TPU plugin.

In short, the previous steps for vAccelRT were the following[^1]:

```
git clone --recursive https://github.com/cloudkernels/vaccel -b feat_gcoral_plugin
cd vaccelrt
mkdir build
cd build
cmake ../
```

The additional step now is to enable the plugin via cmake:

```
cd vaccelrt
mkdir build_coral && cd build_coral
cmake ../ -DBUILD_PLUGIN_CORAL=ON
```

The output of the above command should be something like the following:

```
-- The C compiler identification is GNU 8.3.0
-- The CXX compiler identification is GNU 8.3.0
-- Check for working C compiler: /usr/bin/cc
-- Check for working C compiler: /usr/bin/cc -- works
-- Detecting C compiler ABI info
-- Detecting C compiler ABI info - done
-- Detecting C compile features
-- Detecting C compile features - done
-- Check for working CXX compiler: /usr/bin/c++
-- Check for working CXX compiler: /usr/bin/c++ -- works
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- Configuring done
-- Generating done
-- Build files have been written to: /data/vaccelrt/build_coral/googletest-download
Scanning dependencies of target googletest
[ 11%] Creating directories for 'googletest'
[ 22%] Performing download step (git clone) for 'googletest'
Cloning into 'googletest-src'...
Note: checking out 'release-1.8.1'.

You are in 'detached HEAD' state. You can look around, make experimental
changes and commit them, and you can discard any commits you make in this
state without impacting any branches by performing another checkout.

If you want to create a new branch to retain commits you create, you may
do so (now or later) by using -b with the checkout command again. Example:

  git checkout -b <new-branch-name>

HEAD is now at 2fe3bd99 Merge pull request #1433 from dsacre/fix-clang-warnings
[ 33%] No patch step for 'googletest'
[ 44%] Performing update step for 'googletest'
[ 55%] No configure step for 'googletest'
[ 66%] No build step for 'googletest'
[ 77%] No install step for 'googletest'
[ 88%] No test step for 'googletest'
[100%] Completed 'googletest'
[100%] Built target googletest
-- Found PythonInterp: /usr/bin/python (found version "2.7.16") 
-- Looking for pthread.h
-- Looking for pthread.h - found
-- Looking for pthread_create
-- Looking for pthread_create - not found
-- Check if compiler accepts -pthread
-- Check if compiler accepts -pthread - yes
-- Found Threads: TRUE  
-- Found rt: /usr/lib/aarch64-linux-gnu/librt.so  
Include directories: /data/vaccelrt/src
-- Configuring done
-- Generating done
-- Build files have been written to: /data/vaccelrt/build_coral
```

Finally, building the plugin is as simple as issueing a make command:

```
make
```

The plugin is available at:

```
vaccelrt/build_coral/plugins/coral/libvaccel-coral.so
```

## Extra Files 

To run an example on the Google Coral Edge TPU, follow the instructions available at [Running a simple example](/run).

The files needed for classification are:

```
mobilenet_v1_1.0_224_quant_edgetpu.tflite
imagenet_labels.txt
```

available for download from: [https://github.com/google-coral/test_data](https://github.com/google-coral/test_data).

[^1]: Support for Google Coral is [WiP](https://github.com/cloudkernels/vaccel/pull/14), and will be available shortly in the main branch.
