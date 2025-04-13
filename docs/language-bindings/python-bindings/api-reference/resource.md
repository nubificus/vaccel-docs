<!-- markdownlint-disable -->

# module `resource`




**Global Variables**
---------------
- **ffi**


---

## class `Resource`
A vAccel resource 

vAccel resources are not exposed as concrete data structures from the vAccel runtime for the end-programmer to use. Instead, they are embedded in concrete resources, e.g. a TensorFlow model, hence this is an abstract class with common methods for all exposed methods of vAccel resources 

### method `__init__`

```python
__init__(session, obj, rtype)
```








---

### method `create_resource`

```python
create_resource(rtype)
```

Creates a resource from a file and returns a pointer to it 



**Args:**
 
 - <b>`rtype`</b>:  The resource type 



**Returns:**
 A pointer to the resource 

---

### method `destroy_resource`

```python
destroy_resource()
```





---

### method `id`

```python
id()
```

The id of a vAccel resource 

---

### method `is_registered`

```python
is_registered(session)
```

Checks if the resource is registered with the session 



**Args:**
 
 - <b>`session`</b>:  A vaccel.Session instance 



**Returns:**
 True if the resource is registered with the session 

---

### method `register_resource`

```python
register_resource()
```





---

### method `unregister_resource`

```python
unregister_resource()
```








---


