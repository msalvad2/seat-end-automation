# Seat-End Device Automation Framework

A Python-based automation test framework simulating automated testing of
seat-end IFE (In-Flight Entertainment) hardware. Demonstrates core QA
engineering concepts — defensive programming, boundary value testing, pytest
fixtures, and CI/CD pipeline integration with GitHub Actions.

## What it simulates

A seat-end device is the hardware unit embedded in each aircraft seat that
manages the IFE screen — power state, volume, channel selection, brightness,
and the flight attendant call button. In real avionics testing, automated
test suites run against these devices to verify software behavior before
deployment. This project mocks that device in Python and validates its
behavior with a full pytest suite wired into a CI/CD pipeline.

## Project structure

```
seat-end-automation/
├── device/
│   └── seat_device.py       # Mock seat-end IFE device class
├── tests/
│   └── test_seat_device.py  # pytest test suite (18 test cases)
├── .github/
│   └── workflows/
│       └── ci.yml           # GitHub Actions CI/CD pipeline
├── requirements.txt
└── README.md
```

## Key concepts demonstrated

**Defensive programming** — every method validates device state and input
boundaries before executing. Commands sent to a powered-off device raise
a RuntimeError immediately. Out-of-range values raise a ValueError. The
goal is to fail fast with a clear error message rather than letting bad
state silently propagate and cause hard-to-trace bugs downstream.

**Boundary value testing** — tests cover exact boundary values (0, 100)
and out-of-range values (-1, 101) because that is where off-by-one errors
hide. Testing only the middle of a range gives false confidence that
validation logic is correct.

**pytest fixtures** — `device_off` and `device_on` fixtures provide
consistent, reusable setup so every test starts from a known, predictable
state. This mirrors how real hardware test frameworks manage device
initialization before each test run.

**CI/CD pipeline** — GitHub Actions runs the full test suite automatically
on every push to a fresh Ubuntu environment, then publishes an HTML test
report as a downloadable artifact. Every push is verified — no broken code
gets merged silently.

## Running locally

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# Run tests with HTML report
pytest tests/ -v --html=reports/report.html --self-contained-html
```

## CI/CD

Every push triggers the GitHub Actions pipeline automatically. View
pipeline runs and download test reports in the Actions tab.