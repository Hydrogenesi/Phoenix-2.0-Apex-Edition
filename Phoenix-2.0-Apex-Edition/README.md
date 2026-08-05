# TUA

MATRIUN is a lightweight matrix utility library with a small command-line demo.

## Install

Install from the project root:

```bash
pip install .
```

For editable development installs:

```bash
pip install -e .
```

## Python Usage

```python
from matriun import create_identity_matrix, multiply_matrices

identity = create_identity_matrix(3)
result = multiply_matrices(identity, [[2, 1, 0], [0, 3, 0], [0, 0, 4]])
print(result)
```

## CLI Demo

After installation, run:

```bash
matriun demo
```

You can also specify the demo matrix size:

```bash
matriun demo --size 4
```

Show help:

```bash
matriun --help
```