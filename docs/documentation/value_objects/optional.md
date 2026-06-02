# Optional

The library provides an `Optional` class that follows the Optional/Maybe pattern. It acts as an
immutable container that may or may not hold a value, helping to avoid `None` checks and
`None`-related bugs throughout your codebase.

`Optional` is not a `ValueObject` subclass. Like `Aggregate`, it is a separate construct that
complements the value object pattern.

!!! warning "Not for modelling optional attributes"
    `Optional` is designed as a **return type** — it represents that an operation may or may not
    produce a result. It is not intended for modelling optional attributes of a class. For that,
    use `None` or a dedicated `ValueObject` subclass with a nullable value.

## Creating an Optional

There are several ways to create an `Optional` instance:

```python
from value_object import Optional

# Wrap a present value
present = Optional.of("hello")

# Create an empty Optional
empty = Optional.empty()

# Create from a nullable value
maybe = Optional.from_nullable(get_value_or_none())
```

## Checking for Values

```python
if maybe.is_present():
    print("Has a value")

if maybe.is_empty():
    print("No value")
```

## Extracting Values

Use `unwrap` when you are sure the Optional is present. It raises `ValueError` if empty.

```python
value = maybe.unwrap()
```

Provide a custom error with `unwrap_or_raise`:

```python
value = maybe.unwrap_or_raise(lambda: RuntimeError("Expected a value"))
```

## Transforming Values

Use `map` to transform the inner value without manually checking for emptiness:

```python
from value_object import Optional

result = (
    Optional.of("  hello world  ")
    .map(str.strip)
    .map(lambda s: s.upper())
    .map(lambda s: s.split())
)

print(result.unwrap())  # ["HELLO", "WORLD"]
```

`map` on an empty Optional returns an empty Optional — the function is never called.

## Branching with match

`match` takes two callbacks and executes the appropriate one:

```python
result = maybe.match(
    of=lambda v: f"Value: {v}",
    empty=lambda: "No value",
)
```

## Using with Value Objects

`Optional` works naturally with value objects:

```python
from value_object import Optional, String

maybe_name = Optional.of(String("Alice"))
greeting = maybe_name.map(lambda name: f"Hello, {name.value}!")
```

## raise_error helper

A `raise_error` utility is available for use in `match` expressions when you want to
raise an exception instead of providing a default:

```python
from value_object.optional import raise_error

value = maybe.match(
    of=lambda v: v,
    empty=lambda: raise_error(ValueError("Missing required value")),
)
```

## Summary

| Method              | Purpose                                           |
|---------------------|---------------------------------------------------|
| `of(value)`         | Wrap a present value (raises if `None`)           |
| `empty()`           | Create an empty Optional                          |
| `from_nullable(v)`  | Create from a value that might be `None`          |
| `lift(v, mapper)`   | Map a nullable value into an Optional             |
| `is_present()`      | Check if it holds a value                         |
| `is_empty()`        | Check if it is empty                              |
| `unwrap()`          | Extract the value or raise                        |
| `unwrap_or_raise(e)`| Extract the value or raise a custom error         |
| `map(func)`         | Transform the inner value                         |
| `match(of, empty)`  | Branch on presence or absence                     |
