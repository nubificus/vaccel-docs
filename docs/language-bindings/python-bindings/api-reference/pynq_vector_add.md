<!-- markdownlint-disable -->

# module `pynq_vector_add`

---

## class `Pynq_vector_add`

A Pynq vector add model vAccel resource.

**Attributes:**

- <b>`__op__`</b>: The genop operation type
- <b>`def_arg_write`</b> (bytes): The result of the operation

---

### classmethod `pynq_vector_add`

```python
pynq_vector_add(len_a: int, len_b: int)
```

Executes Pynq vector add operation using vAccel over genop.

**Args:**

- <b>`len_a`</b>: An integer giving the length of the array a
- <b>`len_b`</b>: An integer giving the length of the array b

**Returns:**

- <b>`a`</b>: A float for the array a
- <b>`b`</b>: A float for the array b
- <b>`c`</b>: A float for the result of the addition

---
