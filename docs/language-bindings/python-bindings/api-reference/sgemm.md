<!-- markdownlint-disable -->

# module `sgemm`

---

## class `Sgemm`

An Sgemm model vAccel resource.

**Attributes:**

- <b>`def_arg_write`</b> (bytes): The result of the operation
- <b>`__op__`</b>: The genop operation type

---

### classmethod `sgemm`

```python
sgemm(m: int, n: int, k: int, alpha: float, lda: int, ldb: int, beta: float)
```

Performs the Sgemm using vAccel over genop.

**Args:**

- <b>`m`</b>: An integer for m dimension
- <b>`n`</b>: An integer for m dimension
- <b>`k`</b>: An integer for m dimension
- <b>`alpha`</b>: A float for scalar constant
- <b>`lda`</b>: An integer for the dimension
- <b>`ldb`</b>: An integer for the dimension
- <b>`beta`</b>: A float for scalar constant

**Returns:**

- <b>`ldc`</b>: An integer

---
