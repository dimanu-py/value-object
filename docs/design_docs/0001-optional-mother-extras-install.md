---
created: 2026-05-29
status: Implemented
---

# Split into Independent Packages: value-object-sindri and object-mother-sindri

## Overview

Currently, `sindripy` ships both value object and object mother functionality in a single package with `faker` as a required runtime 
dependency. Object mothers need `faker`; value objects do not. The two modules are already fully independent at the source 
level — neither imports from the other.

This change splits the monolith into two independent PyPI packages within a monorepo:

- **`value-object-sindri`** — value object pattern (zero runtime dependencies)
- **`object-mother-sindri`** — object mother pattern (depends on `faker`)

Users install only what they need. Each package has its own version, changelog, and release cycle.

## Objectives

- Split the single package into two independent PyPI distributions
- Remove `faker` from value objects entirely (zero runtime deps for production code)
- Keep both packages in a single repository using UV workspaces
- Allow independent releases of each package via GitHub Actions
- Preserve all existing functionality with updated import paths

## Requirements

### Functional Requirements

- `pip install value-object-sindri` must install only the value object functionality with no `faker` dependency
- `pip install object-mother-sindri` must install only the object mother functionality with `faker`
- Import paths match the new package names: `from value_objects import Integer` and `from object_mother import IntegerPrimitivesMother`
- The `ObjectMother._faker()` method must raise a clear error if `faker` is missing
- All existing value object classes, methods, and validation behavior must remain unchanged
- All existing object mother classes and methods must remain unchanged

### Non-Functional Requirements

- Zero new runtime dependencies for the `value-object-sindri` package
- Monorepo must use UV workspaces for local development
- Development workflow (`uv sync --all-groups`) must install both packages and all dev dependencies
- CI must run lint, format, typing, and tests for both packages
- Release workflow must allow independent publish of each package

## Usage Examples

### Example 1: Install value objects only

```bash
pip install value-object-sindri
```

```python
from value_objects import Integer, String

age = Integer(30)
name = String("John Doe")
```

### Example 2: Install object mothers only

```bash
pip install object-mother-sindri
```

```python
from object_mother import IntegerPrimitivesMother, StringPrimitivesMother

random_age = IntegerPrimitivesMother.any()
random_name = StringPrimitivesMother.any()
```

### Example 3: Error when faker is missing (object-mother without faker)

```python
>>> from object_mother import ObjectMother
Traceback (most recent call last):
  ...
ImportError: The 'faker' package is required to use ObjectMother.
Install with: pip install object-mother-sindri
```

## Implementation Steps

Use vertical slicing: each step delivers an end-to-end increment that could theoretically be merged independently.

1. **Set up monorepo workspace structure** — Create `packages/` directory, add `[workspace]` to root `pyproject.toml`, create `packages/value-objects/pyproject.toml` and `packages/object-mother/pyproject.toml` with basic metadata and `faker` runtime dep only in object-mother. Move `src/sindripy/value_objects/` into `packages/value-objects/src/value_objects/` and `src/sindripy/mothers/` into `packages/object-mother/src/object_mother/`. Remove old `src/sindripy/` directory. Copy `_compat.py` and `py.typed` into each package.

2. **Fix internal imports for value-objects package** — Update all imports in `packages/value-objects/` to use the new package path (e.g., `from value_objects.aggregate import Aggregate` instead of `from sindripy.value_objects.aggregate import Aggregate`). The `__init__.py` becomes the top-level package init exposing `Integer`, `String`, `ValueObject`, etc. directly at `from value_objects import ...`.

3. **Fix internal imports for object-mother package** — Make `faker` import lazy in `ObjectMother._faker()` with a helpful error message. Update `__init__.py` and all imports to use `from object_mother.xxx import yyy`. Remove `faker` from runtime deps of value-objects.

4. **Restructure tests** — Split `test/sindripy/value_objects/` into `test/value_objects/` and create `test/object_mother/`. Update all test imports to match the new package paths. Add test configurations for both packages in the root `pyproject.toml`.

5. **Update documentation** — Rewrite `docs/documentation/getting_started/installation.md` and `README.md` to reflect two independent packages. Update `first_steps.md` and all doc examples with new import paths.

