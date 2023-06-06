<!-- markdownlint-disable -->

# module `shared_object`




**Global Variables**
---------------
- **ffi**


---

## class `Object`




### method `__init__`

```python
__init__(session, obj, symbol)
```

Create a new vAccel object 




---

### method `create_shared_object`

```python
create_shared_object()
```

Creates a shared object from a file and returns a pointer to it 



**Args:**
 
 - <b>`obj`</b>:  The file path to the object file 



**Returns:**
 A pointer to the shared object 

---

### method `create_shared_objects`

```python
create_shared_objects(objects: List[str]) → List[str]
```

Creates a list of shared objects  from a list of file paths 



**Args:**
 
 - <b>`objects`</b>:  A list of file paths to the object files 



**Returns:**
 A list of pointers to the shared objects 

---

### method `destroy_shared_object`

```python
destroy_shared_object()
```





---

### method `object_symbol`

```python
object_symbol(symbol)
```





---

### method `register_object`

```python
register_object()
```





---

### method `unregister_object`

```python
unregister_object()
```








---


