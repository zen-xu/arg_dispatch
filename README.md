# arg_dispatch
function can be dispatched by its arguments

## Example
```python
from arg_dispatch import dispatch


# Functions
@dispatch
def demo(a, b):
    return 'hello'
    
@dispatch
def demo(c):
    return 'world'
    

demo(a=1, b=2)  # return 'hello'
demo(c=3)       # return 'world'

# try to call a function which has not been registed
demo(d=4)       # raise `FunctionNotRegist`

# Methods
class Demo(object):
    @dispatch
    def demo(self, a, b):
        return 'hello'
        
    @dispatch
    def demo(self, c):
        return 'world'
        
instance = Demo()
instance.demo(a=1, b=2)  # return 'hello'
instance.demo(c=3)       # return 'world'

# try to call a method which has not been registed
instance.demo(d=4)       # raise `FunctionNotRegist`
```

## Notice💣
**positional arguments must be required**
```python
demo(1, 2)          # Boom!💣, raise `ArgumentError`
instance.demo(1, 2) # Boom!💣, raise `ArgumentError`
```

**default value is also not supported**
```python
@dispatch
def demo(a, b=1):            # Boom!💣, raise `ExistDefaultValue`
    return 'hello'
    
class Demo(object):
    @dispatch
    def demo(self, a, b=1):  # Boom!💣, raise `ExistDefaultValue`
        return 'hello'
```
