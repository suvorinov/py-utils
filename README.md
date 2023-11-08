# py-utils

Коллекция небольших функций и классов Python, которые делают работу над проектами проще.
Это не полная коллекция, но она мне очень помогла в прошлом, и я буду продолжать ее расширять.

## В работе !!!

### Installation

```
pip install py-utils
```

### Usage

``` python
from py_utils import print_duration

@print_duration
def fibonacci(n):
    if n in (1, 2):
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)
 
print(fibonacci(10))

```
