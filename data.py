"""Mock data for FixMyMeal application."""

from datetime import datetime, timedelta
from models import Issue


def get_mock_menu():
    """Get a week's worth of mock menu data."""
    today = datetime.now().date()
    
    menu_data = {
        (today + timedelta(days=0)).isoformat(): {
            "breakfast": ["Idli", "Sambar", "Chutney", "Tea"],
            "lunch": ["Rice", "Dal", "Paneer Curry", "Roti", "Salad"],
            "snacks": ["Samosa", "Tea"],
            "dinner": ["Chapati", "Rajma", "Rice", "Mixed Vegetables"],
        },
        (today + timedelta(days=1)).isoformat(): {
            "breakfast": ["Dosa", "Sambar", "Chutney", "Coffee"],
            "lunch": ["Jeera Rice", "Chana Masala", "Cabbage Fry", "Puri", "Pickle"],
            "snacks": ["Pakora", "Tea"],
            "dinner": ["Roti", "Chole Curry", "Rice", "Cucumber Salad"],
        },
        (today + timedelta(days=2)).isoformat(): {
            "breakfast": ["Poha", "Jaggery", "Peanuts", "Tea"],
            "lunch": ["White Rice", "Moong Dal", "Aloo Gobi", "Bhakri", "Pickle"],
            "snacks": ["Biscuit", "Tea"],
            "dinner": ["Missi Roti", "Beans Masala", "Rice", "Carrot Salad"],
        },
        (today + timedelta(days=3)).isoformat(): {
            "breakfast": ["Upma", "Chutney", "Boiled Egg", "Tea"],
            "lunch": ["Basmati Rice", "Kidney Beans Curry", "Broccoli Fry", "Naan", "Raita"],
            "snacks": ["Chakli", "Coffee"],
            "dinner": ["Tawa Roti", "Paneer Do Pyaza", "Rice", "Tomato Salad"],
        },
        (today + timedelta(days=4)).isoformat(): {
            "breakfast": ["Puri", "Aloo Curry", "Chutney", "Tea"],
            "lunch": ["Brown Rice", "Lentil Soup", "Spinach Curry", "Roti", "Salad"],
            "snacks": ["Samosa", "Tea"],
            "dinner": ["Chapati", "Rajma", "Rice", "Mixed Vegetables"],
        },
        (today + timedelta(days=5)).isoformat(): {
            "breakfast": ["Idli", "Sambar", "Chutney", "Tea"],
            "lunch": ["Rice", "Dal", "Paneer Curry", "Roti", "Salad"],
            "snacks": ["Pakora", "Tea"],
            "dinner": ["Roti", "Chole Curry", "Rice", "Cucumber Salad"],
        },
        (today + timedelta(days=6)).isoformat(): {
            "breakfast": ["Dosa", "Sambar", "Chutney", "Coffee"],
            "lunch": ["Jeera Rice", "Chana Masala", "Cabbage Fry", "Puri", "Pickle"],
            "snacks": ["Biscuit", "Tea"],
            "dinner": ["Chapati", "Rajma", "Rice", "Mixed Vegetables"],
        },
    }
    
    return menu_data


def get_today_menu():
    """Get today's menu."""
    today = datetime.now().date().isoformat()
    menu_data = get_mock_menu()
    return menu_data.get(today, {
        "breakfast": ["Idli", "Sambar", "Chutney", "Tea"],
        "lunch": ["Rice", "Dal", "Paneer Curry", "Roti", "Salad"],
        "snacks": ["Samosa", "Tea"],
        "dinner": ["Chapati", "Rajma", "Rice", "Mixed Vegetables"],
    })


def get_mock_issues():
    """Get sample mock issues for the feed."""
    today = datetime.now().date()
    
    mock_issues = [
        Issue(
            id="1",
            description="Found a small stone-like object in the dal during lunch. The food quality was compromised.",
            meal="Lunch",
            date=today.isoformat(),
            created_at=datetime.now(),
            status="Reported",
            category="Hygiene",
            severity="High",
            summary="Possible foreign object visible in the dal served at lunch.",
        ),
        Issue(
            id="2",
            description="The paneer curry served yesterday was excessively salty and almost inedible.",
            meal="Lunch",
            date=(today - timedelta(days=1)).isoformat(),
            created_at=datetime.now() - timedelta(days=1),
            status="Reported",
            category="Taste",
            severity="Medium",
            summary="Student reports paneer curry was excessively salty.",
        ),
        Issue(
            id="3",
            description="The rice portions were significantly reduced. Not enough food for a filling meal.",
            meal="Dinner",
            date=(today - timedelta(days=2)).isoformat(),
            created_at=datetime.now() - timedelta(days=2),
            status="Reported",
            category="Quantity",
            severity="Medium",
            summary="Student reports insufficient rice portions at dinner.",
        ),
        Issue(
            id="4",
            description="Breakfast was delayed by about 15 minutes today. Many students had to skip it due to class timings.",
            meal="Breakfast",
            date=(today - timedelta(days=3)).isoformat(),
            created_at=datetime.now() - timedelta(days=3),
            status="Reported",
            category="Timing",
            severity="Low",
            summary="Breakfast service was delayed by approximately 15 minutes.",
        ),
        Issue(
            id="5",
            description="The bread served with morning tea seemed stale and hard. Appeared to be from a previous day.",
            meal="Breakfast",
            date=(today - timedelta(days=4)).isoformat(),
            created_at=datetime.now() - timedelta(days=4),
            status="Reported",
            category="Taste",
            severity="Low",
            summary="Student reports bread served with morning tea appeared stale.",
        ),
    ]
    
    return mock_issues