6. **Update GitHub Actions release workflow** — Modify `release.yml` to support independent releases:
   - Add `workflow_dispatch` input with a `package` selector (`value-objects`, `object-mother`, `both`)
   - Build the selected package(s) from `packages/<name>/` directory
   - Publish independently to PyPI
   - Each package maintains its own version and changelog

7. **Run quality checks** — Run `make test`, `make check-typing`, `make check-format`, `make check-lint` across both packages. Verify CI passes.

## Migration Plan

Existing users of `sindripy` need a clear path to migrate to the new packages. The migration is a breaking change (package names and import paths both change) and follows a phased approach.

### Phase 1: Ship new packages + compatibility `sindripy` v2

Publish `value-object-sindri` and `object-mother-sindri` to PyPI as new packages. Simultaneously publish a final **`sindripy` v2.0.0** that is a metapackage:

```toml
# sindripy v2.0.0 pyproject.toml
[project]
name = "sindripy"
dependencies = ["value-object-sindri", "object-mother-sindri"]

[project.optional-dependencies]
mother = ["object-mother-sindri"]
```

This means existing users who run `pip install sindripy` automatically get both new packages. The old `sindripy` source code is deleted — the v2 package is purely a dependency bridge.

### Phase 2: Deprecation notice in documentation

Mark `sindripy` as deprecated in the README and all docs. Add a deprecation warning banner:

> **sindripy is deprecated.** Use `value-object-sindri` and `object-mother-sindri` directly. See the [migration guide](link) for details.

Encourage users to switch their `pyproject.toml` dependencies and imports.

### Phase 3: Remove `sindripy` from PyPI (optional)

After a reasonable deprecation window (e.g. 6 months), yank the `sindripy` package from PyPI. Users must explicitly 
install `value-object-sindri` and/or `object-mother-sindri`.

### Per-user migration steps

A user migrating from `sindripy` to the new packages needs to:

| Step | Before (`sindripy`) | After |
|------|---------------------|-------|
| Install value objects | `pip install sindripy` | `pip install value-object-sindri` |
| Install object mothers | `pip install sindripy[mother]` | `pip install object-mother-sindri` |
| Import value objects | `from sindripy.value_objects import Integer` | `from value_objects import Integer` |
| Import mothers | `from sindripy.mothers import IntegerPrimitivesMother` | `from object_mother import IntegerPrimitivesMother` |
| pyproject.toml dep | `"sindripy"` | `"value-object-sindri"` and/or `"object-mother-sindri"` |

Most editors support bulk find-and-replace for import paths, making the migration mechanical:

```
sindripy.value_objects. → value_objects.
sindripy.mothers.       → object_mother.
```

### Compatibility considerations

- **No runtime shim**: No `sindripy` package is kept on PyPI that re-exports with old import paths. This avoids maintaining duplicate code.
- **No deprecation warnings in code**: Since old `sindripy` source is deleted entirely, there's no code to emit warnings. The deprecation is communicated through documentation and the metapackage's README.
- **Version alignment**: The metapackage `sindripy` v2.0.0 simply requires `value-object-sindri >= 1.0.0` and `object-mother-sindri >= 1.0.0` (or whatever the initial versions are).

## Decisions

- **Versioning strategy**: Each package versioned independently. Git tags use `value-objects-v{version}` and `object-mother-v{version}` (the directory layout name, not the PyPI name).
- **Repository name**: Kept as `sindri` / `sindripy` — the project brand stays.
- **CHANGELOG**: One per subpackage, managed by semantic-release per-package configuration.
- **PyPI names**: `value-object-sindri` and `object-mother-sindri` (since `value-objects` and `object-mother` are taken on PyPI).

## Notes

- The two modules are fully independent at the source level: zero cross-imports between value_objects and mothers. This makes the split mechanically simple.
- Mothers work with plain Python types (str, int, float, bool, list), not value object types. They generate raw test data.
- The existing `py.typed` marker must be duplicated in each package for PEP 561 compliance.
- The existing `_compat.py` typing helper is only needed by value-objects (mothers don't use `Self` or `override`), but both packages could have their own copy if needed later.
- The development environment installs both packages via UV workspace, so tests for value-objects can still use object-mother as a dev dependency for test data generation.
