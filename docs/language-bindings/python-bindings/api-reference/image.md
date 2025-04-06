<!-- markdownlint-disable -->

# module `image`

## **Global Variables**

- **ffi**

---

## class `ImageClassify`

An Image Classify model vAccel resource.

**Attributes:**

- <b>`out_size`</b> (int): The maximum length of the output tag

### method `__init__`

```python
__init__()
```

---

### classmethod `classify_from_filename`

```python
classify_from_filename(session: Session, source: str) → str
```

Initialize an ImageClassify model by loading image from filename

**Args:**

- <b>`session`</b>: A vaccel.Session instance
- <b>`source`</b>: A string containing the image's file path

**Returns:** A string containing the classifiaction tag

**Raises:**

- <b>`VaccelError`</b>: An error occured while executing the image
  classification operation

---

## class `ImageDetect`

An Image Detect model vAccel resource

**Attributes:**

- <b>`out_size`</b> (int): The maximum length of the output tag

### method `__init__`

```python
__init__()
```

---

### classmethod `detect_from_filename`

```python
detect_from_filename(session: Session, source: str) → str
```

Initialize an ImageDetect model by loading image from filename

**Args:**

- <b>`session`</b>: A vaccel.Session instance
- <b>`source`</b>: A string containing the image's file path

**Returns:** A string containing the detection result

**Raises:**

- <b>`VaccelError`</b>: An error occured while executing the image detection
  operation

---

## class `ImageSegment`

An Image Segment model vAccel resource

**Attributes:**

- <b>`out_size`</b> (int): The maximum length of the output tag

### method `__init__`

```python
__init__()
```

---

### classmethod `segment_from_filename`

```python
segment_from_filename(session: Session, source: str) → str
```

Initialize an ImageSegment model by loading image from filename

**Args:**

- <b>`session`</b>: A vaccel.Session instance
- <b>`source`</b>: A string containing the image's file path

**Returns:** A string containing the segmentation result

**Raises:**

- <b>`VaccelError`</b>: An error occured while executing the image segmentation
  operation

---

## class `ImagePose`

An Image Pose model vAccel resource

**Attributes:**

- <b>`out_size`</b> (int): The maximum length of the output tag

### method `__init__`

```python
__init__()
```

---

### classmethod `pose_from_filename`

```python
pose_from_filename(session: Session, source: str) → str
```

Initialize an ImagePose model by loading image from filename

**Args:**

- <b>`session`</b>: A vaccel.Session instance
- <b>`source`</b>: A string containing the image's file path

**Returns:** A string containing the pose result

**Raises:**

- <b>`VaccelError`</b>: An error occured while executing the image pose
  operation

---

## class `ImageDepth`

An Image Depth model vAccel resource

**Attributes:**

- <b>`out_size`</b> (int): The maximum length of the output tag

### method `__init__`

```python
__init__()
```

---

### classmethod `depth_from_filename`

```python
depth_from_filename(session: Session, source: str) → str
```

Initialize an ImageDepth model by loading image from filename

**Args:**

- <b>`session`</b>: A vaccel.Session instance
- <b>`source`</b>: A string containing the image's file path

**Returns:** A string containing the depth result

**Raises:**

- <b>`VaccelError`</b>: An error occured while executing the image depth
  operation

---
