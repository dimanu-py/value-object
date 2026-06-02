Once you have [installed the packages], you can start using them to create value objects and 
generate test data using object mothers.

## Your First Value Object

The `value-object-sindri` package comes with a set of built-in value objects that you can use directly in your code
without any additional setup. To create your first value object, follow these steps:

1. First import the value object class you want to use from the `value_objects` module.
2. Then create an instance of the value object by passing the primitive value to its constructor.
3. Finally, you can use the value object in your code and access its value via the `.value` attribute.

```python
from value_objects import Integer, String

age = Integer(30)
name = String("John Doe")

print(f"Name: {name.value}, Age: {age.value}")  # Output -> Name: John Doe, Age: 30
```

!!! tip "More about Value Objects"
    Value objects has a lot more to offer. You can learn more about the value object pattern, the built-in value objects 
    that are implemented, the validation logic behind each value object, and how to extend or create your custom value 
    objects in the [Value Objects] section.

## Your First Object Mother

On the other hand, the `object-mother-sindri` package provides a set of built-in object mothers that you 
can use to generate realistic test data for your value objects. To create your first object mother, follow these steps:

1. First import the object mother classes you want to use from the `object_mother` module.
2. Then use the `any()` method of the object mother to generate a random primitive value
3. Finally, you can use the generated values in your tests.

```python
from object_mother import IntegerPrimitivesMother, StringPrimitivesMother

def test_user_creation() -> None:
    user_request = {
        "age": IntegerPrimitivesMother.any(),
        "name": StringPrimitivesMother.any()
    }
    ...
```

!!! tip "More about Object Mothers"
    Object mothers has a lot more to offer too. You can learn more about the object mother pattern, the built-in object 
    mothers that are implemented, what methods they provide, and how to extend or create your custom object mothers in the 
    [Object Mothers] section.

[installed the packages]: installation.md
[Value Objects]: ../value_objects/index.md
[Object Mothers]: ../object_mothers/index.md
