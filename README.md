# tz-kit

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-brightgreen.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

**A modern timezone toolkit for Python microservices (FastAPI/Starlette).** Built on `zoneinfo` (PEP 615), following Django-inspired timezone handling patterns.

## Core Philosophy
1. **UTC is the language of systems.** Everything stored in the database or passed between services is in UTC.
2. **Local time is the language of users.** The system accepts and provides time in the user's preferred timezone at the edge (middleware).

## How it Works
The package follows a "Set and Forget" architectural pattern:

1. **Extraction**: `TimezoneMiddleware` intercepts every incoming request and looks for the `X-Timezone` header (e.g., `Asia/Kolkata`).
2. **Contextualization**: It sets this timezone in an async-safe `ContextVar`. This ensures that even in highly concurrent environments, each request runs in its own timezone "bubble".
3. **Normalization**: When a Pydantic model uses the `LocalDateTime` type, it automatically detects:
    - **Naive datetimes**: Converted from the request's timezone to UTC.
    - **Time-only strings/objects** (e.g., "10:30"): Anchored to *today* in the request's timezone and converted to UTC.
    - **Flexible Formats**: Handles non-standard separators like `2026:01:10 10:56` or `2026/01/10`.
    - **ISO datetimes**: Normalized to UTC.

### Request Flow Overview

```mermaid
graph TD
    A[Client Request] -->|X-Timezone: Asia/Kolkata| B(TimezoneMiddleware)
    B -->|set_timezone| C{ContextVar}
    C --> D[Business Logic / Pydantic Models]
    D -->|LocalDateTime Validator| E[Normalized UTC Datetime]
    E -->|Store| F[(Database / UTC)]

    style B fill:#f9f,stroke:#333Internal
    style C fill:#bbf,stroke:#333Context
    style E fill:#bfb,stroke:#333UTC
```

## Key Features
- **Modern Python**: Built on `zoneinfo` (PEP 615).
- **Pydantic Integration**: Seamlessly handles timezone conversion in request schemas.
- **Async Ready**: Uses `ContextVar` for thread-safe/async-safe context management.
- **Microservices Ready**: Optimized for the `X-Timezone` header standard.
- **Industry Grade**: Handles DST gaps/overlaps and extreme dates correctly.

## Installation

### For Development (Contributors)
If you're developing this package locally:
```bash
pip install -r requirements.txt
```

### For Production Use (Install in Your Project)
Install directly from GitHub to use in your microservices:

**Install a specific version (Recommended):**
```bash
pip install "git+https://github.com/arun143143/tz-kit.git@v1.0.0"
```

**Install the latest version from main branch:**
```bash
pip install "git+https://github.com/arun143143/tz-kit.git"
```

**Or add to your `requirements.txt`:**
```
tz-kit @ git+https://github.com/arun143143/tz-kit.git@v1.0.0
```

## Quick Start

### 1. Register Middleware
```python
from fastapi import FastAPI
from tz_kit import TimezoneMiddleware

app = FastAPI()
app.add_middleware(TimezoneMiddleware)
```

### 2. Use LocalDateTime in Models
```python
from pydantic import BaseModel
from tz_kit import LocalDateTime

class AppointmentSchema(BaseModel):
    start_time: LocalDateTime # Automatically converts naive inputs to UTC
```

### 3. Manual Conversion Helpers
```python
from tz_kit import utc_to_local, local_to_utc

# Manual conversion when needed
local_time = utc_to_local(utc_datetime)
```


## Validation Modes
- **Lenient (Default)**: If an invalid timezone is provided, the system falls back to UTC to ensure production availability.
- **Strict**: Use `set_timezone(tz, strict=True)` for internal tasks or validation to raise an `InvalidTimezoneError`.

## Requirements
- Python 3.9+
- Pydantic >= 2.5
- Starlette >= 0.36
- tzdata >= 2024.1

## Testing
Run the test suite:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=tz_kit --cov-report=html
```

## Contributing
Contributions are welcome! Please ensure:
1. All tests pass (`pytest`)
2. Code is formatted with `black` and `ruff`
3. Pre-commit hooks are satisfied (run `pre-commit install`)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Links
- **Repository**: [https://github.com/arun143143/tz-kit](https://github.com/arun143143/tz-kit)
- **Issues**: [https://github.com/arun143143/tz-kit/issues](https://github.com/arun143143/tz-kit/issues)

---
**Made with ❤️ for microservices**
