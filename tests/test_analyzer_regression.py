"""
Python Analyzer Regression Tests

These tests verify that Python static analysis tools (flake8, bandit, black)
behave consistently against the fixture files. They catch regressions where
analyzer configuration changes cause false positives or missed detections.
"""

import subprocess
import sys
from pathlib import Path

import pytest

# Path to the fixtures directory
FIXTURES_DIR = Path(__file__).parent / "fixtures"
PYTHON_FIXTURE = FIXTURES_DIR / "analyzer_python.py"


class TestPythonAnalyzerRegression:
    """Test suite for Python analyzer regression detection."""

    def test_fixture_file_exists(self):
        """Verify the fixture file exists."""
        assert PYTHON_FIXTURE.exists(), f"Fixture not found: {PYTHON_FIXTURE}"

    def test_fixture_imports_cleanly(self):
        """Verify the fixture module can be imported without errors."""
        import tests.fixtures.analyzer_python as fixtures  # noqa: F401

        assert fixtures is not None

    def test_fixture_functions_callable(self):
        """Verify fixture functions are callable and return expected types."""
        from tests.fixtures.analyzer_python import (
            calculate_area,
            safe_divide,
            get_status_color,
            Status,
            DataProcessor,
            Config,
            Temperature,
        )

        # Test calculate_area
        area = calculate_area(5.0, 10.0)
        assert area == 50.0
        assert isinstance(area, float)

        # Test safe_divide
        result = safe_divide(10.0, 2.0)
        assert result == 5.0

        inf_result = safe_divide(1.0, 0.0)
        assert inf_result == float('inf')

        # Test get_status_color
        color = get_status_color(Status.SUCCESS)
        assert color == "green"

        # Test DataProcessor
        processor = DataProcessor("test", threshold=0.5)
        result = processor.process([0.3, 0.6, 0.8, 0.2])
        assert result == [0.6, 0.8]

        # Test Config dataclass
        config = Config(host="localhost", port=8080)
        assert config.host == "localhost"
        assert config.port == 8080
        assert config.enabled is True

        # Test Temperature
        temp = Temperature(100.0)
        assert temp.celsius == 100.0
        assert abs(temp.fahrenheit - 212.0) < 0.01

    def test_flake8_passes_on_fixture(self):
        """Verify flake8 passes on the fixture file without errors."""
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "flake8",
                str(PYTHON_FIXTURE),
                "--max-line-length=120",
                "--ignore=E501,W503",
            ],
            capture_output=True,
            text=True,
        )

        # flake8 should exit with 0 (no issues found)
        assert result.returncode == 0, (
            f"flake8 failed on fixture:\n{result.stdout}\n{result.stderr}"
        )

    def test_black_format_check_on_fixture(self):
        """Verify black formatting is consistent on the fixture file."""
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "black",
                "--check",
                str(PYTHON_FIXTURE),
            ],
            capture_output=True,
            text=True,
        )

        # black --check should exit with 0 (file is formatted)
        assert result.returncode == 0, (
            f"black formatting check failed on fixture:\n{result.stdout}\n{result.stderr}"
        )

    def test_fixture_type_hints_present(self):
        """Verify that fixture functions have proper type hints."""
        from tests.fixtures.analyzer_python import (
            calculate_area,
            safe_divide,
            get_status_color,
        )
        import inspect

        # Check calculate_area signature
        sig = inspect.signature(calculate_area)
        for param_name, param in sig.parameters.items():
            assert param.annotation != inspect.Parameter.empty, (
                f"Parameter {param_name} in calculate_area missing type hint"
            )
        assert sig.return_annotation != inspect.Signature.empty, (
            "calculate_area missing return type hint"
        )

        # Check safe_divide signature
        sig = inspect.signature(safe_divide)
        for param_name, param in sig.parameters.items():
            assert param.annotation != inspect.Parameter.empty, (
                f"Parameter {param_name} in safe_divide missing type hint"
            )

    def test_fixture_docstrings_present(self):
        """Verify that fixture functions have docstrings."""
        from tests.fixtures.analyzer_python import (
            calculate_area,
            DataProcessor,
            safe_divide,
            Status,
            Config,
        )

        assert calculate_area.__doc__ is not None
        assert DataProcessor.__doc__ is not None
        assert DataProcessor.process.__doc__ is not None
        assert safe_divide.__doc__ is not None
        assert Status.__doc__ is not None
        assert Config.__doc__ is not None


class TestAnalyzerBenchmark:
    """Benchmark tests to detect performance regressions in analyzers."""

    def test_flake8_analysis_time(self):
        """Measure flake8 analysis time on fixture (baseline: < 1 second)."""
        import time

        start = time.perf_counter()
        subprocess.run(
            [
                sys.executable,
                "-m",
                "flake8",
                str(PYTHON_FIXTURE),
                "--max-line-length=120",
            ],
            capture_output=True,
        )
        elapsed = time.perf_counter() - start

        # Should complete in under 1 second on modern hardware
        assert elapsed < 1.0, (
            f"flake8 took {elapsed:.3f}s on fixture, expected < 1.0s"
        )

    def test_black_format_time(self):
        """Measure black formatting time on fixture (baseline: < 1 second)."""
        import time

        start = time.perf_counter()
        subprocess.run(
            [
                sys.executable,
                "-m",
                "black",
                "--check",
                str(PYTHON_FIXTURE),
            ],
            capture_output=True,
        )
        elapsed = time.perf_counter() - start

        # Should complete in under 1 second on modern hardware
        assert elapsed < 1.0, (
            f"black took {elapsed:.3f}s on fixture, expected < 1.0s"
        )
