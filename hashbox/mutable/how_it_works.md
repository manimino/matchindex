## How It Works, Mutable Edition

MutableAttrIndex contains a dict of set of object IDs.

Well, ok, it's a little more complicated than that. We don't always
use sets, because sets are REALLY inefficient for small collections.

Bytes per integer, by collection size

|              | 1     | 10   | 50   | 100  | 1000 | 10000  |
|--------------|-------|------|------|------|------|--------|
| Python tuple | 56.8  | 14.0 | 9.3  | 8.6  | 32.2 | 39.7   |
| Python set   | 235.6 | 82.1 | 46.0 | 84.5 | 57.2 | 84.6   |
| cykhash set  | 168.5 | 26.5 | 23.6 | 22.3 | 17.0 | 13.6   |
| numpy array  | 169.6 | 23.4 | 11.1 | 9.6  | 8.2  | 8.0    |

Those numbers were measured by examining process-level memory usage before and after
collections were created, so there's a little +/- there.
For example, a set containing a SINGLE INTEGER is actually 248 bytes.

**248.**

**Bytes.**

To store a single 8-byte integer.

Seriously, you can check it yourself.
```
from pympler.asizeof import asizeof
asizeof(set([1]))
# Yep, says 248. Yes, that's actually bytes and not bits.
```

Imagine if all our attribute values were unique, and we're storing a dict of millions of sets of size 1.
Ouch. Yeah, let's not do that. In fact, let's not use Python set() at all! We're only storing numbers, so a typed set
will be much more efficient. The cykhash sets are just perfect for this. They're about as fast as Python sets,
and around 1/4 the RAM.

For smaller collections, below 100 numbers, cykhash is a bit inefficient, so we use tuples there instead.
While they are immutable, it's not a big deal to discard a tuple of size 100 and make another one.

And for collections of size 1... we just store the number.

Using different collection sizes like this helps keep our memory usage from going too crazy.
A naive implementation would spend a gigabyte of RAM indexing a few million integers. While this
adds a bit of code complexity, it's a pretty great trade. Just gotta test it for each collection size, and we do.

For the FrozenHashBox, we use numpy arrays, because they're the best. As long as you don't need to add or remove
objects, anyway.