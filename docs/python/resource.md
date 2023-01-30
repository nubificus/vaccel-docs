<!-- markdownlint-disable -->

# module `resource`






---

## class `Resource`
A vAccel resource 

vAccel resources are not exposed as concrete data structures from the vAccel runtime for the end-programmer to use. Instead, they are embedded in concrete resources, e.g. a TensorFlow model, hence this is an abstract class with common methods for all exposed methods of vAccel resources 




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

Returns true if the resource is registered with the session 




---


