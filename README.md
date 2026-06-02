# Value Objects Sindri

### Value Object pattern for Python and Domain Driven Design applications

Easy use and customizable implementation for the Value Object pattern.

<p align="center">
  <a href="https://dimanu-py.github.io/value-object/getting_started/">Getting Started</a>&nbsp;&nbsp;•&nbsp;
  <a href="https://dimanu-py.github.io/value-object/value_objects/">Value Object Pattern</a>
</p>

<div align="center"><table><tr><td>
Sindri value object replaces ad hoc primitives and fragile validators with a consistent Value Object and Aggregate 
toolkit you can adopt quickly. 
Spin up validated value objects and aggregates with a simple and a small, focused API.

<br>

<b>Why use it?</b> Building your domain with Sindri lets you:

<ul style="list-style-type: none">
  <li>⏱️ Cut domain modeling and validation to seconds</li>
  <li>🛡️ Declare immutable, validated value objects with clear error messages</li>
  <li>🧩 Model aggregates with explicit invariants and composition</li>
  <li>🧰 Start from ready made primitives and identifiers or extend with your own</li>
  <li>🔧 Plug in custom validators, decorators, and typed primitives</li>
</ul>

</td></tr></table></div>

<div style="background-color: #1e2d3d; border: 1px solid #00d9ff; border-radius: 8px; padding: 16px; margin: 16px 0; display: flex; align-items: flex-start; gap: 12px;">
  <div style="font-size: 20px; color: #00d9ff; flex-shrink: 0;">💧</div>
  <div>
    <strong style="color: #00d9ff;">Created with Instant Python</strong><br>
    <span style="color: #a0a0a0;">This project was generated using <a href="https://github.com/dimanu-py/instant-python" style="color: #00d9ff; text-decoration: none;">Instant Python</a>, a fast, easy and reliable project generator for Python projects.</span>
  </div>
</div>

## Fast Kickstart

```bash
pip install value-object-sindri      # zero dependencies
```

Create a value object and use it in your domain:

```python
from value_object import Integer, String

age = Integer(30)
name = String("John Doe")

print(f"Name: {name.value}, Age: {age.value}")
```

## Next Steps

- [Installation](https://dimanu-py.github.io/value-object/getting_started/installation/)
- [First Steps](https://dimanu-py.github.io/value-object/getting_started/first_steps/)
- [Value Object Pattern](https://dimanu-py.github.io/value-object/value_objects/)
- [Contributing Guide](https://dimanu-py.github.io/value-object/contributing/contributing_guide/)

<div style="background-color: #1e2d3d; border: 1px solid #00d9ff; border-radius: 8px; padding: 16px; margin: 16px 0; display: flex; align-items: flex-start; gap: 12px;">
  <div style="font-size: 20px; color: #00d9ff; flex-shrink: 0;">ℹ️</div>
  <div>
    <strong style="color: #00d9ff;">Learn More</strong><br>
    <span style="color: #a0a0a0;">To learn more about advanced usage of value objects, including validation, custom value objects, complex objects like aggregates, visit the <a href="https://dimanu-py.github.io/sindri/value_objects/" style="color: #00d9ff; text-decoration: none;">Value Object Pattern</a> section of the documentation.</span>
  </div>
</div>
