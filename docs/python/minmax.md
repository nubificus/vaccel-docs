<!-- markdownlint-disable -->

# module `minmax`






---

## class `MinMax`
A MinMax model vAccel resource. 



**Attributes:**
 
 - <b>`def_arg_write`</b> (bytes):  The result of the operation 
 - <b>`__op__`</b>:  The genop operation type 




---

### classmethod `minmax`

```python
minmax(
    indata: int,
    ndata: 'str | bytes',
    low_threshold: 'int',
    high_threshold: 'int'
)
```

Performs the MinMax operation using vAccel over genop. 



**Args:**
 
 - <b>`indata`</b>:  An integer giving the number of inputs 
 - <b>`ndata`</b>:  A string or bytes object containing the ndata file path 
 - <b>`low_theshold`</b>:  An integer value for low threshold 
 - <b>`high_threshold`</b>:  An integer value for high threshold 



**Returns:**
 
 - <b>`outdata`</b>:  The array of floats, sorted 
 - <b>`min`</b>:  A float number for the min value 
 - <b>`max`</b>:  A float number for the max value  




---


