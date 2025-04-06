<!-- markdownlint-disable -->

# module `pynq_parallel`

---

## class `Pynq_parallel`

A Pynq parallel model vAccel resource.

**Attributes:**

- <b>`__op__`</b>: The genop operation type
- <b>`def_arg_write`</b> (bytes): The result of the operation

---

### classmethod `pynq_parellel`

```python
pynq_parellel(a: float, len_a: int)
```

Executes Pynq parallel operation using vAccel over genop.

**Args:**

- <b>`a`</b>: A float for the array a
- <b>`len_a`</b>: An integer giving the length of the array

**Returns:**

- <b>`b`</b>: A float for the array b
- <b>`add_out`</b>: A float for the addition
- <b>`mult_out`</b>: A float for the multiplication

---
