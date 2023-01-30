<!-- markdownlint-disable -->

# module `image_genop`






---

## class `ImageClassify`







---

### classmethod `classify`

```python
classify(image: 'str | bytes')
```

Classify image using vAccel over genop. 

Parameters 
---------- image : `str | bytes`   Filename or bytes object of the image. 

Returns 
---------- `str` : Classification tag 


---

## class `ImageDetect`







---

### classmethod `detect`

```python
detect(image: 'str | bytes')
```

Performs image detection operation using vAccel over genop 

Parameters 
---------- image : `str | bytes`   Filename or bytes object of the image. 

Returns 
---------- `str` : Detection result 


---

## class `ImageSegment`







---

### classmethod `segment`

```python
segment(image: 'str | bytes')
```

Performs image segmentation operation using vAccel over genop 

Parameters 
---------- image : `str | bytes`   Filename or bytes object of the image. 

Returns 
---------- `str` : Segmentation result 


---

## class `ImagePose`







---

### classmethod `pose`

```python
pose(image: 'str | bytes')
```

Perform image pose estimation operation using vAccel over genop 

Parameters 
---------- image : `str | bytes`   Filename or bytes object of the image. 

Returns 
---------- `str` : Pose result 


---

## class `ImageDepth`







---

### classmethod `depth`

```python
depth(image: 'str | bytes')
```

Perform image depth estimation operation using vAccel over genop 

Parameters 
---------- image : `str | bytes`   Filename or bytes object of the image. 

Returns 
---------- `str` : Depth result 




---


