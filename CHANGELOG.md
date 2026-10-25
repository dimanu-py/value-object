# CHANGELOG

<!-- version list -->

## v0.3.0 (2026-10-25)

### Build System

- Update packages
  ([`2de12f9`](https://github.com/dimanu-py/value-object/commit/2de12f9ee3855188a395c5f4dba9d8eba56496e2))

### Features

- Add new 'exclude_none' argument to exclude all fields with None values from primitives
  representation
  ([`335aaee`](https://github.com/dimanu-py/value-object/commit/335aaee8b38f8a4cde230ed3289f8a913adcc88f))

- Allow to_primitives to exclude more than one field when passing a set of strings
  ([`72751d5`](https://github.com/dimanu-py/value-object/commit/72751d5d0223d90b8c0108f64c051794c1ecd362))

- Support 'from_primitives' method to pass the different fields of the class separately instead of
  inside a single dictionary
  ([`b44a746`](https://github.com/dimanu-py/value-object/commit/b44a746d288c91b16eeb8711f25dfd5dcfffcd36))

- Support new 'exclude' argument when converting aggregate root to primitives selecting one field to
  be excluded
  ([`fdfee5a`](https://github.com/dimanu-py/value-object/commit/fdfee5a44c725d06f69f5c781686acc67b495cfa))

### Refactoring

- Rename Aggregate class to AggregateRoot since it's what represents in code
  ([`fdb62c7`](https://github.com/dimanu-py/value-object/commit/fdb62c733a021b3469c0d195547ae8db6379bf5a))


## v0.2.0 (2026-06-02)

### Features

- Add Optional wrapper for nullable values with full test coverage
  ([`9b4d197`](https://github.com/dimanu-py/value-object/commit/9b4d1977eb9cad1a407b67437872261dc1adedb4))

- Export Optional from package facade
  ([`7cbd4b8`](https://github.com/dimanu-py/value-object/commit/7cbd4b8a2275b255714cbbda037d439a9c40beb4))


## v0.1.0 (2026-06-02)

### Features

- **value-object**: Add value object pattern implementation from sindripy
  ([`f1a49a3`](https://github.com/dimanu-py/value-object/commit/f1a49a37eb1330da51f1efc8620115d1ebded271))
