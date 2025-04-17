<!-- markdownlint-disable -->

# module `tensorflow`

## **Global Variables**

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

A TensorFlow model vAccel resource

### method `__init__`

```python
__init__()
```

Create a TensorFlow model resource

---

### method `from_data`

```python
from_data(data: bytes)
```

Initialize a TensorFlow model from a byte array

---

### method `from_model_file`

```python
from_model_file(model_path: str)
```

Initialize a TensorFlow model by loading it from a .pb file

---

### method `from_session`

```python
from_session(session, model_path: str)
```

---

### method `id`

```python
id()
```

Id of the TensorFlow model

---

### method `is_registered`

```python
is_registered(session)
```

Returns True if the model is registered with session

---

### method `load_graph`

```python
load_graph(session)
```

---

### method `model_register`

```python
model_register()
```

---

### method `model_set_path`

```python
model_set_path(model_path: str)
```

---

### method `run`

```python
run(session, in_nodes, in_tensors, out_nodes)
```

---
