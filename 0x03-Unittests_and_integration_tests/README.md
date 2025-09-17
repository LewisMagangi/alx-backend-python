# 0x03-Unittests_and_integration_tests

This directory contains code and tests for unit testing and integration testing in Python. The focus is on best practices for writing, organizing, and running tests for Python modules.

## Contents

- `client.py` - Example client code for integration testing
- `fixtures.py` - Test fixtures for use in unit/integration tests
- `utils.py` - Utility functions to be tested
- `test_client.py` - Integration tests for client code
- `test_utils.py` - Unit tests for utility functions

## How to Run Tests

You can run all tests in this directory using:

``` text
python3 -m unittest discover .
```

Or run a specific test file:

``` text
python3 -m unittest test_utils.py
python3 -m unittest test_client.py
```

## Key Concepts Covered

- Writing unit tests with `unittest`
- Using test fixtures and setup/teardown methods
- Mocking and patching dependencies
- Writing integration tests for client-server interactions
- Organizing tests for maintainability

## Requirements

- Python 3.6+
- No external dependencies required for basic tests

---

Feel free to add more tests or utilities as you expand your project!
