# vAccel User API

The vAccel API is work in progress. This page presents the current form of the
vAccel frontend API, that is what is presented to the user. Using this API users
can build vAccel applications that interface directly with libvaccel.so and
their operations can be executed using vAccel plugins.

## Image inference

vAccel supports a set of operations for Image inference using the following
primitive functions (per operation):

### Image classification

```c
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

### Image segmentation

```c
int vaccel_image_segmentation(struct vaccel_session *sess, const void *img,
                              unsigned char *out_imgname, size_t len_img,
                              size_t len_out_imgname);
```

- `struct vaccel_session *sess`: a pointer to a vAccel session created using
  `vaccel_session_init()`.
- `const void *img`: the buffer holding the data to the input image.
- `unsigned char *out_imgname`: the name of the processed image, created as a
  session resource (EXPERIMENTAL).
- `size_t len_img`: the size of `img` in bytes.
- `size_t len_out_imgname`: the size of `out_imagename` in bytes.

### Object detection

```c
int vaccel_image_detection(struct vaccel_session *sess, const void *img,
                           unsigned char *out_imgname, size_t len_img,
                           size_t len_out_imgname);
```

- `struct vaccel_session *sess`: a pointer to a vAccel session created using
  `vaccel_session_init()`.
- `const void *img`: the buffer holding the data to the input image.
- `unsigned char *out_imgname`: the name of the processed image, created as a
  session resource (EXPERIMENTAL).
- `size_t len_img`: the size of `img` in bytes.
- `size_t len_out_imgname`: the size of `out_imagename` in bytes.

### Pose estimation

```c
int vaccel_image_pose(struct vaccel_session *sess, const void *img,
                      unsigned char *out_imgname, size_t len_img,
                      size_t len_out_imgname);
```

- `struct vaccel_session *sess`: a pointer to a vAccel session created using
  `vaccel_session_init()`.
- `const void *img`: the buffer holding the data to the input image.
- `unsigned char *out_imgname`: the name of the processed image, created as a
  session resource (EXPERIMENTAL).
- `size_t len_img`: the size of `img` in bytes.
- `size_t len_out_imgname`: the size of `out_imagename` in bytes.

### Monocular Depth

```c
int vaccel_image_depth(struct vaccel_session *sess, const void *img,
                       unsigned char *out_imgname, size_t len_img,
                       size_t len_out_imgname);
```

- `struct vaccel_session *sess`: a pointer to a vAccel session created using
  `vaccel_session_init()`.
- `const void *img`: the buffer holding the data to the input image.
- `unsigned char *out_imgname`: the name of the processed image, created as a
  session resource (EXPERIMENTAL).
- `size_t len_img`: the size of `img` in bytes.
- `size_t len_out_imgname`: the size of `out_imagename` in bytes.

## BLAS library functions

### Matrix-to-matrix multiplication

```c
int vaccel_sgemm(struct vaccel_session *sess, long long int m, long long int n,
                 long long int k, float *alpha, float *a, long long int lda,
                 float *b, long long int ldb, float beta, float *c,
                 long long int ldc);
```

- `struct vaccel_session *sess`: a pointer to a vAccel session created using
  `vaccel_session_init()`.
- `long long int m`: first dimension of matrix A & matrix C.
- `long long int n`: second dimension of matrix A & first dimension of matrix B.
- `long long int k`: second dimension of matrix B & matrix C.
- `long long int lda`: size of matrix A in bytes.
- `long long int ldb`: size of matrix B in bytes.
- `long long int ldc`: size of matrix C in bytes.
- `float *a`: pointer to matrix A.
- `float *b`: pointer to matrix B.
- `float *c`: pointer to matrix C.
- `float alpha`: the floating point number to be used in `alpha` X (`A` X `B`) +
  `beta` X `C`.
- `float beta`: the floating point number to be used in `alpha` X (`A` X `B`) +
  `beta` X `C`.

### Array copy

```c
int vaccel_fpga_arraycopy(struct vaccel_session *sess, int array[],
                          int out_array[], size_t len_array);
```

- `struct vaccel_session *sess`: a pointer to a vAccel session created using
  `vaccel_session_init()`.
- `int a[]`: input array.
- `int out_a[]`: output array.
- `size_t len_a`: length of input & output arrays.

### Matrix-to-matrix multiplication simple

```c
int vaccel_fpga_mmult(struct vaccel_session *sess, float a[], float b[],
                      float c[], size_t len_a);
```

- `struct vaccel_session *sess`: a pointer to a vAccel session created using
  `vaccel_session_init()`.
- `float a[]`: input array A.
- `float b[]`: input array B.
- `float c[]`: output array C.
- `size_t len_a`: length of array A.

### Matrix-to-matrix multiplication and addition simple [WiP]

```c
int vaccel_fpga_parallel(struct vaccel_session *sess, float a[], float b[],
                         float add_output[], float mult_output[], size_t len_a);
