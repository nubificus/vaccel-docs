# vAccel User API

The vAccel API is work in progress. This page presents the current form of the
vAccel frontend API, that is what is presented to the user. Using this API
users can build vAccel applications that interface directly with libvaccel.so
and their operations can be executed using vAccel plugins.

## Image inference

vAccel supports a set of operations for Image inference using the following
primitive functions (per operation):

#### Image classification

```C
int vaccel_image_classification(struct vaccel_session *sess, const void *img,
		unsigned char *out_text, unsigned char *out_imgname,
		size_t len_img, size_t len_out_text, size_t len_out_imgname);
```

- `struct vaccel_session *sess`: a pointer to a vAccel session created using
  `vaccel_sess_init()`;
- `const void *img`: the buffer holding the data to the input image.
- `unsigned char *out_text`: the buffer holding the classification tag output
- `unsigned char *out_imgname`: the name of the processed image, created as a
session resource (EXPERIMENTAL).
- `size_t len_img`: the size of `img` in bytes.
- `size_t len_out_text`: the size of `out_text` in bytes.
- `size_t len_out_imgname`: the size of `out_imagename` in bytes.

#### Image segmentation
```C
int vaccel_image_segmentation(struct vaccel_session *sess, const void *img,
		const unsigned char *out_imgname, size_t len_img,
		size_t len_out_imgname);
```

- `struct vaccel_session *sess`: a pointer to a vAccel session created using
  `vaccel_sess_init()`;
- `const void *img`: the buffer holding the data to the input image.
- `unsigned char *out_imgname`: the name of the processed image, created as a
session resource (EXPERIMENTAL).
- `size_t len_img`: the size of `img` in bytes.
- `size_t len_out_imgname`: the size of `out_imagename` in bytes.

#### Object detection
```C
int vaccel_image_detection(struct vaccel_session *sess, const void *img,
		const unsigned char *out_imgname, size_t len_img,
		size_t len_out_imgname);
```

- `struct vaccel_session *sess`: a pointer to a vAccel session created using
  `vaccel_sess_init()`;
- `const void *img`: the buffer holding the data to the input image.
- `unsigned char *out_imgname`: the name of the processed image, created as a
session resource (EXPERIMENTAL).
- `size_t len_img`: the size of `img` in bytes.
- `size_t len_out_imgname`: the size of `out_imagename` in bytes.

#### Pose estimation
```C
int vaccel_image_pose(struct vaccel_session *sess, const void *img,
		const unsigned char *out_imgname, size_t len_img,
		size_t len_out_imgname);
```

- `struct vaccel_session *sess`: a pointer to a vAccel session created using
  `vaccel_sess_init()`;
- `const void *img`: the buffer holding the data to the input image.
- `unsigned char *out_imgname`: the name of the processed image, created as a
session resource (EXPERIMENTAL).
- `size_t len_img`: the size of `img` in bytes.
- `size_t len_out_imgname`: the size of `out_imagename` in bytes.

#### Monocular Depth
```C
int vaccel_image_depth(struct vaccel_session *sess, const void *img,
		const unsigned char *out_imgname, size_t len_img,
		size_t len_out_imgname);
```

- `struct vaccel_session *sess`: a pointer to a vAccel session created using
  `vaccel_sess_init()`;
- `const void *img`: the buffer holding the data to the input image.
- `unsigned char *out_imgname`: the name of the processed image, created as a
session resource (EXPERIMENTAL).
- `size_t len_img`: the size of `img` in bytes.
- `size_t len_out_imgname`: the size of `out_imagename` in bytes.


## BLAS library functions

#### Matrix-to-matrix multiplication
```C
int vaccel_sgemm(struct vaccel_session *sess, uint32_t k, uint32_t m,
		uint32_t n, size_t len_a, size_t len_b, size_t len_c,
		float *a, float *b, float *c);
```

- `struct vaccel_session *sess`: a pointer to a vAccel session created using
  `vaccel_sess_init()`.
- `uint32_t k`: first dimension of matrix A & matrix C.
- `uint32_t l`: second dimension of matrix A & first dimension of matrix B.
- `uint32_t n`: second dimension of matrix B & matrix C.
- `size_t len_a`: size of matrix A in bytes.
- `size_t len_b`: size of matrix B in bytes.
- `size_t len_c`: size of matrix C in bytes.
- `float *a`: pointer to matrix A.
- `float *b`: pointer to matrix B.
- `float *c`: pointer to matrix C.

#### Array copy
```C
int vaccel_fpga_arraycopy(struct vaccel_session *sess, int array[],
			 int out_array[], size_t len_array);
```

- `struct vaccel_session *sess`: a pointer to a vAccel session created using
  `vaccel_sess_init()`.
- `int array[]`: input array.
- `int out_array[]`: output array.
- `size_t len_array`: length of input & output arrays.

