!!! info "Python Version Support"
    Both packages officially support Python 3.10 and higher.
    Older versions of Python may work, but they are not guaranteed to be compatible.

The project provides two independent packages you can install separately depending on your needs.

## Installing with pip

```bash
pip install value-object-sindri      # value objects only, zero runtime dependencies
pip install object-mother-sindri      # object mothers with faker for test data
pip install value-object-sindri object-mother-sindri  # both
```

## Installing with uv

```bash
uv add value-object-sindri
uv add object-mother-sindri --group test
```

## Next steps

Now that you have installed the packages, you can advance to the [First Steps] section to learn the basic features 
and how to create value objects and generate test data using object mothers.

[First Steps]: first_steps.md