```

- `struct vaccel_session *sess`: a pointer to a vAccel session created using
  `vaccel_session_init()`.
- `float a[]`: input array A.
- `float b[]`: input array B.
- `float add_output[]`: addition output array.
- `float mult_output[]`: multiplication output array.
- `size_t len_a`: length of array A.

### Vector add

```c
int vaccel_fpga_vadd(struct vaccel_session *sess, float a[], float b[],
                     float c[], size_t len_a, size_t len_b);
```

- `struct vaccel_session *sess`: a pointer to a vAccel session created using
  `vaccel_session_init()`.
- `float a[]`: input array A.
- `float b[]`: input array B.
- `float c[]`: output array C.
- `size_t len_a`: length of array A.
- `size_t len_b`: length of array B.

## Generic executors

### Exec

```c
int vaccel_exec(struct vaccel_session *sess, const char *library,
                const char *fn_symbol, struct vaccel_arg *read,
                size_t nr_read, struct vaccel_arg *write, size_t nr_write);
```

- `struct vaccel_session *sess`: a pointer to a vAccel session created using
  `vaccel_session_init()`.
- `const char *library`: name of the shared object to open.
- `const char *fn_symbol`: name of the symbol to dereference in the shared
  object `library`.
- `struct vaccel_arg *read`: pointer to an array of `struct vaccel_arg`
  read-only arguments to `fn_symbol`.
- `size_t nr_read`: number of elements for the `read` array.
- `struct vaccel_arg *write`: pointer to an array of `struct vaccel_arg`
  write-only arguments to `fn_symbol`.
- `size_t nr_write`: number of elements for the `write` array.

### Exec with resource

```c
int vaccel_exec_with_resource(struct vaccel_session *sess,
                              struct vaccel_resource *resource,
                              const char *fn_symbol, struct vaccel_arg *read,
                              size_t nr_read, struct vaccel_arg *write,
                              size_t nr_write);
```

- `struct vaccel_session *sess`: a pointer to a vAccel session created using
  `vaccel_session_init()`.
- `struct vaccel_resource *resource`: pointer to a vAccel resource which
  contains the shared object created using `vaccel_resource_init()` or similar
  vAccel function, and registered to a session using
  `vaccel_resource_register()`.
- `const char *fn_symbol`: name of the symbol to dereference in the shared
  object `library`.
- `struct vaccel_arg *read`: pointer to an array of `struct vaccel_arg`
  read-only arguments to `fn_symbol`.
- `size_t nr_read`: number of elements for the `read` array.
- `struct vaccel_arg *write`: pointer to an array of `struct vaccel_arg`
  write-only arguments to `fn_symbol`.
- `size_t nr_write`: number of elements for the `write` array.

## TensorFlow operations

### TensorFlow session load

```c
int vaccel_tf_session_load(struct vaccel_session *session,
                           struct vaccel_resource *model,
                           struct vaccel_tf_status *status);
```

- `struct vaccel_session *sess`: a pointer to a vAccel session created using
  `vaccel_session_init()`.
- `struct vaccel_resource *model`: a vAccel resource structure, created using
  `vaccel_resource_init()` or similar vAccel function, and registered to a
  session using `vaccel_resource_register()`. Internally, it contains the model
  to be used.
- `struct vaccel_tf_status *status`: return value in the form of
  `struct vaccel_tf_status()`.

### TensorFlow session run

```c
int vaccel_tf_session_run(struct vaccel_session *session,
                          const struct vaccel_resource *model, const struct vaccel_tf_buffer *run_options,
                          const struct vaccel_tf_node *in_nodes, struct vaccel_tf_tensor *const *in, int nr_inputs,
                          const struct vaccel_tf_node *out_nodes, struct vaccel_tf_tensor **out, int nr_outputs,
                          struct vaccel_tf_status *status);
```

- `struct vaccel_session *sess`: a pointer to a vAccel session created using
  `vaccel_session_init()`.
- `struct vaccel_resource *model`: a vAccel resource structure. It should have
  been loaded previously with `vaccel_tf_session_load()`.
- `const struct vaccel_tf_buffer *run_options`: runtime parameters for the TF
  instance in the form of `{data, size}`.
- `const struct vaccel_tf_node *in_nodes`: input nodes.
- `const struct vaccel_tf_tensor *const *in`: array of input tensors.
- `int nr_inputs`: size of input tensors array.
- `const struct vaccel_tf_node *out_nodes`: output nodes.
- `const struct vaccel_tf_tensor **out`: array of input tensors.
- `int nr_outputs`: size of output tensors array.
- `struct vaccel_tf_status *status`: return value in the form of
  `struct vaccel_tf_status()`.

### TensorFlow session delete

```c
int vaccel_tf_session_delete(struct vaccel_session *session,
                             struct vaccel_resource *model,
                                struct vaccel_tf_status *status);