#### Vector add 
```C
int vaccel_fpga_vadd(struct vaccel_session *sess, float A[], float B[], 
		    float C[], size_t len_a, size_t len_b, size_t len_c);
```

- `struct vaccel_session *sess`: a pointer to a vAccel session created using
  `vaccel_sess_init()`.
- `float A[]`: input vector A.
- `float B_array[]`: input vector B.
- `float C_array[]`: output vector C.
- `size_t len_a`: length of vector A.
- `size_t len_b`: length of vector B.
- `size_t len_c`: length of vector C.

#### Matrix-to-matrix multiplication and addition simple [WiP]
```C
int vaccel_fpga_mmult(struct vaccel_session *sess, float A_array[], 
		     float B_array[], float C_array[], float D_out[])
```

- `struct vaccel_session *sess`: a pointer to a vAccel session created using
  `vaccel_sess_init()`.
- `float A_array[]`: input array A.
- `float B_array[]`: input array B.
- `float C_array[]`: input array C.
- `float D_out[]`: output array D.
- `int out_array[]`: output array.


## Generic executor

#### Exec
```C
int vaccel_exec(struct vaccel_session *sess, const char *library,
                const char *fn_symbol, struct vaccel_arg *read,
                size_t nr_read, struct vaccel_arg *write, size_t nr_write);
```

- `struct vaccel_session *sess`: a pointer to a vAccel session created using
  `vaccel_sess_init()`.
- `const char *library`: name of the shared object to open.
- `const char *fn_symbol`: name of the symbol to dereference in the shared object `library`.
- `struct vaccel_arg *read`: pointer to an array of `struct vaccel_arg` read-only arguments to `fn_symbol`.
- `size_t nr_read`: number of elements for the `read` array.
- `struct vaccel_arg *write`: pointer to an array of `struct vaccel_arg` write-only arguments to `fn_symbol`.
- `size_t nr_write`: number of elements for the `write` array.

## TensorFlow operations

#### TensorFlow session load

```C
int vaccel_tf_session_load(struct vaccel_session *session,
			  struct vaccel_tf_saved_model *model,
			  struct vaccel_tf_status *status);
```

- `struct vaccel_session *sess`: a pointer to a vAccel session created using
- `struct vaccel_tf_saved_model *model`: a saved model structure, created using `vaccel_tf_saved_model_new()`.
- `struct vaccel_tf_status *status`: return value in the form of `struct vaccel_tf_status()`.

#### TensorFlow session run

```C
int vaccel_tf_session_run(struct vaccel_session *session,
  	      		 const struct vaccel_tf_saved_model *model, const struct vaccel_tf_buffer *run_options,
 		         const struct vaccel_tf_node *in_nodes, struct vaccel_tf_tensor *const *in, int nr_inputs,
		         const struct vaccel_tf_node *out_nodes, struct vaccel_tf_tensor **out, int nr_outputs,
        		 struct vaccel_tf_status *status);
```
- `struct vaccel_session *sess`: a pointer to a vAccel session created using
- `struct vaccel_tf_saved_model *model`: a saved model structure, created using `vaccel_tf_saved_model_new()`.
- `const struct vaccel_tf_buffer *run_options`: runtime parameters for the TF instance in the form of `{data, size}`.
- `const struct vaccel_tf_node *in_nodes`: input nodes.
- `const struct vaccel_tf_tensor *const *in`: array of input tensors.
- `int nr_inputs`: size of input tensors array.
- `const struct vaccel_tf_node *out_nodes`: output nodes.
- `const struct vaccel_tf_tensor **out`: array of input tensors.
- `int nr_outputs`: size of output tensors array.
- `struct vaccel_tf_status *status`: return value in the form of `struct vaccel_tf_status()`.

#### TensorFlow session delete

```C
int vaccel_tf_session_delete(struct vaccel_session *session,
			     struct vaccel_tf_saved_model *model,
		   	     struct vaccel_tf_status *status);
```
- `struct vaccel_session *sess`: a pointer to a vAccel session created using
- `struct vaccel_tf_saved_model *model`: a saved model structure, created using `vaccel_tf_saved_model_new()`.
- `struct vaccel_tf_status *status`: return value in the form of `struct vaccel_tf_status()`.


## Misc operations

#### MinMax

```C
int vaccel_minmax(struct vaccel_session *sess, const double *indata, 
		 int ndata, int low_threshold, int high_threshold, 
		 double *outdata, double *min, double *max);
```

- `struct vaccel_session *sess`: a pointer to a vAccel session created using
  `vaccel_sess_init()`.
- `const double *indata`: input data (text file, one number per line).
- `int ndata`: input size (number of lines).
- `int low_threshold`: lower threshold for the minmax algorithm.
- `int high_threshold`: higher threshold for the minmax algorithm.
- `double *outdata`: array of output data.
- `double *min`: minimum number from input data set.
- `double *max`: maximum number from input data set.


