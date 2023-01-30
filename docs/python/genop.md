<!-- markdownlint-disable -->

# module `genop`




**Global Variables**
---------------
- **ffi**


---

## class `VaccelOpType`
An enumeration. 





---

## class `VaccelArg`




### method `__init__`

```python
__init__(data) → None
```






---

#### property content





---

#### property raw_content







---

### method `to_cffi`

```python
to_cffi()
```






---

## class `VaccelArgInfo`




### method `__init__`

```python
__init__(datatype='', datasize='') → None
```








---

### method `detect_datatype`

```python
detect_datatype(arg: VaccelArg) → str
```





---

### classmethod `from_vaccel_arg`

```python
from_vaccel_arg(arg: VaccelArg)
```






---

## class `VaccelArgList`




### method `__init__`

```python
__init__(args: List[VaccelArg]) → None
```








---

### method `to_cffi`

```python
to_cffi()
```






---

## class `Genop`




### method `__init__`

```python
__init__()
```








---

### classmethod `genop`

```python
genop(
    session: Session,
    arg_read: List[VaccelArg],
    arg_write: List[VaccelArg]
) → List[str]
```

Vaccel genop. 

Paramters 
--------- session : `Any` arg_read : `list`  arg_write : `list` 

Returns 
--------- List of `str`. 




---