```

- `struct vaccel_session *sess`: a pointer to a vAccel session created using
  `vaccel_session_init()`.
- `struct vaccel_resource *model`: a vAccel resource structure that has been
  previously loaded using `vaccel_tf_session_load()`.
- `struct vaccel_tf_status *status`: return value in the form of
  `struct vaccel_tf_status()`.

## TensorFlow Lite operations

### TensorFlow Lite session load

```c
int vaccel_tflite_session_load(struct vaccel_session *session,
                               struct vaccel_resource *model);
```

- `struct vaccel_session *sess`: a pointer to a vAccel session created using
  `vaccel_session_init()`.
- `struct vaccel_resource *model`: a vAccel resource structure that represents
  the TFLite model, created using `vaccel_resource_init()` or similar vAccel
  function, and registered to a session using `vaccel_resource_register()`.

### TensorFlow Lite session run

```c
int vaccel_tflite_session_run(struct vaccel_session *session,
                              const struct vaccel_resource *model,
                              struct vaccel_tflite_tensor *const *in,
                              int nr_inputs, struct vaccel_tflite_tensor **out,
                              int nr_outputs, uint8_t *status);
```

- `struct vaccel_session *sess`: a pointer to a vAccel session created using
  `vaccel_session_init()`.
- `const struct vaccel_resource *model`: a vAccel resource structure. It should
  have been loaded previously with `vaccel_tflite_session_load()`.
- `struct vaccel_tflite_tensor *const *in`: array of input tensors.
- `int nr_inputs`: size of input tensors array.
- `struct vaccel_tflite_tensor **out`: array of input tensors.
- `int nr_outputs`: size of output tensors array.
- `uint8_t *status`: return value in the form of `uint8_t`.

### TensorFlow Lite session delete

```c
int vaccel_tflite_session_delete(struct vaccel_session *session,
                                 struct vaccel_resource *model);
```

- `struct vaccel_session *sess`: a pointer to a vAccel session created using
  `vaccel_session_init()`.
- `struct vaccel_resource *model`: a vAccel resource structure that has been
  previously loaded using `vaccel_tflite_session_load()`.

## Torch operations

### JIT loading and forwarding

```c
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
- `const struct vaccel_resource *model`: a vAccel resource structure to hold the
  model. It should have been previously created with `vaccel_resource_init()` or
  similar vAccel function and registered to the input session by using
  `vaccel_resource_register()`.
- `const struct vaccel_torch_buffer *run_options`: a buffer to hold other data
  that may be useful for the plugin. It may be empty.
- `struct vaccel_torch_tensor **in_tensor`: the input tensors to be used for the
  model inference.
- `int nr_read`: the number of the input tensors.
- `struct vaccel_torch_tensor **out_tensor`: this tensor array will hold the
  output tensors after the end of the operation.
- `int nr_write`: the number of the output tensors.

### Matrix-to-matrix multiplication

```c
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
- `struct vaccel_torch_tensor **out`: the tensor that will hold the output
  tensor.

## Misc operations

### MinMax

```c
int vaccel_minmax(struct vaccel_session *sess, const double *indata,
                  int ndata, int low_threshold, int high_threshold,
                  double *outdata, double *min, double *max);
```

- `struct vaccel_session *sess`: a pointer to a vAccel session created using
  `vaccel_session_init()`.
- `const double *indata`: input data (text file, one number per line).
- `int ndata`: input size (number of lines).
- `int low_threshold`: lower threshold for the minmax algorithm.
- `int high_threshold`: higher threshold for the minmax algorithm.
- `double *outdata`: array of output data.
- `double *min`: minimum number from input data set.
- `double *max`: maximum number from input data set.

## Generic operation

vAccel supports a generic operation that can be used to run all supported
operations:

```c
int vaccel_genop(struct vaccel_session *sess, struct vaccel_arg *read,
                 int nr_read, struct vaccel_arg *write, int nr_write);
```

- `struct vaccel_session *sess`: a pointer to a vAccel session created with
  `vaccel_session_init()`.
- `struct vaccel_arg *read`: the read arguments to be passed to the operation.
  The first argument should be the operation type, a `vaccel_op_type_t`
  instance.
- `int nr_read`: the number of the input arguments.
- `struct vaccel_arg *write`: the buffer that will hold the output arguments,
  after the end of the operation.
- `int nr_write`: the number of the write arguments.

## Debug operation

vAccel supports the no-op operation, which can be used for debugging purposes:

```c
int vaccel_noop(struct vaccel_session *sess);
```

- `struct vaccel_session *sess`: a pointer to a vAccel session created with
  `vaccel_session_init()`.
