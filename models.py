"""Data models for FixMyMeal application."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class AIAnalysis:
    """AI-generated analysis of a complaint."""
    category: str
    severity: str
    summary: str


@dataclass
class Issue:
    """A reported food quality issue."""
    id: str
    description: str  # Original student complaint
    meal: str  # Breakfast, Lunch, Snacks, Dinner
    date: str  # YYYY-MM-DD
    created_at: datetime
    status: str = "Reported"  # Default status for MVP
    image: Optional[bytes] = None
    has_evidence: bool = False
    
    # AI-generated fields
    category: Optional[str] = None
    severity: Optional[str] = None
    summary: Optional[str] = None
    
    def __post_init__(self):
        """Set has_evidence flag based on image presence."""
        self.has_evidence = self.image is not None


@dataclass
class MenuItem:
    """A menu item for a meal."""
    breakfast: list = field(default_factory=list)
    lunch: list = field(default_factory=list)
    snacks: list = field(default_factory=list)
    dinner: list = field(default_factory=list)
