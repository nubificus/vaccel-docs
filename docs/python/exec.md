<!-- markdownlint-disable -->

# module `exec`




**Global Variables**
---------------
- **ffi**


---

## class `Vaccel_Args`
A helper class for converting argument lists to the appropriate vAccel format 




---

### method `vaccel_args`

```python
vaccel_args(args: List[Any]) → List[VaccelArg]
```

Convert a list of arguments to a list of VaccelArg objects 



**Args:**
 
  - <b>`args `</b>:  A list of integers 



**Returns:**
 A list of VaccelArg objects 




---

## class `Exec_Operation`
An Exec Operation model vAccel resource 



**Attributes:**
 
 - <b>`def_arg_write`</b> (bytes):  The result of the operation 





---

## class `Exec`
An Exec operation model vAccel resource 



**Attributes:**
 
 - <b>`__op__`</b>:  The genop operation type 




---

### classmethod `exec`

```python
exec(library: str, symbol: str, arg_read: List[Any], arg_write: List[Any])
```

Performs the Exec using vAccel over genop. 



**Args:**
 
 - <b>`library`</b>:  Path to the shared object containing the function that the user wants to call 
 - <b>`symbol`</b>:  Name of the function contained in the above shared object 
 - <b>`arg_read`</b>:  A list of inputs 



**Returns:**
 
 - <b>`arg_write`</b>:  A list of outputs 


---

## class `Exec_with_resource`
An Exec with resource model vAccel resource. 



**Attributes:**
 
 - <b>`__op__`</b>:  The genop operation type 




---

### classmethod `exec_with_resource`

```python
exec_with_resource(
    obj: str,
    symbol: str,
    arg_read: List[Any],
    arg_write: List[Any]
)
```

Performs the Exec with resource operation 



**Args:**
 
 - <b>`object`</b>:  Filename of a shared object to be used with vaccel exec 
 - <b>`symbol`</b>:  Name of the function contained in the above shared object 
 - <b>`arg_read`</b>:  A list of inputs 



**Returns:**
 
 - <b>`arg_write`</b>:  A list of outputs 




---


