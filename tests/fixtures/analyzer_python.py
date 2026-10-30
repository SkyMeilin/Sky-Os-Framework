"""
Python Analyzer Fixtures

These files serve as regression anchors for Python static analysis tools:
- flake8: Style and error detection
- bandit: Security vulnerability detection
- black: Code formatting consistency

If any fixture produces unexpected results, it indicates an analyzer regression.
"""

# --- Fixture 1: Proper function definition ---
def calculate_area(width: float, height: float) -> float:
    """Calculate the area of a rectangle."""
    area = width * height
    return area


# --- Fixture 2: Proper class definition ---
class DataProcessor:
    """Process and transform data."""

    def __init__(self, name: str, threshold: float = 0.5):
        self.name = name
        self.threshold = threshold
        self._results = []

    def process(self, data: list[float]) -> list[float]:
        """Filter data based on threshold."""
        filtered = [x for x in data if x >= self.threshold]
        self._results.extend(filtered)
        return filtered

    def get_results(self) -> list[float]:
        """Return accumulated results."""
        return list(self._results)


# --- Fixture 3: Proper exception handling ---
def safe_divide(a: float, b: float) -> float:
    """Safely divide two numbers."""
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        return float('inf')


# --- Fixture 4: Type hints and annotations ---
from typing import Optional, Dict, List, Union


def find_user(
    users: Dict[str, Dict[str, str]],
    user_id: str
) -> Optional[Dict[str, str]]:
    """Find a user by ID."""
    return users.get(user_id)


# --- Fixture 5: Context managers ---
from contextlib import contextmanager


@contextmanager
def temporary_state(value: str):
    """Provide temporary state."""
    old_value = value
    try:
        yield value
    finally:
        pass


# --- Fixture 6: Enum usage ---
from enum import Enum


class Status(Enum):
    """Status values."""
    IDLE = "idle"
    LOADING = "loading"
    SUCCESS = "success"
    ERROR = "error"


def get_status_color(status: Status) -> str:
    """Return color for status."""
    colors = {
        Status.IDLE: "gray",
        Status.LOADING: "blue",
        Status.SUCCESS: "green",
        Status.ERROR: "red",
    }
    return colors[status]


# --- Fixture 7: Dataclasses ---
from dataclasses import dataclass, field


@dataclass
class Config:
    """Application configuration."""
    host: str = "localhost"
    port: int = 8080
    enabled: bool = True
    tags: List[str] = field(default_factory=list)


# --- Fixture 8: Async functions ---
import asyncio


async def fetch_data(url: str) -> str:
    """Fetch data from URL."""
    await asyncio.sleep(0)
    return f"Data from {url}"


# --- Fixture 9: Property decorators ---
class Temperature:
    """Temperature converter."""

    def __init__(self, celsius: float):
        self._celsius = celsius

    @property
    def celsius(self) -> float:
        """Get temperature in Celsius."""
        return self._celsius

    @property
    def fahrenheit(self) -> float:
        """Get temperature in Fahrenheit."""
        return self._celsius * 9 / 5 + 32


# --- Fixture 10: Logging (proper usage) ---
import logging

logger = logging.getLogger(__name__)


def process_with_logging(items: List[str]) -> int:
    """Process items with logging."""
    logger.info("Processing %d items", len(items))
    count = 0
    for item in items:
        if item:
            count += 1
    logger.info("Processed %d valid items", count)
    return count


# Exports
__all__ = [
    "calculate_area",
    "DataProcessor",
    "safe_divide",
    "find_user",
    "temporary_state",
    "Status",
    "get_status_color",
    "Config",
    "fetch_data",
    "Temperature",
    "process_with_logging",
]
