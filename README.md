# ftw-devtools

**A lightweight Testing Infrastructure Utility for isolated environment sandboxing.**

`ftw-devtools` provides essential tools to manage test environments, specifically designed to protect your host system from side effects during CLI and filesystem-related testing.

## Key Features
* **TestHomeEnvironment**: A robust sandbox that redirects `HOME` and neutralizes `XDG` environment variables to isolate the developer's actual system.
* **Filesystem Orchestration**: Helpers to deploy configuration, data, and cache files into simulated user directories.
* **Doc-Include Integration**: Seamlessly copy test-generated artifacts into your documentation build.

## Installation
```bash
pip install ftw-devtools
```

## Usage
The package uses the `fitzzftw.devtools` namespace.

```python
from fitzzftw.devtools.testinfra import TestHomeEnvironment
```
