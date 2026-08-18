"""Utility functions for FixMyMeal application."""

from datetime import datetime


def format_date(date_str: str) -> str:
    """Format a date string for display."""
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%b %d, %Y")
    except Exception:
        return date_str


def format_datetime(dt: datetime) -> str:
    """Format a datetime object for display."""
    return dt.strftime("%b %d, %Y at %I:%M %p")


def get_severity_color(severity: str) -> str:
    """Get color for severity level."""
    severity_map = {
        "Low": "🟢",
        "Medium": "🟡",
        "High": "🔴",
        "Critical": "🔴",
    }
    return severity_map.get(severity, "⚪")


def get_category_emoji(category: str) -> str:
    """Get emoji for issue category."""
    category_map = {
        "Hygiene": "🧼",
        "Taste": "👅",
        "Quantity": "📦",
        "Timing": "⏰",
        "Other": "❓",
    }
    return category_map.get(category, "❓")


def validate_complaint(description: str, meal: str) -> tuple[bool, str]:
    """Validate complaint input."""
    if not description or not description.strip():
        return False, "Please enter a complaint description."
    
    if len(description.strip()) < 10:
        return False, "Complaint description should be at least 10 characters."
    
    if meal not in ["Breakfast", "Lunch", "Snacks", "Dinner"]:
        return False, "Please select a valid meal."
    
    return True, ""
