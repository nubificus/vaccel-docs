# vAccel API (WiP)

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

