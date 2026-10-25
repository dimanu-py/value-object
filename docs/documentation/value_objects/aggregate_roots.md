# Aggregate Roots

The library provides out-of-the-box support for defining aggregate roots using the `Aggregate` base class.

Aggregate roots are special domain entities that serve as the main entry point for interacting with a cluster 
of related objects. They ensure the integrity and consistency of the aggregate as a whole. Is typically used in
Domain-Driven Design (DDD) to model complex business domains.

## Features of Aggregate Roots

- **Composition**: Aggregate roots can contain multiple attributes, each represented by their own value objects.
- **String Representation**: Aggregate roots provide a clear string representation that includes all their non-private attributes.
- **Equality**: Aggregate roots implement equality based on the values of their attributes, ensuring that two instances
  with the same attribute values are considered equal.
- **Creation from Dictionary**: Aggregate roots can be instantiated from dictionaries through the `from_primitives` method, 
allowing easy deserialization from JSON or other data formats.
- **Primitive Extraction**: Aggregate roots can convert themselves back to dictionaries of primitive values using the
  `to_primitives` method, facilitating serialization and avoiding exposing internal structures.

## Working with Aggregate Roots

Unlike primitive value objects that wrap a single value, aggregates contain multiple attributes and represent
higher-level domain concepts.

!!! note "Aggregates and entities"
    Aggregate roots are not entities themselves, but rather the root of an aggregate that may contain entities and other value objects.
    Its attributes can be a mix of value objects and primitive types, but the aggregate itself is treated as a single unit.

### Defining an Aggregate Root

The easiest way to define an aggregate root is by subclassing the `Aggregate` base class and defining
its attributes using type annotations. Each attribute can be a primitive type or another value object.

```python
from value_object import AggregateRoot, String, Integer, List


class Address(AggregateRoot):
    _street: String
    _city: String
    _zip_code: String

    def __init__(self, street: str, city: str, zip_code: str):
        self._street = String(street)
        self._city = String(city)
        self._zip_code = String(zip_code)


address_from_constructor = Address(street="123 Main St", city="Springfield", zip_code="12345")
address_from_primitives = Address.from_primitives({
    "street": "123 Main St",
    "city": "Springfield",
    "zip_code": "12345"
})
```

???+ tip "Another option to create an Aggregate Root"
    ```python
    from value_object import Aggregate, String, Integer, List
    
    class Address(Aggregate):
        street: String
        city: String
        zip_code: String
    
        def __init__(self, street: String, city: String, zip_code: String):
            self.street = street
            self.city = city
            self.zip_code = zip_code
    
    address_from_constructor = Address(street=String("123 Main St"), city=String("Springfield"), zip_code=String("12345"))
    address_from_primitives = Address.from_primitives({
        "street": "123 Main St",
        "city": "Springfield",
        "zip_code": "12345"
    })
    ```

### Exposing Attributes

If you define Aggregate attributes as public you can access them directly:

```python
print(address_from_constructor.street)  # String("123 Main St")
```

A general good practice is to avoid exposing attributes directly. Instead, you can define
the attributes with a leading underscore to mark them as protected and try to encapsulate
their behavior through methods or properties.

!!! note "Protected attributes"
    The leading underscore is a convention in Python to indicate that an attribute is intended for internal use only.
    It does not enforce access restrictions, but it signals to other developers that the attribute should be treated as non-public.

With this approach, if we wanted to verify if two addresses are in the same city, we could define a method:

```python
from typing import Self
from value_object import AggregateRoot, String


class Address(AggregateRoot):
    _street: String
    _city: String
    _zip_code: String

    def __init__(self, street: str, city: str, zip_code: str):
        self._street = String(street)
        self._city = String(city)
        self._zip_code = String(zip_code)

    def is_in_same_city(self, other: Self) -> bool:
        return self._city == other._city
```

### Excluding Fields from Primitives

By default, `to_primitives` includes every non-private attribute of the aggregate. You can narrow down the
result with two optional, combinable parameters:

- `exclude`: the name of a single field, or a set of field names, to leave out of the resulting dictionary.
- `exclude_none`: when set to `True`, removes every field whose value is `None`, regardless of `exclude`.

```python
from value_object import AggregateRoot


class Customer(AggregateRoot):
    def __init__(self, customer_id: int, name: str, email: str | None = None):
        self.customer_id = customer_id
        self.name = name
        self.email = email


customer = Customer(customer_id=42, name="Alice Smith", email=None)

customer.to_primitives()
# {"customer_id": 42, "name": "Alice Smith", "email": None}

customer.to_primitives(exclude="email")
# {"customer_id": 42, "name": "Alice Smith"}

customer.to_primitives(exclude={"customer_id", "name"})
# {"email": None}

customer.to_primitives(exclude_none=True)
# {"customer_id": 42, "name": "Alice Smith"}

customer.to_primitives(exclude="name", exclude_none=True)
# {"customer_id": 42}
```

!!! note "Unknown field names"
    Passing a field name to `exclude` that does not exist on the aggregate has no effect; it is silently ignored.

!!! danger "Avoid using `to_primitives` to expose internal state"
    You can expose all the attributes too through the `to_primitives` method, however, the main 
    purpose of this method is to facilitate serialization and data transfer, not to expose internal state.
