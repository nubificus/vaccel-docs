<!-- markdownlint-disable -->

# module `tensorflow`




**Global Variables**
---------------
- **ffi**


---

## class `Node`
A representation of TensorFlow graph input or output node 

### method `__init__`

```python
__init__(name, node_id)
```






---

#### property id





---

#### property name







---

### method `to_cffi`

```python
to_cffi()
```






---

## class `TensorType`
An enumeration. 





---

## class `Tensor`
A representation of a Tensor 

### method `__init__`

```python
__init__(dims, dtype: TensorType)
```






---

#### property data





---

#### property dims







---

### method `get`

```python
get(indices)
```





---

### method `get_index`

```python
get_index(indices)
```





---

### method `len`

```python
len()
```





---

### method `to_cffi`

```python
to_cffi()
```






---

## class `TensorFlowModel`







---

### method `load`

```python
load(session, resource)
```





---

### method `run`

```python
run(session, resource, in_nodes, in_tensors, out_nodes)
```








---


