Once you have [installed the packages], you can start using it to create value objects and enrich your domain models.

## Your First Value Object

The `value-object-sindri` package comes with a set of built-in value objects that you can use directly in your code
without any additional setup. To create your first value object, follow these steps:

1. First import the value object class you want to use from the `value_object` module.
2. Then create an instance of the value object by passing the primitive value to its constructor.
3. Finally, you can use the value object in your code and access its value via the `.value` attribute.

```python
from value_object import Integer, String

age = Integer(30)
name = String("John Doe")

print(f"Name: {name.value}, Age: {age.value}")  # Output -> Name: John Doe, Age: 30
```

!!! tip "More about Value Objects"
    Value objects has a lot more to offer. You can learn more about the value object pattern, the built-in value objects 
    that are implemented, the validation logic behind each value object, and how to extend or create your custom value 
    objects in the [Value Objects] section.

[installed the packages]: installation.md
[Value Objects]: ../value_objects/index.md
