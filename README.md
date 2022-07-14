# HashIndex

[![tests Actions Status](https://github.com/manimino/hashindex/workflows/tests/badge.svg)](https://github.com/manimino/hashindex/actions)

Find Python objects by their attributes.

`pip install hashindex`

Usage:

```
from hashindex import HashIndex
hi = HashIndex(objects, ['attr1', 'attr2', 'attr3'])
hi.find(                                  # find objects
    match={'attr1': a, 'attr2': [b, c]},  # where attr1 == a and attr2 in [b, c]
    exclude={'attr3': d}                  # and attr3 != d
)
```

Any Python object can be indexed: class instances, namedtuples, dicts, strings, floats, ints, etc.

In addition to attributes, HashIndex can find objects by user-defined functions.  
This allows for finding by nested attributes and many more applications. 

____

## Examples

### Find dicts by attribute

```
from hashindex import HashIndex

objects = [
    {'order': 1, 'size': 'regular', 'topping': 'smothered'}, 
    {'order': 2, 'size': 'regular', 'topping': 'diced'}, 
    {'order': 3, 'size': 'large', 'topping': 'covered'},
    {'order': 4, 'size': 'triple', 'topping': 'chunked'}
]

hi = HashIndex(objects, on=['size', 'topping'])

# returns order 1
hi.find(match={'size': 'regular', 'topping': 'smothered'})  

# returns orders 1 and 2
hi.find(
    match={'size': ['regular', 'large']},  # match 'regular' or 'large' sizes
    exclude={'topping': 'covered'}         # exclude where topping is 'covered'
)
```

### Find by nested attribute, using a function

```
class Order:
    def __init__(self, num, size, toppings):
        self.num = num
        self.size = size
        self.toppings = toppings
    
objects = [
    Order(1, 'regular', ['scattered', 'smothered', 'covered']),
    Order(2, 'large', ['scattered', 'covered', 'peppered']),
    Order(3, 'large', ['scattered', 'diced', 'chunked']),
    Order(4, 'triple', ['all the way']),
]

def has_cheese(obj):
    return 'covered' in obj.toppings or 'all the way' in obj.toppings
    
hi = HashIndex(objects, ['size', has_cheese])

# returns orders 1, 2 and 4
hi.find({has_cheese: True})  
```

### Find string objects

This example uses a FrozenHashIndex. A FrozenHashIndex works just like a HashIndex, but items cannot be added, removed, 
or updated after initialization.

FrozenHashIndex is faster than the regular HashIndex, and good for multithreaded use cases.

```
from hashindex import FrozenHashIndex

objects = ['one', 'two', 'three']

def e_count(obj):
    return obj.count('e')

hi = FrozenHashIndex(objects, [e_count, len])
hi.find({len: 3})       # returns ['one', 'two']
hi.find({e_count: 2})  # returns ['three']
```

### Bigger examples
 
 - [Document search]()
 - [Wordle solver]()

____

## How it works

At a high level, you can think of each attribute index as a dict of set of object IDs. Each attribute lookup
returns a set of object IDs. Then union / intersection / difference operations are performed on the results of those
lookups to find the object IDs matching the query constraints. Finally, the object corresponding to each ID is returned. 

In practice, HashIndex uses specialized data structures to achieve this in a fast, memory-efficient way.

[Would you like to know more?](docs/design.md)

____

## Notes

 - The objects do not need to be hashable. They are not serialized, copied, or persisted. HashIndex is just a container.
 - The attributes must be hashable.
 - If an object is missing an attribute, it will be indexed with a `None` value for that attribute.
 - HashIndex is mutable; `add`, `remove` and `update` of objects is supported.
 - If you do not need mutability, `FrozenHashIndex` is the immutable version. It is faster, more RAM-efficient, and 
thread-safe.
 - They are designed to store a billion items or more in memory on a decent-sized machine.

____

## HashIndex API

### 

____

## FrozenHashIndex API

### 


____

## Performance


